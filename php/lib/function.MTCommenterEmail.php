<?php
function smarty_function_MTCommenterEmail($args, &$ctx) {
    $a =& $ctx->stash('commenter');
    isset($a) ? $a['session_email'] : '';
}
?>
