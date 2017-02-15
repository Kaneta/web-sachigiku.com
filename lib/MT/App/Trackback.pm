# Copyright 2001-2004 Six Apart. This code cannot be redistributed without
# permission from www.movabletype.org.
#
# $Id: Trackback.pm,v 1.42 2004/10/01 18:26:04 ezra Exp $

package MT::App::Trackback;
use strict;

use File::Spec;
use MT::ConfigMgr;
use MT::TBPing;
use MT::Trackback;
use MT::Util qw( first_n_words encode_xml is_valid_url start_background_task );
use MT::App;
use MT::I18N;
@MT::App::Trackback::ISA = qw( MT::App );

sub init {
    my $app = shift;
    $app->SUPER::init(@_) or return;
    $app->add_methods(
        ping => \&ping,
        view => \&view,
        rss => \&rss,
    );
    $app->{default_mode} = 'ping';
    $app->{charset} = $app->{cfg}->PublishCharset;
    $app;
}

sub view {
    my $app = shift;
    my $q = $app->{query};
    require MT::Template;
    require MT::Template::Context;
    require MT::Entry;
    my $entry_id = $q->param('entry_id');
    my $entry = MT::Entry->load($entry_id)
        or return $app->error($app->translate(
            "Invalid entry ID '[_1]'", $entry_id));
    my $ctx = MT::Template::Context->new;
    $ctx->stash('entry', $entry);
    $ctx->{current_timestamp} = $entry->created_on;
    my $tmpl = MT::Template->load({ type => 'pings',
                                    blog_id => $entry->blog_id })
        or return $app->error($app->translate(
            "You must define a Ping template in order to display pings."));
    defined(my $html = $tmpl->build($ctx))
        or return $app->error($tmpl->errstr);
    $html;
}

## The following subroutine strips the UTF8 flag from a string, thus
## forcing it into a series of bytes. "pack 'C0'" is a magic way of
## forcing the following string to be packed as bytes, not as UTF8.
sub no_utf8 {
    for (@_) {
        next if !defined $_;
        $_ = pack 'C0A*', $_;
    }
}

my %map = ('&' => '&amp;', '"' => '&quot;', '<' => '&lt;', '>' => '&gt;');
sub _response {
    my $app = shift;
    my %param = @_;
    $app->response_code($param{Code});
    $app->send_http_header('text/xml');
    $app->{no_print_body} = 1;

    if (my $err = $param{Error}) {
        my $re = join '|', keys %map;
        $err =~ s!($re)!$map{$1}!g;
	$err = MT::I18N::encode_text($err,undef,'utf-8');
        print <<XML;
<?xml version="1.0" encoding="UTF-8"?>
<response>
<error>1</error>
<message>$err</message>
</response>
XML
    } else {
        print <<XML;
<?xml version="1.0" encoding="UTF-8"?>
<response>
<error>0</error>
XML
        if (my $rss = $param{RSS}) {
	    $rss = MT::I18N::encode_text($rss,undef,'utf-8');
            print $rss;
        }
        print <<XML;
</response>
XML
    }

    1;
}

sub _get_params {
    my $app = shift;
    my($tb_id, $pass);
    if ($tb_id = $app->{query}->param('tb_id')) {
        $pass = $app->{query}->param('pass');
    } else {
        if (my $pi = $app->path_info) {
            $pi =~ s!^/!!;
            $pi =~ s!^\D*!!;
            ($tb_id, $pass) = split /\//, $pi;
        }
    }
    ($tb_id, $pass);
}

