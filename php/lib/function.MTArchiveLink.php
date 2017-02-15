<?php
function smarty_function_MTArchiveLink($args, &$ctx) {
    $inside_cat = $ctx->stash('inside_mt_categories');
    if ($inside_cat) {
        return $ctx->tag('CategoryArchiveLink', $args);
    }

    $blog = $ctx->stash('blog');
    $at = isset($args['archive_type']) ? $args['archive_type'] : $ctx->stash('current_archive_type');
    $ts = $ctx->stash('current_timestamp');
    if ($at == 'Monthly') {
         $ts = substr($ts, 0, 6) . '01000000';
    } elseif ($at == 'Daily') {
         $ts = substr($ts, 0, 8) . '000000';
    } elseif ($at == 'Weekly') {
         require_once("MTUtil.php");
         list($ws, $we) = start_end_week($ts);
         $ts = $ws;
    } elseif ($at == 'Yearly') {
         $ts = substr($ts, 0, 4) . '0101000000';
    } elseif ($at == 'Individual') {
        $args['archive_type'] or $args['archive_type'] = $at;
        return $ctx->tag('EntryPermalink', $args);
    }
    $args['blog_id'] = $blog['blog_id'];
    return $ctx->mt->db->archive_link($ts, $at, $args);
}
?>
