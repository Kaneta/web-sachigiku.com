# A plugin for filtering Comment and TBPing Spams
#
# Release 0.20 (Apr 8, 2005)
#
# This software is provided as-is. You may use it for commercial or 
# personal use. If you distribute it, please keep this notice intact.
#
# Copyright (c) 2005 Hirotaka Ogawa

package MT::Plugin::Quasi_SpamFilter;
use strict;
use vars qw($COMMENT_PATTERN $COMMENT_METHOD
	    $TBPING_PATTERN $TBPING_METHOD
	    $ENABLE_LOGGING
	    $URL %comment_methods %tbping_methods);

# Set your spam pattern
$COMMENT_PATTERN = '<h1>|<a\s'; # H1 or A elements
$TBPING_PATTERN = '<h1>|<a\s'; # H1 or A elements

# Choose a method for rejecting Spam Comments from: 
# 'CommentFilter', 'CommentThrottleFilter', 'CommentError',
# 'CommentLongError', 'CommentRedirect', 'CommentEvilRedirect'
$COMMENT_METHOD = 'CommentError';

# Choose a method for rejecting Spam Pings from:
# 'TBPingFilter', 'TBPingThrottleFilter', 'TBPingError'
$TBPING_METHOD = 'TBPingError';

# Set your Redirect URL (for 'CommentRedirect' and 'CommentEvilRedirect')
$URL = 'http://www.google.co.jp/';

# Enable logging? (1/0)
$ENABLE_LOGGING = 1;

eval("use Storable;");
if (!$@ && MT->can('add_plugin')) {
    require MT::Plugin;
    my $plugin = new MT::Plugin();
    $plugin->name("Quasi Spam Filter Plugin 0.20");
    $plugin->description("A Simple filter for Comment &amp; TBPing Spams");
    $plugin->doc_link("http://as-is.net/hacks/2005/01/quasi_spam_filter_plugin.html");
    MT->add_plugin($plugin);
}

%comment_methods = (
    'CommentFilter' => 'comment_filter',
    'CommentThrottleFilter' => 'comment_throttle_filter',
    'CommentError' => 'comment_error',
    'CommentLongError' => 'comment_long_error',
    'CommentRedirect' => 'comment_redirect',
    'CommentEvilRedirect' => 'comment_evil_redirect'
);

%tbping_methods = (
    'TBPingFilter' => 'tbping_filter',
    'TBPingThrottleFilter' => 'tbping_throttle_filter',
    'TBPingError' => 'tbping_error'
);

if (defined(my $method = $comment_methods{$COMMENT_METHOD})) {
    if ($COMMENT_METHOD =~ /Filter$/ && MT->can('add_callback')) {
	MT->add_callback($COMMENT_METHOD, 10, 'Reject Spam Comments', \&$method);
    } else {
	*MT::App::Comments::pre_run = \&$method;
    }
}

if (defined(my $method = $tbping_methods{$TBPING_METHOD})) {
    if ($TBPING_METHOD =~ /Filter$/ && MT->can('add_callback')) {
	MT->add_callback($TBPING_METHOD, 10, 'Reject Spam TBPings', \&$method);
    } else {
	*MT::App::Trackback::pre_run = \&$method;
    }
}

use MT::Comment;
use MT::TBPing;

sub is_comment_spam {
    my $comment = shift;
    return ($comment->text =~ /$COMMENT_PATTERN/i);
}

sub is_tbping_spam {
    my $tbping = shift;
    return ($tbping->excerpt =~ /$TBPING_PATTERN/i);
}

sub _make_pseudo_comment {
    my $app = shift;
    my $q = $app->{query};
    my $comment = MT::Comment->new;
    $comment->author($q->param('author') || '');
    $comment->email($q->param('email') || '');
    $comment->url($q->param('url') || '');
    $comment->text($q->param('text') || '');
    $comment->ip($app->remote_ip || '');
    return $comment;
}

