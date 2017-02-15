<?php
function smarty_block_MTArchiveList($args, $content, &$ctx, &$repeat) {
    $localvars = array('current_archive_type', 'current_timestamp', 'current_timestamp_end', 'entries', 'archive_count', '_archive_list_num', '_archive_list_results','entry');
    if (!isset($content)) {
        require_once("archive_lib.php");
        $blog = $ctx->stash('blog');
        $at = $ctx->stash('current_archive_type');
        $at or $at = $blog['blog_archive_type'];
        if ($arg_at = $args['archive_type']) {
            $at = $arg_at;
        } elseif ($blog_at = $blog['blog_archive_type_preferred']) {
            $at = $blog_at;
        } elseif (empty($at)) {
            $types = explode(',', $at);
            $at = $types[0];
        }
        if (empty($at) || $at == 'None') {
            $repeat = false;
            return '';
        }

        $ctx->localize($localvars);
        $ctx->stash('current_archive_type', $at);
        ## If we are producing a Category archive list, don't bother to
        ## handle it here--instead hand it over to <MTCategories>.
        if ($at == 'Category') {
            require_once("block.MTCategories.php");
            return smarty_block_MTCategories($args, $content, $ctx, $repeat);
        }
        $blog_id = $blog['blog_id'];
        $args['sort'] = 'created_on';
        $args['direction'] = 'descend';
        $args['archive_type'] = $at;
        $args['blog_id'] = $blog_id;

        $archive_list_results =& $ctx->mt->db->get_archive_list($args);
        $ctx->stash('_archive_list_results', $archive_list_results);
        # allow <MTEntries> to load them
        $ctx->stash('entries', null);
        $i = 0;
    } else {
        $at = $ctx->stash('current_archive_type');
        $archive_list_results = $ctx->stash('_archive_list_results');
        $i = $ctx->stash('_archive_list_num');
    }

    if ($at == 'Category') {
        $content = smarty_block_MTCategories($args, $content, $ctx, $repeat);
        if (!$repeat)
            $ctx->restore($localvars);
        return $content;
    }

    if ($i < count($archive_list_results)) {
        $grp = $archive_list_results[$i];
        if ($at == 'Individual') {
            $cnt = 1;
            $entry_id = $grp[0];
            $entry = $ctx->mt->db->fetch_entry($entry_id);
            $ctx->stash('current_timestamp', $grp[1]);
            $ctx->stash('entry', $entry);
            #$ctx->stash('entries', array($entry));
            $ctx->stash('entries', array());
        } else {
            $cnt = array_shift($grp);
        }
        $sec_ts = '_al_'.$at.'_section_timestamp';
        list($start, $end) = $sec_ts($ctx, $grp);
        $ctx->stash('current_timestamp', $start);
        $ctx->stash('current_timestamp_end', $end);
        $ctx->stash('archive_count', $cnt);
        $ctx->stash('_archive_list_num', $i + 1);
        $repeat = true;
    } else {
        $ctx->restore($localvars);
        $repeat = false;
    }
    return $content;
}
?>