sub _builtin_throttle {
    my ($eh, $app, $tb) = @_;
    my $user_ip = $app->remote_ip;
    use MT::Util qw(offset_time_list);
    my @ts = offset_time_list(time - 3600,
			      $tb->blog_id);
    my $from = sprintf("%04d%02d%02d%02d%02d%02d",
		       $ts[5]+1900, $ts[4]+1, @ts[3,2,1,0]);
    require MT::TBPing;
    if ($app->{cfg}->OneHourMaxPings
          <= MT::TBPing->count({ blog_id => $tb->blog_id,
                                 created_on => [$from] },
                               {range => {created_on => 1} }))
    {
	return 0;
    }

    @ts = offset_time_list(time - $app->{cfg}->ThrottleSeconds*4000 - 1,
                           $tb->blog_id);
    $from = sprintf("%04d%02d%02d%02d%02d%02d",
                    $ts[5]+1900, $ts[4]+1, @ts[3,2,1,0]);
    my $count = MT::TBPing->count({ blog_id => $tb->blog_id,
				    created_on => [$from] },
				  {range => {created_on => 1} });
    if ($count >= $app->{cfg}->OneDayMaxPings) {
        return 0;
# 	require MT::IPBanList;
# 	my $ipban = MT::IPBanList->new();
# 	$ipban->set_values({blog_id => $tb->blog_id,
# 			    ip => $user_ip});
# 	$ipban->save();
# 	start_background_task(sub {
#             $app->log("IP $user_ip banned because TrackBack ping rate " .
#                       "exceeded 8 in " .
#                       10 * $app->{cfg}->ThrottleSeconds . " seconds.");
#             require MT::Mail;
#             if ($tb->entry_id) {
#                 my $entry = MT::Entry->load($tb->entry_id);
#                 my $author = MT::Author->load($entry->author_id);
#                 $app->set_language($author->preferred_language)
#                     if $author && $author->preferred_language;
#                
#                 my $blog = MT::Blog->load($entry->blog_id);
#                 if ($author && $author->email) {
#                     my %head = ( To => $author->email || "",
#                                  From => $app->{cfg}->EmailAddressMain
#                                  || $author->email || "",
#                                  Subject =>
#                                  '[' . $blog->name . '] ' .
#                                  $app->translate("IP Banned Due to Excessive TrackBack Pings"));
#                     my $charset = $app->{cfg}->PublishCharset || 'iso-8859-1';
#                     $head{'Content-Type'} = qq(text/plain; charset="$charset");
#                     my $body = $app->translate('Another weblog [_1] has automatically been banned by posting more than the allowed number of TrackBack pings in the last [_2] seconds. This has been done to prevent a malicious script from overwhelming your weblog with pings. The banned IP address is
#
#     [_3]
#
# If this was a mistake, you can unblock the IP address and allow the weblog to ping again by logging in to your Movable Type installation, going to Weblog Config - IP Banning, and deleting the IP address [_4] from the list of banned addresses.', $blog->name, 10 * $app->{cfg}->ThrottleSeconds, $user_ip, $user_ip);
#                     require Text::Wrap;
#                     $Text::Wrap::cols = 72;
#                     $body = Text::Wrap::wrap('', '', $body);
#                     MT::Mail->send(\%head, $body);
#                 }
#             }
#         });
# 	return 0;
    }
    return 1;
}

