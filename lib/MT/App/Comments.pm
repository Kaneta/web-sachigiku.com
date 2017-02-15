# Copyright 2001-2004 Six Apart. This code cannot be redistributed without
# permission from www.movabletype.org.
#
# $Id: Comments.pm,v 1.71.4.1 2004/12/16 01:51:31 ezra Exp $

package MT::App::Comments;
use strict;

use MT::App;
@MT::App::Comments::ISA = qw( MT::App );

use MT::Comment;
use MT::I18N;
use MT::Util qw( remove_html encode_html decode_url );
use MT::Entry qw(:constants);
use MT::Author qw(:constants);

my $COMMENTER_COOKIE_NAME = "tk_commenter";

sub init {
    my $app = shift;
    $app->SUPER::init(@_) or return;
    $app->add_methods(
        preview => \&preview,
        post => \&post,
        view => \&view,
        handle_sign_in => \&handle_sign_in,
        cmtr_name_js => \&commenter_name_js,
        red => \&do_red,
    );
    $app->{default_mode} = 'view';
    $app->{charset} = $app->{cfg}->PublishCharset;
    my $q = $app->{query};

    ## We don't really have a __mode parameter, because we have to
    ## use named submit buttons for Preview and Post. So we hack it.
    if ($q->param('post')) {
        $q->param('__mode', 'post');
    } elsif ($q->param('preview')) {
        $q->param('__mode', 'preview');
    }
    $app;
}

#
# $app->_get_commenter_session()
#
# Creates a commenter record based on the cookies in the $app, if
# one already exists corresponding to the browser's session.
#
# Returns a pair ($session_key, $commenter) where $session_key is the
# key to the MT::Session object (as well as the cookie value) and
# $commenter is an MT::Author record. Both values are undef when no
# session is active.
#
sub _get_commenter_session {
    my $app = shift;
    my $q = $app->{query};
    
    my $session_key;
    
    my %cookies = $app->cookies();
    if (!$cookies{$COMMENTER_COOKIE_NAME}) {
        return (undef, undef);
    }
    $session_key = $cookies{$COMMENTER_COOKIE_NAME}->value() || "";
    $session_key =~ y/+/ /;
    require MT::Session;
    my $sess_obj = MT::Session->load({ id => $session_key });
    my $timeout = $app->{cfg}->CommentSessionTimeout;
    if (!$sess_obj || ($sess_obj->start() + $timeout < time))
    {
        $session_key = undef;
        
        # blotto the cookie
        my %dead_kookee = (-name => $COMMENTER_COOKIE_NAME,
                           -value => '',
                           -path => '/',
                           -expires => '-10y');
        $app->bake_cookie(%dead_kookee);
        my %dead_name_kookee = (-name => "commenter_name",
                                -value => '',
                                -path => '/',
                                -expires => '-10y');
        $app->bake_cookie(%dead_name_kookee);
        $sess_obj->remove() if ($sess_obj);
        $sess_obj = undef;
        return (undef, undef);
    } else {
        # session is valid!
        return ($session_key, MT::Author->load({name => $sess_obj->name,
                                                type=>MT::Author::COMMENTER}));
    }
}

sub do_red {
    my $app = shift;
    my $q = $app->{query};
    my $id = $q->param('id') or return $app->error("No id");
    my $comment = MT::Comment->load($id)
        or return $app->error("No such comment");
    my $uri = encode_html($comment->url);
    return <<HTML;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head><title>Redirecting...</title>
<meta name="robots" content="noindex, nofollow">
<script type="text/javascript">
window.onload = function() { document.location = '$uri'; };
</script></head>
<body>
<p><a href="$uri">Click here</a> if you are not redirected</p>
</body>
</html>
HTML
}

