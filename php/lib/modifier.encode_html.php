<?php
function smarty_modifier_encode_html($text) {
     global $mt;
     $charset = $mt->config['PublishCharset'];
     return htmlentities($text, ENT_COMPAT, $charset );
}
?>
