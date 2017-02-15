<?php
function smarty_modifier_dirify($text) {
    require_once("MTUtil.php");
    return dirify($text);
}
?>