# _builtin_throttle is the builtin throttling code
# others can be added by plugins
# a filtering callback must return true or false; true
#    means OK, false means filter it out.
sub _builtin_throttle {
    my $eh = shift;
    my $app = shift;
    my ($entry) = @_;

    my $throttle_period = $app->{cfg}->ThrottleSeconds;
    my $user_ip = $app->remote_ip;
    return 1 if ($throttle_period <= 0);    # Disabled by ThrottleSeconds 0

    require MT::Util;
    my @ts = MT::Util::offset_time_list(time - $throttle_period,
                                        $entry->blog_id);
    my $from = sprintf("%04d%02d%02d%02d%02d%02d",
                       $ts[5]+1900, $ts[4]+1, @ts[3,2,1,0]);
    require MT::Comment;
    
    if (MT::Comment->count({ ip => $user_ip,
                             created_on => [$from],
                             blog_id => $entry->blog_id},
                           {range => {created_on => 1} }))
    {
        return 0;                          # Put a collar on that puppy.
    }
    @ts = MT::Util::offset_time_list(time - $throttle_period * 10 - 1,
                                     $entry->blog_id);
    $from = sprintf("%04d%02d%02d%02d%02d%02d",
                    $ts[5]+1900, $ts[4]+1, @ts[3,2,1,0]);
    my $count =  MT::Comment->count({ ip => $user_ip,
                                      created_on => [$from],
                                      blog_id => $entry->blog_id },
                                    { range => {created_on => 1} });
    if ($count >= 8)
    {
        require MT::IPBanList;
        my $ipban = MT::IPBanList->new();
        $ipban->blog_id($entry->blog_id);
        $ipban->ip($user_ip);
        $ipban->save();
        $ipban->commit();
        $app->log("IP $user_ip banned because comment rate " .
                  "exceeded 8 comments in " .
                  10 * $throttle_period . " seconds.\n");
        require MT::Mail;
        my $author = $entry->author;
        $app->set_language($author->preferred_language)
            if $author && $author->preferred_language;
        
        my $blog = MT::Blog->load($entry->blog_id);
        if ($author && $author->email) {
            my %head = ( To => $author->email,
                         From => $app->{cfg}->EmailAddressMain,
                         Subject =>
                         '[' . $blog->name . '] ' .
                         $app->translate("IP Banned Due to Excessive Comments"));
            my $charset = $app->{cfg}->PublishCharset || 'iso-8859-1';
            $head{'Content-Type'} = qq(text/plain; charset="$charset");
            my $body = $app->translate('_THROTTLED_COMMENT_EMAIL',
                                       $blog->name, 10 * $throttle_period,
                                       $user_ip, $user_ip);
            $body = MT::I18N::wrap_text($body,72);
            MT::Mail->send(\%head, $body);
        }
        return 0;
    }
    return 1;
}

