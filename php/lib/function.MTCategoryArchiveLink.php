<?php
function smarty_function_MTCategoryArchiveLink($args, &$ctx) {
    $category = $ctx->stash('category') or $ctx->stash('archive_category');
    if (!$category) return '';
    $url = $ctx->mt->db->category_link($category['category_id'], $args);
    return $url;
}
?>
