<?php
function smarty_function_MTStaticWebPath($args, &$ctx) {
    $path = $ctx->mt->config['StaticWebPath'];
    if (substr($path, strlen($path) - 1, 1) != '/')
        $path .= '/';
    return $path;
}
?>