sub post {
    my $app = shift;
    my $q = $app->{query};

    return do_preview($app, $q, @_) if $app->request_method() ne 'POST';

    my $entry_id = $q->param('entry_id')
        or return $app->error("No entry_id");
    require MT::Entry;
    my $entry = MT::Entry->load($entry_id)
        or return $app->error($app->translate(
            "No such entry '[_1]'.", scalar $q->param('entry_id')));
    return $app->error($app->translate(
                       "No such entry '[_1]'.", scalar $q->param('entry_id')))
        if $entry->status != RELEASE;

    require MT::IPBanList;
    my $iter = MT::IPBanList->load_iter({ blog_id => $entry->blog_id });
    while (my $ban = $iter->()) {
        my $banned_ip = $ban->ip;
        if ($app->remote_ip =~ /$banned_ip/) {
            return $app->handle_error($app->translate(
                                      "You are not allowed to post comments."));
        }
    }

    # FIXME: move this to startup time (would it make a difference? maybe not)
    MT->add_callback('CommentThrottleFilter', 1, undef,
                     \&MT::App::Comments::_builtin_throttle);

    # Run all the Comment-throttling callbacks
    my $passed_filter = MT->run_callbacks('CommentThrottleFilter',
                                          $app, $entry);

    $passed_filter ||
        return $app->handle_error($app->translate("_THROTTLED_COMMENT"),
                                  "403 Throttled");

    if (my $state = $q->param('comment_state')) {
        require MT::Serialize;
        my $ser = MT::Serialize->new($app->{cfg}->Serializer);
        $state = $ser->unserialize(pack 'H*', $state);
        $state = $$state;
        for my $f (keys %$state) {
            $q->param($f, $state->{$f});
        }
    }
    unless ($entry->allow_comments eq '1') {
        return $app->handle_error($app->translate(
            "Comments are not allowed on this entry."));
    }

    require MT::Blog;
    my $blog = MT::Blog->load($entry->blog_id);

    if (!$q->param('text')) {
       return $app->handle_error($app->translate("Comment text is required."));
    }
    my ($comment, $commenter) = _make_comment($app, $entry);
    if (!$blog->allow_unreg_comments) {
        if (!$commenter) {
            return $app->handle_error($app->translate(
                                      "Registration is required."))
        }
    }
    if (!$blog->allow_anon_comments && 
        (!$comment->author || !$comment->email)) {
        return $app->handle_error($app->translate(
                           "Name and email address are required."));
    }
    if ($blog->allow_unreg_comments()) {
        $comment->email($q->param('email')) unless $comment->email();
    }
    if ($comment->email) {
        require MT::Util;
        if (my $fixed = MT::Util::is_valid_email($comment->email)) {
            $comment->email($fixed);
        } elsif ($comment->email =~ /^[0-9A-F]{40}$/i) {
            # It's a FOAF-style mbox hash; accept it if blog config says to.
            return $app->handle_error("A real email address is required")
                if ($blog->require_comment_emails());
        } else {
            return $app->handle_error($app->translate(
                "Invalid email address '[_1]'", $comment->email));
        }
    }
    if ($comment->url) {
        require MT::Util;
        if (my $fixed = MT::Util::is_valid_url($comment->url, 'stringent')) {
            $comment->url($fixed);
        } else {
            return $app->handle_error($app->translate(
                "Invalid URL '[_1]'", $comment->url));
        }
    }
    
    return $app->handle_error($app->errstr()) unless $comment;

    ## Here comes the fancy logic for deciding whether or not the
    ## comment appears.

    if ($commenter) {
        # First, auto-approve if necessary.
        if (!$blog->manual_approve_commenters &&
            ($commenter->status($entry->blog_id) == PENDING))
        {
            $commenter->approve($entry->blog_id);
        }
        # If the commenter is approved, publish the comment.
        if ($commenter->status($blog->id) == APPROVED) {
            $comment->visible(1);
        }
    } else {
        # We don't have a commenter object, but the user wasn't booted
        # so unless moderation is on, we can publish the comment.
        unless ($blog->moderate_unreg_comments) {
            $comment->visible(1);
        }
    }

    # Form a link to the comment
    my $comment_link;
    if (!$q->param('static')) {
        my $url = $app->base . $app->uri;
        $url .= '?entry_id=' . $q->param('entry_id');
        $url .= '&static=0&arch=1' if ($q->param('arch'));
        $comment_link = $url;
    } else {
        my $static = $q->param('static');
        if ($static == 1) {
            # I think what we really want is the individual archive.
            $comment_link = $entry->permalink;
        } else {
            $comment_link = $static . '#' . $comment->id;
        }
    }

    if (!$commenter || $commenter->status($blog->id) != BLOCKED)
    {
        # Before saving this comment, check whether this commenter has
        # placed any other comments on the entry's author's other entries.
        # (on any other entries by the same author as this one)
        
        my $commenter_has_comment = 0;
        if ($commenter) {
            my $other_comment=MT::Comment->load({commenter_id=>$commenter->id});
            if ($other_comment) {
                my $other_entry
                   =MT::Entry->load({author_id => $entry->author_id},
                                    {join=>['MT::Comment', 'entry_id',
                                            {commenter_id=>$commenter->id},{}]});
                $commenter_has_comment = !!$other_entry;
            }
        }

        if (MT->run_callbacks('CommentFilter', $app, $comment))
        {
            $comment->save;
            $blog->touch;
            $blog->save;

            if ($comment->visible) {
                # Rebuild the entry synchronously so that if the user gets
                # redirected to the indiv. page it will be up-to-date.
                $app->rebuild_entry( Entry => $entry )
                    or return $app->error($app->translate(
                                          "Rebuild failed: [_1]", $app->errstr));
                # Index rebuilds and notifications are done in the background.
                MT::Util::start_background_task(sub {
                    $app->rebuild_indexes( Blog => $blog )
                        or return $app->error($app->translate(
                                              "Rebuild failed: [_1]", $app->errstr));
                    my $send_notfn_email = 0;
                    if (!$commenter) {
                        $send_notfn_email = !$comment->visible();
                    } else {
                        $send_notfn_email = !$commenter_has_comment
                            && !$comment->visible();
                    }
                    if ($blog->email_new_comments || $send_notfn_email)
                    {
                        $app->_send_comment_notification($comment, $comment_link,
                                                         $entry, $blog);
                    }
                });
            }
        }
    }
    MT::Util::start_background_task(
            sub {
                 _expire_sessions($app->{cfg}->CommentSessionTimeout)
                });
    if (!$comment->visible) {
        return $app->preview('pending');
    } else {
        return $app->redirect($comment_link);
    }
}