sub ping {
    my $app = shift;
    my $q = $app->{query};

    return $app->_response("Trackback pings must use HTTP POST")
        if $app->request_method() ne 'POST';

    my($tb_id, $pass) = $app->_get_params;
    return $app->_response(Error =>
           $app->translate("Need a TrackBack ID (tb_id)."))
        unless $tb_id;

    require MT::Trackback;
    my $tb = MT::Trackback->load($tb_id)
        or return $app->_response(Error =>
            $app->translate("Invalid TrackBack ID '[_1]'", $tb_id));

    my $user_ip = $app->remote_ip;

    ## Check if this user has been banned from sending TrackBack pings.
    require MT::IPBanList;
    my $iter = MT::IPBanList->load_iter({ blog_id => $tb->blog_id });
    while (my $ban = $iter->()) {
        my $banned_ip = $ban->ip;
        if ($user_ip =~ /$banned_ip/) {
            return $app->_response(Error =>
              $app->translate("You are not allowed to send TrackBack pings."));
        }
    }

    MT->add_callback('TBPingThrottleFilter', 1, undef,
		     \&MT::App::Trackback::_builtin_throttle);

    my $passed_filter = MT->run_callbacks('TBPingThrottleFilter',
					  $app, $tb);
    if (!$passed_filter) {
	return $app->_response(Error => $app->translate("You are pinging trackbacks too quickly. Please try again later."), Code => "403 Throttled");
    }

    my($title, $excerpt, $url, $blog_name, $enc) = map scalar $q->param($_),
                                             qw( title excerpt url blog_name charset);

    no_utf8($tb_id, $title, $excerpt, $url, $blog_name);
    # guess encoding as possible
    $enc = MT::I18N::guess_encoding($excerpt.$title.$blog_name) unless $enc;
    ($title, $excerpt, $blog_name) = map {MT::I18N::encode_text($_,$enc,undef)} ($title, $excerpt, $blog_name);

    return $app->_response(Error=> $app->translate("Need a Source URL (url)."))
        unless $url;

    if (my $fixed = MT::Util::is_valid_url($url || "")) {
        $url = $fixed; 
    } else {
        return $app->_response(Error =>
            $app->translate("Invalid URL '[_1]'", $url));
    }

    require MT::TBPing;

    return $app->_response(Error =>
        $app->translate("This TrackBack item is disabled."))
        if $tb->is_disabled;

    if ($tb->passphrase && (!$pass || $pass ne $tb->passphrase)) {
        return $app->_response(Error =>
          $app->translate("This TrackBack item is protected by a passphrase."));
    }

    my $ping = MT::TBPing->new;
    $ping->blog_id($tb->blog_id);
    $ping->tb_id($tb_id);
    $ping->source_url($url);
    $ping->ip($app->remote_ip || '');
    if ($excerpt) {
        if ($app->{cfg}->DefaultLanguage eq 'ja') {
            if (MT::I18N::length_text($excerpt) > 80) {
                $excerpt = MT::I18N::substr_text($excerpt,0,80) . '...';
            }
        } else {
            if (length($excerpt) > 255) {
                $excerpt = substr($excerpt, 0, 252) . '...';
            }
        }
        if ($app->{cfg}->DefaultLanguage eq 'ja') {
            $title = MT::I18N::first_n_text($excerpt, 10)
                unless defined $title;
        } else {
            $title = first_n_words($excerpt, 5)
                unless defined $title;
        }
        $ping->excerpt($excerpt);
    }
    $ping->title(defined $title && $title ne '' ? $title : $url);
    $ping->blog_name($blog_name);
    if (!MT->run_callbacks('TBPingFilter', $app, $ping)) {
        return $app->_response(Error => "", Code => 403);
    }

    $ping->save;

    require MT::Blog;
    my $blog = MT::Blog->load($ping->blog_id);
    $blog->touch; $blog->save;

    start_background_task(sub {
    ## If this is a trackback item for a particular entry, we need to
    ## rebuild the indexes in case the <$MTEntryTrackbackCount$> tag
    ## is being used. We also want to place the RSS files inside of the
    ## Local Site Path.
    my($blog_id, $entry, $cat);
    if ($tb->entry_id) {
        require MT::Entry;
        $entry = MT::Entry->load($tb->entry_id);
        $blog_id = $entry->blog_id;
    } elsif ($tb->category_id) {
        require MT::Category;
        $cat = MT::Category->load($tb->category_id);
        $blog_id = $cat->blog_id;
    }
    $app->rebuild_indexes( Blog => $blog )
        or return $app->_response(Error =>
            $app->translate("Rebuild failed: [_1]", $app->errstr));

    if ($tb->entry_id) {
	$app->rebuild_entry(Entry => $entry, Blog => $blog,
			    BuildDependencies => 1);
    }
    if ($tb->category_id) { 
	$app->_rebuild_entry_archive_type(
		Entry => undef, Blog => $blog,
		Category => $cat, ArchiveType => 'Category'
	);
    }

    if ($app->{cfg}->GenerateTrackBackRSS) {
        ## Now generate RSS feed for this trackback item.
        my $rss = _generate_rss($tb, 10);
        my $base = $blog->archive_path;
        my $feed = File::Spec->catfile($base, $tb->rss_file || $tb->id . '.xml');
        my $fmgr = $blog->file_mgr;
        $fmgr->put_data($rss, $feed)
            or return $app->_response(Error =>
                $app->translate("Can't create RSS feed '[_1]': ", $feed,
                $fmgr->errstr));
    }

    if ($blog->email_new_pings) {
        $app->_send_ping_notification($blog, $entry, $cat, $ping);
    }
 });

    return $app->_response;
}

