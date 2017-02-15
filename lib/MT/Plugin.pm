# Copyright 2001-2004 Six Apart. This code cannot be redistributed without
# permission from www.movabletype.org.
#
# $Id: Plugin.pm,v 1.9 2004/06/15 20:18:59 ezra Exp $

package MT::Plugin;

use strict;

use MT::ErrorHandler;
@MT::Plugin::ISA = qw( MT::ErrorHandler );

sub new {
    my $class = shift;
    my ($this) = ref$_[0] ? @_ : {@_};
    require Data::Dumper;
    bless $this, $class;
}

sub name {
    my $this = shift;
    my ($new_name) = @_;
    $this->{name} = $new_name if ($new_name);
    return $this->{name};
}

sub config_link {
    my $this = shift;
    my ($new_config_link) = @_;
    $this->{config_link} = $new_config_link if ($new_config_link);
    return $this->{config_link};
}

sub doc_link {
    my $this = shift;
    my ($new_doc_link) = @_;
    $this->{doc_link} = $new_doc_link if ($new_doc_link);
    return $this->{doc_link};
}

sub description {
    my $this = shift;
    my ($new_desc) = @_;
    $this->{description} = $new_desc if ($new_desc);
    return $this->{description};
}

sub envelope {
    my $this = shift;
    my ($new_envelope) = @_;
    $this->{envelope} = $new_envelope if ($new_envelope);
    return $this->{envelope};
}

sub set_config_value {
    my $this = shift;
    my ($variable, $value) = @_;
    use MT::PluginData;
    my $pdata_obj = MT::PluginData->load({plugin => $this->name(),
					  key => 'configuration'});
    if (!$pdata_obj) {
	$pdata_obj = MT::PluginData->new();
	$pdata_obj->plugin($this->name());
	$pdata_obj->key('configuration');
    }
    my $configuration = $pdata_obj->data();
    $configuration->{$variable} = $value;
    $pdata_obj->data($configuration);
    $pdata_obj->save();
}

sub get_config_hash {
    my $this = shift;
    require MT::PluginData;
    my $pdata_obj = MT::PluginData->load({plugin => $this->name(),
					  key => 'configuration'});
    return $pdata_obj && $pdata_obj->data()
	? $pdata_obj->data() : undef;
}

sub get_config_value {
    my $this = shift;
    my $config = $this->get_config_hash();
    return $config ? $config->{$_[0]} : undef;
}

1;
__END__

=head1 NAME

MT::Plugin - Movable Type class holding information that describes a
plugin

=head1 SYNOPSIS

  $plugin = new MT::Plugin({name => "Example Plugin, v1.12",
			    description => "Frobnazticates all Diffyhorns",
			    config_link => <configuration URL>,
			    doc_link => <documentation URL>});

=head1 DESCRIPTION

An I<MT::Plugin> object holds data about a plugin which is used to help
users understand what the plugin does and let them configure the
plugin.

Normally, a plugin will construct an I<MT::Plugin> object and pass it
to the C<add_plugin> method of the I<MT> class:

    MT->add_plugin($plugin);

This will insert a slug for that plugin on the main MT page; the slug
gives the name and description and provides links to the documentation
and configuration pages, if any.

When adding callbacks, you will use the plugin object as well; this
object is used to help the user identify errors that arise in
executing the callback. For example, to add a callback which is
executed before the I<MT::Foo> object is saved to the database, you might
make a call like this:

   MT::Foo->add_callback("pre_save", 10, 
			 $plugin, \&callback_function);

This call will tell I<MT::Foo> to call the function
C<callback_function> just before executing any C<save> operation. The
number '10' is signalling the priority, which controls the order in
which various plugins are called. Lower number callbacks are called
first.

=head1 ARGUMENTS

=over 4

=item * name

A human-readable string identifying the plugin, including its version
number. This will be displayed in the plugin's slug on the MT front
page.

=item * description (optional)

A longer string giving a brief description of what the plugin does.

=item * doc_link (optional)

A URL pointing to some documentation for the plugin. This can be a
relative path, in which case it identifies documentation within the
plugin's distribution, or it can be an absolute URL, pointing at
off-site documentation.

=item * config_link (optional)

The relative path of a CGI script or some other configuration
interface for the plugin. [TBD: relative to what? Need to figure out
how cgi-bin directories are treated?]

=head1 Methods

Each of the above arguments to the constructor is also a 'getter'
method that returns the corresponding value. C<MT::Plugin> also offers
the following methods:

=item * envelope

Returns the path to the plugin, relative to the MT directory. This is
determined automatically when the plugin is loaded.

=item * set_config_value

TBD

=item * get_config_value

TBD

=head1 AUTHOR & COPYRIGHTS

Please see the I<MT> manpage for author, copyright, and license information.

=cut
