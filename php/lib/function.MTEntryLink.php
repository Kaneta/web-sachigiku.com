<?php
function smarty_function_MTEntryLink($args, &$ctx) {
    $args['no_anchor'] = 1;
    $link = $ctx->tag('EntryPermalink', $args);
    return $link;
}
?>
