<?php
function smarty_function_MTLink($args, &$ctx) {
    // status: incomplete
    // parameters: template, entry_id
    if (isset($args['template'])) {
        $name = $args['template'];
        $tmpl = $ctx->mt->db->load_index_template($ctx, $name);
        $blog = $ctx->stash('blog');
        $site_url = $blog['blog_site_url'];
        if (!preg_match('!/$!', $site_url)) $site_url .= '/';
        return $site_url . $tmpl['template_outfile'];
    } elseif (isset($args['entry_id'])) {
        $arg = array('entry_id' => $args['entry_id']);
        list($entry) = $ctx->mt->db->fetch_entries($arg);
        $ctx->localize(array('entry'));
        $ctx->stash('entry', $entry);
        $link = $ctx->tag('EntryPermalink',$args);
        $ctx->restore(array('entry'));
        return $link;
    }
    return '';
}
?>