#
# $app->_make_comment($entry)
#
# _make_comment creates an MT::Comment record attached to the $entry,
# based on the query information in $app (It neeeds the whole app object
# so it can get the user's IP). Also creates an MT::Author record
# representing the person who placed the comment, if necessary.
#
# Always returns a pair ($comment, $commenter). The latter is undef if
# there is no commenter for the session (or if there is no active
# session).
#
# Validation of the comment data is left to the caller.
#
sub _make_comment {
    my ($app, $entry) = @_;
    my $q = $app->{query};
    
    my $nick = $q->param('author');
    my $email = $q->param('email');
    my ($session, $commenter) = $app->_get_commenter_session();
    if ($commenter) {
        $nick = $commenter->nickname();
        $email = $commenter->email();
    }
    my $url = $q->param('url') || ($commenter ? $commenter->url() : '');
    my $comment = MT::Comment->new;
    if ($commenter) {
        $comment->commenter_id($commenter->id);
    }
    $comment->ip($app->remote_ip);
    $comment->blog_id($entry->blog_id);
    $comment->entry_id($entry->id);
    $comment->author(remove_html($nick));
    $comment->email(remove_html($email));
    $comment->url(MT::Util::is_valid_url($url, 'stringent'));
    $comment->text($q->param('text'));
    
    return ($comment, $commenter);
}

sub _send_comment_notification {
    my $app = shift;
    my ($comment, $comment_link, $entry, $blog) = @_;
    require MT::Mail;
    my $author = $entry->author;
    $app->set_language($author->preferred_language)
        if $author && $author->preferred_language;
    my $from_addr = $comment->email 
        || $app->{cfg}->EmailAddressMain || $author->email;
    use MT::Util qw(is_valid_email);
    if (!is_valid_email($from_addr)) {
        $from_addr = $app->{cfg}->EmailAddressMain || $author->email;
    }
    if ($author && $author->email) {
        my %head = ( To => $author->email,
                     From => $from_addr,
                     Subject =>
                     '[' . $blog->name . '] ' .
                     $app->translate('New Comment Posted to \'[_1]\'',
                                     $entry->title)
                   );
        my $charset = $app->{cfg}->PublishCharset || 'iso-8859-1';
        $head{'Content-Type'} = qq(text/plain; charset="$charset");
        my $base = $app->base . $app->path . $app->{cfg}->AdminScript;
        my %param = (
                     blog_name => $blog->name,
                     entry_id => $entry->id,
                     entry_title => $entry->title,
                     view_url => $comment_link,
                     edit_url => $base . '?__mode=view&blog_id=' . $blog->id
                                 . '&_type=comment&id=' . $comment->id,
                     ban_url => $base . '?__mode=save&_type=banlist&blog_id='
                                 . $blog->id . '&ip=' . $comment->ip,
                     comment_ip => $comment->ip,
                     comment_name => $comment->author,
                     (is_valid_email($comment->email)?
                      (comment_email => $comment->email):()),
                     comment_url => $comment->url,
                     comment_text => $comment->text,
                     unapproved => !$comment->visible(),
                    );
        my $body = MT->build_email('new-comment.tmpl', \%param);
        MT::Mail->send(\%head, $body)
            or return $app->handle_error(MT::Mail->errstr());
    }
}

sub preview { my $app = shift; do_preview($app, $app->{query}, @_) }

sub _make_commenter {
    my $app = shift;
    my %params = @_;
    require MT::Author;
    my $cmntr = MT::Author->load({ name => $params{name},
                                   type => MT::Author::COMMENTER });
    if (!$cmntr) {
        $cmntr = MT::Author->new();
        $cmntr->set_values({email => $params{email},
                            name => $params{name},
                            nickname => $params{nickname},
                            password => "(none)",
                            type => MT::Author::COMMENTER,
                            url => $params{url},
                            });
        $cmntr->save();
    } else {
        $cmntr->set_values({email => $params{email},
                            nickname => $params{nickname},
                            password => "(none)",
                            type => MT::Author::COMMENTER,
                            url => $params{url},
                            });
        $cmntr->save();
    }
    return $cmntr;
}

