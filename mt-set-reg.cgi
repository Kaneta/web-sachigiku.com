#!/usr/bin/perl -w
# Copyright 2001-2004 Six Apart. This code cannot be redistributed without
# permission from www.movabletype.org.
#
# $Id: mt-set-reg.cgi,v 1.3 2004/05/17 19:51:25 ezra Exp $

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

use CGI;
my $q = new CGI;

local $| = 1;
print "Content-Type: text/html\n\n";
print "<pre>\n\n";

eval {
    local $SIG{__WARN__} = sub { print "**** WARNING: $_[0]\n" };

    require MT;

    my $mt = MT->new( Config => $MT_DIR . 'mt.cfg')
        or die MT->errstr;

    print "Setting the registration key.\n";
    
    #print join " ", (map { "$_=" . $ENV{$_} } keys %ENV);

    my $key = $q->param('k') || $ARGV[0]
	|| die "No key supplied in k parameter.";

    my $blog = MT::Blog->load();
    $blog->mt_update_key($key);
    $blog->save();

    print <<HTML;

Your registration key has been set to $key

HTML
};
if ($@) {
    print <<HTML;

An error occurred while setting the registration key:

$@

HTML
}

print "</pre>\n";
