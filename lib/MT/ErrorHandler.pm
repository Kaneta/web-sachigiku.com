# Copyright 2001-2004 Six Apart. This code cannot be redistributed without
# permission from www.movabletype.org.
#
# $Id: ErrorHandler.pm,v 1.9 2004/04/29 02:42:57 ezra Exp $

package MT::ErrorHandler;
use strict;

use vars qw( $ERROR );

sub new    { bless {}, shift }
sub error  {
    my $msg = $_[1] || '';
    $msg .= "\n" unless $msg =~ /\n$/;
    if (ref($_[0])) {
        $_[0]->{_errstr} = $msg;
    } else {
        $ERROR = $msg;
    }
    return;
 }
sub errstr { ref($_[0]) ? $_[0]->{_errstr} : $ERROR }

1;
__END__


=head1 NAME

MT::ErrorHandler - MT error handling

=head1 SYNOPSIS

    package Foo;
    use MT::ErrorHandler;
    @Foo::ISA = qw( MT::ErrorHandler );

    sub class_method {
        my $class = shift;
        ...
        return $class->error("Help!")
            unless $continue;
    }

    sub object_method {
        my $obj = shift;
        ...
        return $obj->error("I am no more")
            unless $continue;
    }

    package main;
    use Foo;

    Foo->class_method or die Foo->errstr;

    my $foo = Foo->new;
    $foo->object_method or die $foo->errstr;

=head1 DESCRIPTION

I<MT::ErrorHandler> provides an error-handling mechanism for all <MT>
modules/classes. It is meant to be used as a base class for classes that wish
to use its error-handling methods: derived classes use its two methods,
I<error> and I<errstr>, to communicate error messages back to the calling
program.

On failure (for whatever reason), a subclass should call I<error> and return
to the caller; I<error> itself sets the error message internally, then returns
C<undef>. This has the effect of the method internally, then returns C<undef>.
This has the effect of the method that failed returning C<undef> to the
caller. The caller should check for errors by checking for a return value of
C<undef>, and in this case should call I<errstr> to get the value of the error
message. Note that calling I<errstr> when an error has not occurred is
undefined behavior and will I<rarely> do what you want.

As demonstrated in the I<SYNOPSIS> (above), I<error> and I<errstr> work both
as class methods and as object methods.

=head1 USAGE

=head2 Class->error($message)

=head2 $object->error($message)

Sets the error message for either the class I<Class> or the object
I<$object> to the message I<$message>. Returns C<undef>.

=head2 Class->errstr

=head2 $object->errstr

Accesses the last error message set in the class I<Class> or the
object I<$object>, respectively, and returns that error message.

=head1 AUTHOR & COPYRIGHTS

Please see the I<MT> manpage for author, copyright, and license information.

=cut
