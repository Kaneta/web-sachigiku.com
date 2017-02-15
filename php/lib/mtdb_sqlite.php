<?php
# Copyright 2001-2004 Six Apart. This code cannot be redistributed without
# permission from www.movabletype.org.
#
# $Id: mtdb_sqlite.php,v 1.8 2004/08/29 18:01:44 ezra Exp $

require_once("ezsql".DIRECTORY_SEPARATOR."ezsql_sqlite.php");
require_once("mtdb_base.php");

class MTDatabase_sqlite extends MTDatabaseBase {
    var $vendor = 'sqlite';
    function MTDatabase($dbuser, $dbpassword, $dbname, $dbhost) {
        parent::MTDatabaseBase($dbname);
    }
}
?>