sub _expire_sessions {
    my ($timeout) = @_;

    require MT::Session;
    my @old_sessions = MT::Session->load({start => 
                                              [0, time() - $timeout]},
                                         {range => {start => 1}});
    foreach (@old_sessions) {
        $_->remove() || die "couldn't remove sessions because "
            . $_->errstr();
    }
}

sub _make_commenter_session {
    my $app = shift;
    my ($session_key, $email, $name, $nick) = @_;
    my $enc = $app->{cfg}->PublishCharset || '';
    $nick = MT::I18N::encode_text($nick, $enc, 'utf-8');

    my %kookee = (-name => $COMMENTER_COOKIE_NAME,
                  -value => $session_key,
                  -path => '/',
                  -expires => '+1h');
    $app->bake_cookie(%kookee);
    my %name_kookee = (-name => "commenter_name",
                       -value => $nick,
                       -path => '/',
                       -expires => '+1h');
    $app->bake_cookie(%name_kookee);

    require MT::Session;
    my $sess_obj = MT::Session->new();
    $sess_obj->id($session_key);
    $sess_obj->email($email);
    $sess_obj->name($name);
    $sess_obj->start(time);
    $sess_obj->kind("SI");
    $sess_obj->save()
        or return $app->error("The login could not be confirmed because of a database error (" . $sess_obj->errstr() . ")");
    return $session_key;
}

my $SIG_WINDOW = 60 * 10;  # ten minute handoff between TP and MT

sub _validate_signature {
    my $app = shift;
    my ($sig_str, %params) = @_;

    # the DSA sig parameter is composed of the two pieces of the
    # real DSA sig, packed in Base64, separated by a colon.

#    my ($r, $s) = split /:/, decode_url($sig_str);
    my ($r, $s) = split /:/, $sig_str;
    $r =~ s/ /+/g;
    $s =~ s/ /+/g;

    $params{email} =~ s/ /+/g;
    require MIME::Base64;
    import MIME::Base64 qw(decode_base64);
    use MT::Util qw(bin2dec);
    $r = bin2dec(decode_base64($r));
    $s = bin2dec(decode_base64($s));

    my $sig = {'s' => $s,
               'r' => $r};
    my $timer = time;
    require MT::Util; import MT::Util ('dsa_verify');
    my $msg;
    if ($app->{cfg}->TypeKeyVersion eq '1.1') {
        $msg = ($params{email} . "::" . $params{name} . "::" .
                $params{nick} . "::" . $params{ts} . "::" . $params{token});
    } else {
        $msg = ($params{email} . "::" . $params{name} . "::" .
                $params{nick} . "::" . $params{ts});
    }

    my $dsa_key;
    require MT::Session;
    $dsa_key = eval { MT::Session->load({id => 'KY',
                                         kind => 'KY'}); } || undef; 
    if ($dsa_key) {
        if ($dsa_key->start() < time - 24 * 60 * 60) {
            $dsa_key = undef;
        }
        $dsa_key = $dsa_key->data if $dsa_key;
    }
    if ( ! $dsa_key ) {
        # Load the override key
        $dsa_key = $app->{cfg}->get('SignOnPublicKey');
    }
    # Load the DSA key from the RegKeyURL
    my $key_location = $app->{cfg}->RegKeyURL;
    if (!$dsa_key && $key_location) {
        require LWP::UserAgent;
        my $ua = new LWP::UserAgent(timeout => 15);
        my $req = new HTTP::Request(GET => $key_location);
        my $resp = $ua->request($req);
        return $app->error("Couldn't get public key from url provided")
            unless $resp->is_success();
        # TBD: Check the content-type
        $dsa_key = $resp->content();

        require MT::Session;
        my $key_cache = new MT::Session();

        my @chs = ('a' .. 'z', '0' .. '9');
        $key_cache->set_values({id => 'KY',
                                data => $dsa_key,
                                kind => 'KY',
                                start => time});
        $key_cache->save();
    }
    if (!$dsa_key) {
        return $app->error($app->translate(
                    "No public key could be found to validate registration."));
    }
    my ($p) = $dsa_key =~ /p=([0-9a-f]*)/i;
    my ($q) = $dsa_key =~ /q=([0-9a-f]*)/i;
    my ($g) = $dsa_key =~ /g=([0-9a-f]*)/i;
    my ($pub_key) = $dsa_key =~ /pub_key=([0-9a-f]*)/i;
    $dsa_key = {p=>$p, q=>$q, g=>$g, pub_key=>$pub_key};
    my $valid = dsa_verify(Key => $dsa_key,
                           Signature => $sig,
                           Message => $msg);
    $timer = time - $timer;

    MT::log("TypeKey signature verif'n returned "
            . ($valid ? "VALID" : "INVALID") . " in "
            . $timer. " seconds "
            . "verifying [$msg] with [$sig_str]\n")
        unless $valid;

    return ($valid && $params{ts} + $SIG_WINDOW >= time);
}

