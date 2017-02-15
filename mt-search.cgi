#!/usr/bin/perl -w

# Original copyright 2001-2002 Jay Allen.
# Modifications and integration Copyright 2001-2004 Six Apart.
# This code cannot be redistributed without
# permission from www.movabletype.org.
#
# $Id: mt-search.cgi,v 1.3 2004/05/17 19:51:25 ezra Exp $
use strict;

my($MT_DIR);
BEGIN {
    if ($0 =~ m!(.*[/\\])!) {
        $MT_DIR = $1;
    } else {
        $MT_DIR = './';
    }
    unshift @INC, $MT_DIR . 'lib';
    unshift @INC, $MT_DIR . 'extlib';
}

eval {
    require MT::App::Search;
    my $app = MT::App::Search->new( Config => $MT_DIR . 'mt.cfg' )
        or die MT::App::Search->errstr;
    local $SIG{__WARN__} = sub { $app->trace($_[0]) };
    $app->run;
};
if ($@) {
    print "Content-Type: text/html\n\n";
    print "Got an error: $@";
}
