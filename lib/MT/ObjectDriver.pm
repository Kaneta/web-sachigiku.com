# Copyright 2001-2004 Six Apart. This code cannot be redistributed without
# permission from www.movabletype.org.
#
# $Id: ObjectDriver.pm,v 1.11 2004/04/29 02:42:57 ezra Exp $

package MT::ObjectDriver;
use strict;

use MT::ConfigMgr;

use MT::ErrorHandler;
@MT::ObjectDriver::ISA = qw( MT::ErrorHandler );

sub new {
    my $class = shift;
    my $type = shift;
    $class .= "::" . $type;
    eval "use $class;";
    die "Unsupported driver $class: $@" if $@;
    my $driver = bless {}, $class;
    $driver->init(@_) or return $class->error($driver->errstr);
    $driver;
}

sub init {
    my $driver = shift;
    $driver->{cfg} = MT::ConfigMgr->instance;
    $driver;
}

sub cfg { $_[0]->{cfg} }

sub load;
sub exists;
sub save;


sub set_callback_routine {
    my $driver = shift;
    $driver->{callback_routine} = $_[0];
}

sub run_callbacks {
    my $driver = shift;
    my $cb;
    if (($cb = $driver->{callback_routine}) && (ref($cb) eq 'CODE')){
	$cb->('MT', @_);
    }
}

1;