sub _handle_sign_in {
    my $app = shift;
    my $q = $app->{query};
    my ($weblog) = @_;

    if ($q->param('logout')) {
        my %cookies = $app->cookies();

        my $cookie_val = ($cookies{$COMMENTER_COOKIE_NAME}
                          ? $cookies{$COMMENTER_COOKIE_NAME}->value()
                          : "");
        #my ($email, $session) = split(/::/, $cookie_val) if $cookie_val;
        my $session = $cookie_val;
        require MT::Session;
        my $sess_obj = MT::Session->load({id => $session });
        $sess_obj->remove() if ($sess_obj);
        
        my %kookee = (-name => $COMMENTER_COOKIE_NAME,
                      -value => '',
                      -path => '/',
                      -expires => '+1h');
        $app->bake_cookie(%kookee);
        my %name_kookee = (-name => 'commenter_name',
                           -value => '',
                           -path => '/',
                           -expires => '+1h');
        $app->bake_cookie(%name_kookee);
        return 1;
    } elsif ($q->param('sig')) {
        my $session = undef;
        my ($email, $name, $nick);
        my $ts = $q->param('ts') || "";
        $email = $q->param('email') || "";
        $name = $q->param('name') || "";
        $nick = $q->param('nick') || "";
        my $sig_str = $q->param('sig');
        my $cmntr;
        if ($sig_str) {
            if (!$app->_validate_signature($sig_str, 
                                           token => $weblog->effective_remote_auth_token,
                                           email => decode_url($email),
                                           name => decode_url($name),
                                           nick => decode_url($nick),
                                           ts => $ts))
            {
                # Signature didn't match, or timestamp was out of date.
                # This implies tampering, not a user mistake.
                return $app->error("The validation failed.");
            }
            
            if ($weblog->require_comment_emails && !is_valid_email($email)) {
                return $app->error("This weblog requires commenters to pass an email address. If you'd like to do so you may log in again, and give the authentication service permission to pass your email address.");
            }

            # Signature was valid, so create a session, etc.
            my $enc = $app->{cfg}->PublishCharset || '';
            $nick = MT::I18N::encode_text($nick, 'utf-8', $enc);
            $session = $app->_make_commenter_session($sig_str, $email,
                                                     $name, $nick)
                || return $app->error($app->errstr()
                                      || "Couldn't save the session");
            $cmntr = $app->_make_commenter(email => $email,
                                           nickname => $nick,
                                           name => $name);
        } else {
            # If there's no signature, then we trust the cookie.
            my %cookies = $app->cookies();
            if ($cookies{$COMMENTER_COOKIE_NAME}
                && ($session = $cookies{$COMMENTER_COOKIE_NAME}->value())) 
            {
                require MT::Session; require MT::Author;
                my $sess = MT::Session->load({id => $session});
                $cmntr = MT::Author->load({name => $sess->name,
                                           type => MT::Author::COMMENTER});
                if ($weblog->require_comment_emails
                    && !is_valid_email($cmntr->email))
                {
                    return $app->error("This weblog requires commenters to pass an email address");
                }
            } else {
            }
        }
        if ($q->param('sig') && !$cmntr) {
            return $app->handle_error($app->errstr());
        }
        return $cmntr;
    }
}

