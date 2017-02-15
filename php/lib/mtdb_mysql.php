<?php
# Copyright 2001-2004 Six Apart. This code cannot be redistributed without
# permission from www.movabletype.org.
#
# $Id: mtdb_mysql.php,v 1.11 2004/08/29 18:01:44 ezra Exp $

require_once("ezsql".DIRECTORY_SEPARATOR."ezsql_mysql.php");
require_once("mtdb_base.php");

class MTDatabase_mysql extends MTDatabaseBase {
    var $vendor = 'mysql';
}
?>
