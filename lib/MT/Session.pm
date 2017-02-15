# Copyright 2001-2004 Six Apart. This code cannot be redistributed without
# permission from www.movabletype.org.
#
# $Id: Session.pm,v 1.7 2004/07/26 22:59:28 ezra Exp $

package MT::Session;
use strict;

use MT::Object;
@MT::Session::ISA = qw( MT::Object );
__PACKAGE__->install_properties({
    columns => [ qw(id data email name kind start) ],
    indexes => { id => 1, start => 1, kind => 1 },
    datasource => 'session',
});

sub get_unexpired_value {
    my $timeout = shift;
    my $candidate = __PACKAGE__->load(@_);
    if ($candidate && $candidate->start() < time - $timeout) {
        $candidate->remove();
        $candidate = undef;
    }
    return $candidate;
}

1;

__END__

=pod

=head1 NAME

MT::Session - temporary storage of arbitrary data.

=head1 SYNOPSIS

    MT::Session->get_unexpired_value($timeout, { id => $id });

Fetches the specified session record, if it is current (within last
$timeout seconds). After the $timeout parameter, the arguments are
treated exactly the same as those of MT::Object::load.

=cut