# This actually handles a UI-level sign-in or sign-out request.
sub handle_sign_in {
    my $app = shift;
    my $q = $app->{query};

    my $entry = MT::Entry->load($q->param('entry_id'));
    my $weblog = MT::Blog->load($q->param('blog_id') || $entry->blog_id);

    return $app->handle_error($app->translate("Sign in requires a secure signature; logout requires the logout=1 parameter")) 
        unless ($q->param('sig') || $q->param('logout'));
    
    $app->_handle_sign_in($weblog)
        || return $app->handle_error($app->errstr() || 
                  $app->translate("The sign-in attempt was not successful; please try again."), 403);

    my $target;
    if ($q->param('static')) {
        if ($q->param('static') eq 1) {
            require MT::Entry;
            my $entry = MT::Entry->load($q->param('entry_id'));
            $target = $entry->archive_url;
        } else {
            $target = $q->param('static');
        }
    } else {
        $target = ($app->{cfg}->CGIPath . $app->{cfg}->CommentScript
                   . "?entry_id=" . $entry->id
                   . ($q->param('arch') ? '&static=0&arch=1' : ''));
    } 
    require MT::Util;
    if ($q->param('logout')) {
        return $app->redirect($app->{cfg}->SignOffURL . "&_return=" .
                              MT::Util::encode_url($target),
                              UseMeta => 1);
    } else {
        return $app->redirect($target, UseMeta => 1);
    }
}

sub commenter_name_js {
    local $SIG{__WARN__} = sub {};
    my $app = shift;
    my $commenter_name = $app->cookie_val('commenter_name');
    $commenter_name = MT::I18N::encode_text($commenter_name,'utf-8',undef);

    return "var commenter_name = '$commenter_name';\n";
}

sub view {
    my $app = shift;
    my $q = $app->{query};
    my %param = $app->param_hash();
    my %overrides = ref($_[0]) ? %{$_[0]} : ();
    @param{keys %overrides} = values %overrides;

    my $cmntr;
    my $session_key;

    my $weblog = MT::Blog->load($q->param('blog_id'));

    if ($q->param('logout')) {
        return $app->handle_sign_in($weblog);
    }

    if ($q->param('sig')) {
        $cmntr = $app->_handle_sign_in($weblog)
            || return $app->handle_error($app->translate(
                 "The sign-in validation was not successful. Please make sure your weblog is properly configured and try again."));
        $cmntr = undef if $cmntr == 1;   # 1 is returned on logout.
    } else {
        ($session_key, $cmntr) = $app->_get_commenter_session();
    }

    require MT::Template;
    require MT::Template::Context;

    require MT::Entry;
    my $entry_id = $q->param('entry_id')
        or return $app->error("No entry_id");
    my $entry = MT::Entry->load($entry_id)
        or return $app->error($app->translate(
            "No such entry ID '[_1]'", $entry_id));
    return $app->error($app->translate(
            "No such entry ID '[_1]'", $entry_id))
        if $entry->status != RELEASE;

    require MT::Blog;
    my $blog = MT::Blog->load($entry->blog_id);
    require Data::Dumper;
    if ($cmntr) {
        if (!$blog->manual_approve_commenters &&
            ($cmntr->status($entry->blog_id) == PENDING))
        {
            $cmntr->approve($entry->blog_id);
        }
    }

    my $ctx = MT::Template::Context->new;
    $ctx->stash('entry', $entry);
    $ctx->stash('commenter', $cmntr) if ($cmntr);
    $ctx->{current_timestamp} = $entry->created_on;
    my %cond = (
        EntryIfExtended => $entry->text_more ? 1 : 0,
        EntryIfAllowComments => $entry->allow_comments,
        EntryIfCommentsOpen => $entry->allow_comments eq '1',
        EntryIfAllowPings => $entry->allow_pings,
        IfAllowCommentHTML => $blog->allow_comment_html,
        IfRegistrationRequired => !$blog->allow_unreg_comments(),
        IfCommentsAllowed => $blog->allow_reg_comments
                               || $blog->allow_unreg_comments,
        IfDynamicCommentsStaticPage => 0,
        IfDynamicComments => MT::ConfigMgr->instance()->DynamicComments,
                # We suppress IfDynamicComments because we are already 
                # AT the dynamic comment page; a bit of a hack
        IfCommenterPending => $cmntr && ($cmntr->status($blog->id) == PENDING),
        IfNeedEmail => $blog->require_comment_emails,
    );
    my $tmpl = ($q->param('arch')) ?
        (MT::Template->load({ type => 'individual',
                                        blog_id => $entry->blog_id })
            or return $app->error($app->translate(
                 "You must define an Individual template in order to " .
                 "display dynamic comments.")))
    :
        (MT::Template->load({ type => 'comments',
                                        blog_id => $entry->blog_id })
            or return $app->error($app->translate(
                 "You must define a Comment Listing template in order to " .
                                                  "display dynamic comments.")));

    my $html = $tmpl->build($ctx, \%cond);
    $html = MT::Util::encode_html($tmpl->errstr) unless defined $html;
    $html;
}