sub _make_pseudo_tbping {
    my $app = shift;
    my $q = $app->{query};
    my $tbping = MT::TBPing->new;
    $tbping->title($q->param('title') || '');
    $tbping->excerpt($q->param('excerpt') || '');
    $tbping->source_url($q->param('url') || '');
    $tbping->blog_name($q->param('blog_name') || '');
    $tbping->ip($app->remote_ip || '');
    return $tbping;
}

sub comment_filter {
    my ($eh, $app, $comment) = @_;
    if (is_comment_spam($comment)) {
	$app->log("[QSF] drop a spam comment from " . $comment->author) if $ENABLE_LOGGING;
	return 0;
    }
    return 1;
}

sub comment_throttle_filter {
    my ($eh, $app, $entry) = @_;
    my $comment = _make_pseudo_comment($app);
    if (is_comment_spam($comment)) {
	$app->log("[QSF] drop a spam comment from " . $comment->author) if $ENABLE_LOGGING;
	return 0;
    }
    return 1;
}

sub comment_error {
    my $app = shift;
    my $q = $app->{query};
    my $mode = $q->param('__mode') || $app->{default_mode};
    return if $mode ne 'post';
    my $comment = _make_pseudo_comment($app);
    if (is_comment_spam($comment)) {
	$app->add_methods(post => sub { });
	$app->error("Spam Comment!");
	$app->log("[QSF] drop a spam comment from " . $comment->author) if $ENABLE_LOGGING;
    }
}

sub comment_long_error {
    my $app = shift;
    my $q = $app->{query};
    my $mode = $q->param('__mode') || $app->{default_mode};
    return if $mode ne 'post';
    my $comment = _make_pseudo_comment($app);
    if (is_comment_spam($comment)) {
	$app->add_methods(post => sub { $_[0]->handle_error("Spam Comments!") });
	$app->log("[QSF] drop a spam comment from " . $comment->author) if $ENABLE_LOGGING;
    }
}

sub comment_redirect {
    my $app = shift;
    my $q = $app->{query};
    my $mode = $q->param('__mode') || $app->{default_mode};
    return if $mode ne 'post';
    my $comment = _make_pseudo_comment($app);
    if (is_comment_spam($comment)) {
	$app->add_methods(post => sub { });
	$app->redirect($URL);
	$app->log("[QSF] drop a spam comment from " . $comment->author) if $ENABLE_LOGGING;
    }
}

sub comment_evil_redirect {
    my $app = shift;
    my $q = $app->{query};
    my $mode = $q->param('__mode') || $app->{default_mode};
    return if $mode ne 'post';
    my $comment = _make_pseudo_comment($app);
    if (is_comment_spam($comment)) {
	$app->add_methods(post => sub { });
	$app->redirect($q->param('url') || $URL);
	$app->log("[QSF] drop a spam comment from " . $comment->author) if $ENABLE_LOGGING;
    }
}

sub tbping_filter {
    my ($eh, $app, $tbping) = @_;
    if (is_tbping_spam($tbping)) {
	$app->log("[QSF] drop a spam tbping from " . $tbping->blog_name) if $ENABLE_LOGGING;
	return 0;
    }
    return 1;
}

sub tbping_throttle_filter {
    my ($eh, $app, $tb) = @_;
    my $tbping = _make_pseudo_tbping($app);
    if (is_tbping_spam($tbping)) {
	$app->log("[QSF] drop a spam tbping from " . $tbping->blog_name) if $ENABLE_LOGGING;
	return 0;
    }
    return 1;
}

sub tbping_error {
    my $app = shift;
    my $q = $app->{query};
    my $mode = $q->param('__mode') || $app->{default_mode};
    return if $mode ne 'ping';
    my $tbping = _make_pseudo_tbping($app);
    if (is_tbping_spam($tbping)) {
	$app->add_methods('ping' => sub { });
	$app->_response(Error => 'Spam TBPing!', Code => 403);
	$app->log("[QSF] drop a spam tbping from " . $tbping->blog_name) if $ENABLE_LOGGING;
    }
}

1;