# one of $entry or $cat must be passed.
sub _send_ping_notification {
    my $app = shift;
    my ($blog, $entry, $cat, $ping) = @_;
    
    require MT::Mail;
    my($author, $subj, $body);
    if ($entry) {
        $author = $entry->author;
        $app->set_language($author->preferred_language)
            if $author && $author->preferred_language;
        $subj = $app->translate('New TrackBack Ping to Entry [_1] ([_2])',
                                $entry->id, $entry->title);
        $body = $app->translate('A new TrackBack ping has been sent to your weblog, on the entry [_1] ([_2]).', $entry->id, $entry->title);
    } elsif ($cat) {
        require MT::Author;
        $author = MT::Author->load($cat->created_by);
        $app->set_language($author->preferred_language)
            if $author && $author->preferred_language;
        $subj = $app->translate('New TrackBack Ping to Category [_1] ([_2])',
                                $cat->id, $cat->label);
        $body = $app->translate('A new TrackBack ping has been sent to your weblog, on the category [_1] ([_2]).', $cat->id, $cat->label);
    }
    if ($author && $author->email) {
        my %head = ( To => $author->email,
                     From => $app->{cfg}->EmailAddressMain || 
                     $author->email || "",
                     Subject => '[' . $blog->name . '] ' . $subj );
        my $charset = $app->{cfg}->PublishCharset || 'iso-8859-1';
        $head{'Content-Type'} = qq(text/plain; charset="$charset");
        $body = MT::I18N::wrap_text($body,72) . "\n\n" .
            $app->translate('IP Address:') . ' ' . $ping->ip . "\n" .
            $app->translate('URL:') . ' <' . $ping->source_url . ">\n" .
            $app->translate('Title:') . ' ' . $ping->title . "\n" .
            $app->translate('Weblog:') . ' ' . $ping->blog_name . "\n\n" .
            $app->translate('Excerpt:') . "\n" . $ping->excerpt . "\n";
        MT::Mail->send(\%head, $body);
    }
}

sub rss {
    my $app = shift;
    my($tb_id, $pass) = $app->_get_params;
    my $tb = MT::Trackback->load($tb_id)
        or return $app->_response(Error =>
            $app->translate("Invalid TrackBack ID '[_1]'", $tb_id));
    my $rss = _generate_rss($tb);
    $app->_response(RSS => $rss);
}

sub _generate_rss {
    my($tb, $lastn) = @_;
    my $lang = MT::ConfigMgr->instance()->DefaultLanguage || 'en-us';
    my $rss = <<RSS;
<rss version="0.91"><channel>
<title>@{[ $tb->title ]}</title>
<link>@{[ $tb->url || '' ]}</link>
<description>@{[ $tb->description || '' ]}</description>
<language>$lang</language>
RSS
    my %arg;
    if ($lastn) {
        %arg = ('sort' => 'created_on', direction => 'descend',
                limit => $lastn);
    }
    my $iter = MT::TBPing->load_iter({ tb_id => $tb->id }, \%arg);
    while (my $ping = $iter->()) {
        $rss .= sprintf qq(<item>\n<title>%s</title>\n<link>%s</link>\n),
            encode_xml($ping->title), encode_xml($ping->source_url);
        if ($ping->excerpt) {
            $rss .= sprintf qq(<description>%s</description>\n),
                encode_xml($ping->excerpt);
        }
        $rss .= qq(</item>\n);
    }
    $rss .= qq(</channel>\n</rss>);
    my $enc = MT::ConfigMgr->instance()->PublishCharset || 'UTF-8';
    $rss = MT::I18N::encode_text($rss,$enc,'utf-8');
    $rss;
}

1;