sub handle_error {
    my $app = shift;
    my($err, $status_line) = @_;
    my $html = do_preview($app, $app->{query}, $err)
        || return "An error occurred: " . $err;
    $app->{status_line} = $status_line;
    $html;
}

sub do_preview {
    my($app, $q, $err) = @_;
    require MT::Template;
    require MT::Template::Context;
    require MT::Entry;
    require MT::Util;
    require MT::Comment;
    my $entry_id = $q->param('entry_id') 
        || return $app->error($app->translate('No entry was specified; perhaps there is a template problem?'));
    my $entry = MT::Entry->load($entry_id)
        || return $app->error($app->translate("Somehow, the entry you tried to comment on does not exist"));
    my $ctx = MT::Template::Context->new;

    my ($comment, $commenter) = $app->_make_comment($entry);
    return "An error occurred: " . $app->errstr() unless $comment;

    ## Set timestamp as we would usually do in ObjectDriver.
    my @ts = MT::Util::offset_time_list(time, $entry->blog_id);
    my $ts = sprintf "%04d%02d%02d%02d%02d%02d",
        $ts[5]+1900, $ts[4]+1, @ts[3,2,1,0];
    $comment->created_on($ts);
    $ctx->stash('comment_preview', $comment);

    unless ($err) {
        ## Serialize comment state, then hex-encode it.
        require MT::Serialize;
        my $ser = MT::Serialize->new($app->{cfg}->Serializer);
        my $state = $comment->column_values;
        $state->{static} = $q->param('static');
        $ctx->stash('comment_state', unpack 'H*', $ser->serialize(\$state));
    }
    $ctx->stash('comment_is_static', $q->param('static'));
    $ctx->stash('entry', $entry);
    $ctx->{current_timestamp} = $ts;
    $ctx->stash('commenter', $commenter);
    my($tmpl);
    $err ||= '';
    if ($err eq 'pending') {
        $tmpl = MT::Template->load({ type => 'comment_pending',
                                     blog_id => $entry->blog_id })
        or return $app->error($app->translate(
            "You must define a Comment Pending template."));
    } elsif ($err) {
        $ctx->stash('error_message', $err);
        $tmpl = MT::Template->load({ type => 'comment_error',
                                     blog_id => $entry->blog_id })
        or return $app->error($app->translate(
            "You must define a Comment Error template."));
    } else {
        $tmpl = MT::Template->load({ type => 'comment_preview',
                                     blog_id => $entry->blog_id })
        or return $app->error($app->translate(
            "You must define a Comment Preview template."));
    }
    require MT::Blog;
    my $blog = MT::Blog->load($entry->blog_id);
    my %cond = (IfAllowCommentHTML => $blog->allow_comment_html,
                IfRegistrationRequired => !$blog->allow_unreg_comments,
                IfCommentsAllowed => $blog->allow_reg_comments
                                       || $blog->allow_unreg_comments,
                IfNeedEmail => $blog->require_comment_emails);
    my $html = $tmpl->build($ctx, \%cond);
    $html = $tmpl->errstr unless defined $html;
    $html;
}

1;
__END__

=head1 NAME

MT::App::Comments

=head1 SYNOPSIS

The application-level callbacks of the C<MT::App::Comments> application
are documented here.

=head1 CALLBACKS

=over 4

=item CommentThrottleFilter

Called as soon as a new comment has been received. The callback must
return a boolean value. If the return value is false, the incoming
comment data will be discarded and the app will output an error page
about throttling. A CommentThrottleFilter callback has the following
signature:

    sub comment_throttle_filter($eh, $app, $entry)
    {
        ...
    }

I<$app> is the C<MT::App::Comments> object, whose interface is documented
in L<MT::App::Comments>, and I<$entry> is the entry on which the
comment is to be placed.

Note that no comment object is passed, because it has not yet been
built. As such, this callback can be used to tell the application to
exit early from a comment attempt, before much processing takes place.

When more than one CommentThrottleFilter is installed, the data is
discarded unless all callbacks return true.

=item CommentFilter

Called once the comment object has been constructed, but before saving
it. If any CommentFilter callback returns false, the comment will not
be saved. The callback has the following signature:

    sub comment_filter($eh, $app, $comment)
    {
        ...
    }

=back
