# Copyright 2001-2004 Six Apart. This code cannot be redistributed without
# permission from www.movabletype.org.
#
# $Id: Promise.pm,v 1.5 2004/10/06 01:50:28 ezra Exp $

package MT::Promise;
use Exporter;
*import = \&Exporter::import;
@EXPORT_OK = qw(delay force lazy);

sub new {
    my ($class, $code) = @_;
    my $this = \$code;
    bless $this, $class;
}

sub delay {
    my ($this) = @_;
    __PACKAGE__->new($this);
}

sub lazy (&) {
    my ($this) = @_;
    __PACKAGE__->new($this);    
}

sub force {
    my ($this) = @_;
    return $this if (ref $this ne 'MT::Promise');
    if (ref $$this eq 'CODE') {
	$$this = $$this->();
    } else {
	return $$this;
    } 
}

1;
