#!/usr/bin/perl -w

# Copyright 2001-2004 Six Apart. This code cannot be redistributed without
# permission from www.movabletype.org.
#
# $Id: mt-comments.cgi,v 1.35 2004/05/17 19:51:25 ezra Exp $
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
    require MT::App::Comments;
    my $app = MT::App::Comments->new( Config => $MT_DIR . 'mt.cfg',
                                      Directory => $MT_DIR )
        or die MT::App::Comments->errstr;
    local $SIG{__WARN__} = sub { $app->trace($_[0]) };
    $app->run;
};
if ($@) {
    print "Content-Type: text/html\n\n";
    print "An error occurred: $@";
}
