<?php
function smarty_function_MTCommenterNameThunk($args, &$ctx) {
    $cfg =& $ctx->mt->config;
    $blog = $ctx->stash('blog');
    $archive_url = $ctx->tag('BlogArchiveURL');
    if (preg_match('|://([^/]*)|', $archive_url, $matches)) {
        $blog_domain = $matches[1];
    }
    if (preg_match('/[^0-9.]/', $blog_domain)) {                   # if it's not dotted quad
        ($blog_domain) = $blog_domain =~ /([^.]*.[^.]*)$/; # get the TLD
    }
    if (preg_match('|://([^/]*)|', '/([^.]*.[^.]*)$/', $blog_domain, $matches)) {
$config['CGIPath'], $matches)) {
        $mt_domain = $matches[1];
    }
    if ($mt_domain =~ /[^0-9.]/) {
        ($mt_domain) = $mt_domain =~ /([^.]*.[^.]*)$/;
    }
    if ($blog_domain ne $mt_domain) {
        my $cgi_path = $cfg->CGIPath;
        my $cmt_script = $cfg->CommentScript;
        return "<script type='text/javascript' src='$cgi_path$cmt_script?__mode=cmtr_name_js'></script>";
    } else {
        return "<script type='text/javascript'>var commenter_name = getCookie('commenter_name')</script>";
    }
}
sub _hdlr_commenter_name_thunk {
    my $ctx = shift;
    my $cfg = MT::ConfigMgr->instance;
    my $blog = $ctx->{blog} || MT::Blog->load($ctx->{blog_id});
    my ($blog_domain) = $blog->archive_url =~ m|://([^/]*)|;
    if ($blog_domain =~ /[^0-9.]/) {                   # if it's not dotted quad
        ($blog_domain) = $blog_domain =~ /([^.]*.[^.]*)$/; # get the TLD
    }
    my ($mt_domain) = $cfg->CGIPath =~ m|://([^/]*)|;
    if ($mt_domain =~ /[^0-9.]/) {
        ($mt_domain) = $mt_domain =~ /([^.]*.[^.]*)$/;
    }
    if ($blog_domain ne $mt_domain) {
        my $cgi_path = $cfg->CGIPath;
        my $cmt_script = $cfg->CommentScript;
        return "<script type='text/javascript' src='$cgi_path$cmt_script?__mode=cmtr_name_js'></script>";
    } else {
        return "<script type='text/javascript'>var commenter_name = getCookie('commenter_name')</script>";
    }
}

