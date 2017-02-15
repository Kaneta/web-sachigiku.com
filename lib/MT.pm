# Copyright 2001-2004 Six Apart. This code cannot be redistributed without
# permission from www.movabletype.org.
#
# $Id: MT.pm,v 1.214 2004/09/30 01:01:13 ezra Exp $

package MT;
use strict;

use vars qw( $VERSION $PORTAL);
$VERSION = '3.151-ja';
$PORTAL = 'www.movabletype.jp';

use MT::ConfigMgr;
use MT::Object;
use MT::Blog;
use MT::Util qw( start_end_day start_end_week start_end_month start_end_period
                 archive_file_for get_entry );
use MT::I18N;
use File::Spec;
use File::Basename;
use Fcntl qw( LOCK_EX );

use MT::ErrorHandler;
@MT::ISA = qw( MT::ErrorHandler );

use vars qw( %Text_filters );

sub version_number {
    (my $ver = $VERSION) =~ s/[^\d\.].*$//;
    $ver;
}

sub version_slug {
    return <<SLUG;
Powered by Movable Type
Version $VERSION
http://$PORTAL/
SLUG
}

# MT and all it's subclasses are now singleton classes, meaning you
# can only have one instance. MT->instance() returns that one
# instance. MT->new() is now an alias to instance.

my $mt;

sub instance {
    return $mt if ($mt);

    my $class = shift;
    $mt = bless { }, $class;
    $mt->init(@_) or
        return $class->error($mt->errstr);
    $mt;
}

# unplug 
# Removes the global reference to the MT instance. Returning from all
# local scopes that have references should cause the process to
# DESTROY the object, thus getting rid of anything that might
# interfere with the next request.  This is only necesssary because we
# have some crap that's request-specific crammed into the MT
# instance. Someday we should cull that stuff out to MT::Request.
sub unplug {
    $mt = undef;
}

sub log {
    shift if ref $_[0];
    require MT::Log;
    my $logentry = new MT::Log();
    $logentry->message($_[0]);
    $logentry->save();
    print STDERR "Message: " . $_[0] . "\n";
}
my $plugin_envelope;           # this is used by the plugin loader to tell
                               # add_plugin what directory the plugin is in.
use vars '@Plugins';

sub add_plugin {
    my $class = shift;
    my ($plugin) = @_;
    $plugin->envelope($plugin_envelope);
    push @Plugins, $plugin if UNIVERSAL::isa($plugin, 'MT::Plugin');
}

#xxxx TBD FIXME: move this down to MT::App
use vars '%PluginActions';
sub add_plugin_action {
    my $class = shift;
    my ($object_type, $action_link, $link_text) = @_;
    $action_link .= '?' unless $action_link =~ m.\?.;
    push @{$PluginActions{$object_type}},
         { page => MT::ConfigMgr->instance()->CGIPath . 
	       $plugin_envelope . 
	       '/' . $action_link,
	   link_text => $link_text };
}

my %Methods = (
    PreEntrySave => 'MT::Entry::pre_save',
    PreCommentSave => 'MT::Comment::pre_save',
    CommentThrottleFilter => 'CommentThrottleFilter',
    TBPingThrottleFilter => 'TBPingThrottleFilter',
    AppPostEntrySave => 'AppPostEntrySave',
    CommentFilter => 'CommentFilter',
    TBPingFilter => 'TBPingFilter',
    BuildFileFilter => 'BuildFileFilter',
    BuildFile => 'BuildFile',
    PeriodicTask => 'PeriodicTask',
);
my @Callbacks;
sub add_callback {
    my $class = shift;
    my($meth, $priority, $plugin, $code) = @_;
    if (ref $plugin && !UNIVERSAL::isa($plugin, "MT::Plugin")) {
	return $class->error("If present, 3rd argument to add_callback "
			     . "must be an object of type MT::Plugin");
    }
    if ((ref$code) ne 'CODE') {
	return $class->error('4th argument to add_callback must be '
			     . 'a CODE reference.');
    }
    unless ($meth =~ /::/) {
        $meth = $Methods{$meth}
            or return $class->error("Invalid callback name $meth");
    }
    # 0 and 11 are exclusive.
    if ($priority == 0 || $priority == 11) {
	if ($Callbacks[$priority]->{$meth}) {
	    return $class->error("Two plugins are in conflict");
	}
    }
    return $class->error("Invalid priority level $priority at add_callback")
	if (($priority < 0) || ($priority > 11));
    require MT::Callback;
    push @{$Callbacks[$priority]->{$meth}}, new MT::Callback(plugin => $plugin, 
							  code => $code,
							  priority => $priority,
							  method => $meth);
}

use vars qw( $CB_ERR );

sub callback_error { $CB_ERR = $_[0]; }
sub callback_errstr { $CB_ERR }

# A callback should return a true/false value. The result of
# run_callbacks is the logical AND of all the callback's return
# values. Some hookpoints will ignore the return value: e.g. object
# callbacks don't use it. By convention, those that use it have Filter
# at the end of their names (CommentPostFilter, CommentThrottleFilter,
# etc.)
# Note: this composition is not short-circuiting. All callbacks are
# executed even if one has already returned false.
# ALSO NOTE: failure (dying or setting $cb->errstr) does not force a
# "false" return.
# THINK: are there cases where a true value should override all false values?
# that is, where logical OR is the right way to compose multiple callbacks?
sub run_callbacks {
    my $class = shift;
    my($meth, @args) = @_;
    my @errors;
    my $filter_value = 1;
    my $result = eval {
	my $try_callback = sub {       # return value of $try_callback is ignored
	    my ($cb) = @_;
	    $cb->error();                         # reset the error string
	    if (ref $cb->{code} eq 'CODE') {
		my $result = eval {
		    my $temp = $cb->invoke(@args);
		    $filter_value &&= $temp;
		}; if ($@) {
                    push @errors, $@;
		    $class->instance->log(($cb->{plugin} ? 
				 ($cb->{plugin}->name() || "Unnamed plugin") :
				 "Unnamed plugin")
				. " died with: " . $@);
		    return 0;
		}
		if ($cb->errstr() =~ /\w/) {
                    push @errors, $cb->errstr();
		    $class->instance->log(($cb->{plugin} ? 
				 ($cb->{plugin}->name() || "Unnamed plugin") :
				 "Unnamed plugin")
				. " returned error: "
				. $cb->errstr());
		    return 0;
		}
	    } else { return 0; }
	    return 1;
	};

	foreach my $callback_sheaf (@Callbacks) {
	    for my $cb (@{$callback_sheaf->{$meth}}) {
		$try_callback->($cb) || next;
	    }
	}
	1;
    };
    $class->instance->log("Callback died: " . $@) if !$result;
    callback_error(join(" ", @errors));
    return $filter_value;
}

sub new {
    &instance;
}

sub init {
    my $mt = shift;
    my %param = @_;

    MT->add_text_filter(__default__ => {
        label => 'Convert Line Breaks',
        on_format => sub { MT::Util::html_text_transform($_[0]) },
    });

    ## Initialize the language to English in case any errors occur in
    ## the rest of the initialization process.
    $mt->set_language('en_us'); 
    my $cfg = $mt->{cfg} = MT::ConfigMgr->instance;
    my($cfg_file);
    unless ($cfg_file = $param{Config}) {
        for my $f (qw( mt.cfg )) {
            $cfg_file = $f, last if -r $f;
        }
    }
    if ($cfg_file) {
        $cfg->read_config($cfg_file) or
            return $mt->error($cfg->errstr);
    }
    $mt->{mt_dir} = "";
    if (my $dir = $param{Directory}) {
        $mt->{mt_dir} = $dir;
    }
    $mt->{mt_dir} = dirname($cfg_file||"")
        if !$mt->{mt_dir} || $mt->{mt_dir} !~ m|^/|;
    $mt->{mt_dir} = $ENV{PWD} if !$mt->{mt_dir} || $mt->{mt_dir} !~ m|^/|;
    $mt->{mt_dir} = dirname($ARGV[0])
        if (!$mt->{mt_dir} || $mt->{mt_dir}) !~ m|^/| && $ARGV[0];
    $mt->{mt_dir} = dirname($ENV{SCRIPT_FILENAME}) 
        if (!$mt->{mt_dir} || $mt->{mt_dir} !~ m|^/|) && $ENV{SCRIPT_FILENAME};
    my %default_dirs = (
        TemplatePath =>  'tmpl',
        CSSPath => 'css',
        ImportPath => 'import',
        PluginPath => 'plugins',
        SearchTemplatePath => 'search_templates',
    );
    my $config_dir = dirname($cfg_file||"");
    for my $meth (keys %default_dirs) {
        $cfg->$meth(File::Spec->catfile($config_dir, $default_dirs{$meth}))
            unless defined $cfg->$meth();
    }
    if ($cfg->ObjectDriver =~ /DBI::(?:mysql|postgres)/) {
        my $pass_file = File::Spec->catfile($config_dir, 'mt-db-pass.cgi');
        local *FH;
        if (open FH, $pass_file) {
            my $pass = <FH>;
            close FH;
            if ($pass) {
                chomp($pass);
                $pass =~ s!^\s*!!;
                $pass =~ s!\s*$!!;
            }
            $cfg->DBPassword($pass);
        }
    }
    MT::Object->set_driver($cfg->ObjectDriver)
        or return $mt->error("Bad ObjectDriver config: "
			     . MT::ObjectDriver->errstr);
    MT::Object->set_callback_routine(\&run_callbacks);

    $mt->set_language($cfg->DefaultLanguage);
    # FIXME: these are request-long caches; should be in MT::Request
    $mt->{__rebuilt} = {};
    $mt->{__cached_maps} = {};
    $mt->{__cached_templates} = {};
    my $plugin_dir = $cfg->PluginPath;
    local *DH;
    if (opendir DH, $plugin_dir) {
        my @p = readdir DH;
        PLUGIN:
        for my $plugin (@p) {
	    next if ($plugin =~ /^\./ || $plugin =~ /~$/);

	    my $load_plugin = sub {
		my ($plugin) = @_;
		die "Bad plugin filename '$plugin'"
		    if ($plugin !~ /^([-\\\/\@\:\w\.\s~]+)$/);
		$plugin = $1;
		eval { require $plugin };
                if ($@) {
                    $mt->log("Plugin error: $plugin $@");
                    return 0;
                }
                return 1;
	    };

	    $plugin = File::Spec->catfile($plugin_dir, $plugin);
	    if (-f $plugin) {
		$plugin_envelope = 'plugins';
		$load_plugin->($plugin) if ($plugin =~ /\.pl$/
                                            && $plugin !~ m{(/|^)\.[^/]*$});
	    } else {
 		my $plugin_path = $plugin;
		$plugin_envelope = $plugin_path;
 		$plugin_envelope =~ s|$plugin_dir|/plugins/|;
		$plugin_envelope =~ s|/+|/|;
		opendir SUBDIR, $plugin_path;
		my @plugins = readdir SUBDIR;
		for my $plugin (@plugins) {
		    my $plugin_file = File::Spec->catfile($plugin_path,
							  $plugin);
		    next if $plugin_file !~ /^[^.].*\.pl$/;
		    if (-f $plugin_file) {
			$load_plugin->($plugin_file) or next PLUGIN;
		    }
		}
		closedir SUBDIR;
	    }
        }
        closedir DH;
    }
    $mt;
}

sub server_path {
    my $mt = shift;
    $mt->{mt_dir};
}

#################### # Rebuilding routines # ####################
# TBD? pull these out to MT::Foreperson, who oversees the building

sub rebuild {
    my $mt = shift;
    my %param = @_;
    my $blog;
    unless ($blog = $param{Blog}) {
        my $blog_id = $param{BlogID};
        $blog = MT::Blog->load($blog_id) or
            return $mt->error(
                $mt->translate("Load of blog '[_1]' failed: [_2]",
                    $blog_id, MT::Blog->errstr));
    }
    return 1 if $blog->is_dynamic;
    my $at = $blog->archive_type || '';
    my @at = split /,/, $at;
    if (my $set_at = $param{ArchiveType}) {
        my %at = map { $_ => 1 } @at;
        return $mt->error(
            $mt->translate("Archive type '[_1]' is not a chosen archive type",
                $set_at)) unless $at{$set_at};
        @at = ($set_at);
    }
    if (@at) {
        require MT::Entry;
        my %arg = ('sort' => 'created_on', direction => 'descend');
        if ($param{Limit}) {
            $arg{offset} = $param{Offset};
            $arg{limit} = $param{Limit};
        }
        my $iter = MT::Entry->load_iter({ blog_id => $blog->id,
					  status => MT::Entry::RELEASE() },
					\%arg);
        my $cb = $param{EntryCallback};
        while (my $entry = $iter->()) {
	    if ($cb) {
		$cb->($entry) || $mt->log($cb->errstr());
	    }
            for my $at (@at) {
                if ($at eq 'Category') {
                    my $cats = $entry->categories;
                    for my $cat (@$cats) {
                        $mt->_rebuild_entry_archive_type(
                            Entry => $entry, Blog => $blog,
                            Category => $cat, ArchiveType => 'Category',
                            NoStatic => $param{NoStatic},
                        ) or return;
                    }
                } else {
                    $mt->_rebuild_entry_archive_type( Entry => $entry,
                                                      Blog => $blog,
                                                      ArchiveType => $at,
                                                      $param{TemplateID}
                                                       ? (TemplateID =>
                                                           $param{TemplateID})
                                                       : (),
                                                      NoStatic => $param{NoStatic})
                        or return;
                }
            }
        }
    }
    unless ($param{NoIndexes}) {
        $mt->rebuild_indexes( Blog => $blog ) or return;
    }
    my $identity_link_image = $blog->site_path . "/nav-commenters.gif";
    # TBD: Use StaticWebPath version unless mt.cfg says use this.
    unless (-f $identity_link_image) {
	my $nav_commenters_gif = (q{47494638396116000f00910200504d4b}.
				  q{ffffffffffff00000021f90401000002}.
				  q{002c0000000016000f0000022c948fa9}.
				  q{19e0bf2208b482a866a51723bd75dee1}.
				  q{70e2f83586837ed773a22fd4ba6cede2}.
				  q{241c8f7ceff9e95005003b});
	$nav_commenters_gif = pack("H*", $nav_commenters_gif);
	eval {
	    if (open(TARGET, ">$identity_link_image")) {
                print TARGET $nav_commenters_gif;
                close TARGET;
            } else {
		$mt->log("Couldn't write to $identity_link_image");
                die;
            }
	};
    }
    1;
}

#   rebuild_entry
#
# $mt->rebuild_entry(Entry => $entry_id,
#                    Blog => [ $blog | $blog_id ],
#                    [ BuildDependencies => (0 | 1), ]
#                    [ OldPrevious => $old_previous_entry_id,
#                      OldNext => $old_next_entry_id, ]
#                    [ NoStatic => (0 | 1), ]
#                    );
sub rebuild_entry {
    my $mt = shift;
    my %param = @_;
    my $entry = $param{Entry} or
        return $mt->error($mt->translate("Parameter '[_1]' is required",
            'Entry'));
    $entry = MT::Entry->load($entry) unless ref $entry;
    my $blog;
    unless ($blog = $param{Blog}) {
        my $blog_id = $entry->blog_id;
        $blog = MT::Blog->load($blog_id) or
            return $mt->error($mt->translate("Load of blog '[_1]' failed: [_2]",
                $blog_id, MT::Blog->errstr));
    }
    return 1 if $blog->is_dynamic;
#    MT::Util::start_background_task(sub {
    my $at = $blog->archive_type;
    if ($at && $at ne 'None') {
        my @at = split /,/, $at;
        for my $at (@at) {
            if ($at eq 'Category') {
                my $cats = $entry->categories;   # (ancestors => 1)
                for my $cat (@$cats) {
                    $mt->_rebuild_entry_archive_type(
                        Entry => $entry, Blog => $blog,
                        ArchiveType => $at, Category => $cat,
                        NoStatic => $param{NoStatic}
                    ) or return;
                }
            } else {
                $mt->_rebuild_entry_archive_type( Entry => $entry,
                                                  Blog => $blog,
                                                  ArchiveType => $at,
                                                  NoStatic => $param{NoStatic}
                ) or return;
            }
        }
    }

    ## The above will just rebuild the archive pages for this particular
    ## entry. If we want to rebuild all of the entries/archives/indexes
    ## on which this entry could be featured etc., however, we need to
    ## rebuild all of the entry's dependencies. Note that all of these
    ## are not *necessarily* dependencies, depending on the usage of tags,
    ## etc. There is not a good way to determine exact dependencies; it is
    ## easier to just rebuild, rebuild, rebuild.

    return 1 unless $param{BuildDependencies};

    ## Rebuild previous and next entry archive pages.
    if (my $prev = $entry->previous(1)) {
        $mt->rebuild_entry( Entry => $prev ) or return;
    }
    if (my $next = $entry->next(1)) {
        $mt->rebuild_entry( Entry => $next ) or return;
    }

    ## Rebuild the old previous and next entries, if we have some.
    if ($param{OldPrevious} && (my $old_prev = MT::Entry->load($param{OldPrevious}))) {
        $mt->rebuild_entry( Entry => $old_prev ) or return;
    }
    if ($param{OldNext} && (my $old_next = MT::Entry->load($param{OldNext}))) {
        $mt->rebuild_entry( Entry => $old_next ) or return;
    }

    ## Rebuild all indexes, in case this entry is on an index.
    $mt->rebuild_indexes( Blog => $blog ) or return;

    ## Rebuild previous and next daily, weekly, and monthly archives;
    ## adding a new entry could cause changes to the intra-archive
    ## navigation.
    my %at = map { $_ => 1 } split /,/, $blog->archive_type;
    for my $at (qw( Daily Weekly Monthly )) {
        if ($at{$at}) {
            my @arg = ($entry->created_on, $entry->blog_id, $at);
            if (my $prev_arch = get_entry(@arg, 'previous')) {
                $mt->_rebuild_entry_archive_type(NoStatic => $param{NoStatic},
                          Entry => $prev_arch,
                          Blog => $blog,
                          ArchiveType => $at) or return;
            }
            if (my $next_arch = get_entry(@arg, 'next')) {
                $mt->_rebuild_entry_archive_type(NoStatic => $param{NoStatic},
                          Entry => $next_arch,
                          Blog => $blog,
                          ArchiveType => $at) or return;
            }
        }
    }
#    });

    1;
}

sub _rebuild_entry_archive_type {
    my $mt = shift;
    my %param = @_;
    my $at = $param{ArchiveType} or
        return $mt->error($mt->translate("Parameter '[_1]' is required",
            'ArchiveType'));
    return 1 if $at eq 'None';
    my $entry = ($param{ArchiveType} ne 'Category') ? ($param{Entry} or
        return $mt->error($mt->translate("Parameter '[_1]' is required",
            'Entry'))) : undef;
    my $blog;
    unless ($blog = $param{Blog}) {
        my $blog_id = $entry->blog_id;
        $blog = MT::Blog->load($blog_id) or
            return $mt->error($mt->translate("Load of blog '[_1]' failed: [_2]",
                $blog_id, MT::Blog->errstr));
    }

    ## Load the template-archive-type map entries for this blog and
    ## archive type. We do this before we load the list of entries, because
    ## we will run through the files and check if we even need to rebuild
    ## anything. If there is nothing to rebuild at all for this entry,
    ## we save some time by not loading the list of entries.
    require MT::TemplateMap;
    my @map;
    if (my $maps = $mt->{__cached_maps}{$at . $blog->id}) {
        @map = @$maps;
    } else {
        @map = MT::TemplateMap->load({ archive_type => $at,
                                       blog_id => $blog->id,
                                       $param{TemplateID}
                                         ? (template_id => $param{TemplateID})
                                         : ()
                                     });
        $mt->{__cached_maps}{$at . $blog->id} = \@map;
    }
#     return $mt->error($mt->translate(
#         "You selected the archive type '[_1]', but you did not " .
#         "define a template for this archive type.", $at)) unless @map;
    return 1 unless @map;
    my @map_build;

#     ## We keep a running total of the pages we have rebuilt
#     ## in this session in $mt->{__rebuilt}.
#     my $done = $mt->{__rebuilt};
    for my $map (@map) {
        my $file = archive_file_for($entry, $blog, $at, $param{Category}, $map);
	if (!defined($file)) {
	    return $mt->error($mt->translate($blog->errstr()));
	}
        push @map_build, $map unless $mt->{done}->{$file};
        $map->{__saved_output_file} = $file;
    }
    return 1 unless @map_build;
    @map = @map_build;
    
    my(%cond);
    require MT::Template::Context;
    my $ctx = MT::Template::Context->new;
    $ctx->{current_archive_type} = $at;
    
    $cond{IfAllowCommentHTML} = $blog->allow_comment_html;
    $cond{IfRegistrationRequired} = !$blog->allow_unreg_comments;
    $cond{IfCommentsAllowed} = $blog->allow_unreg_comments
	                         || $blog->allow_reg_comments;
    $cond{IfRegistrationAllowed} = $blog->allow_reg_comments;
    $cond{IfUnregisteredAllowed} = $blog->allow_unreg_comments;
    $cond{IfDynamicComments} = 
	$cond{IfDynamicCommentsStaticPage} = 
	MT::ConfigMgr->instance()->DynamicComments;
    $cond{IfNeedEmail} = $blog->require_comment_emails;
    
    $at ||= "";

    require MT::Promise;
    import MT::Promise qw(delay);
    
    if ($at eq 'Individual') {
        $ctx->stash('entry', $entry);
        $ctx->{current_timestamp} = $entry->created_on;
        $ctx->{modification_timestamp} = $entry->modified_on;
        $cond{EntryIfAllowComments} = $entry->allow_comments;
        $cond{EntryIfCommentsOpen} = $entry->allow_comments &&
            $entry->allow_comments eq '1';
        $cond{EntryIfAllowPings} = $entry->allow_pings;
        $cond{EntryIfExtended} = $entry->text_more ? 1 : 0;
    } elsif ($at eq 'Daily') {
        my($start, $end) = start_end_day($entry->created_on, $blog);
        $ctx->{current_timestamp} = $start;
        $ctx->{current_timestamp_end} = $end;
        my @entries = MT::Entry->load({ created_on => [ $start, $end ],
                                        blog_id => $blog->id,
                                        status => MT::Entry::RELEASE() },
                                      { range_incl => { created_on => 1 } });
        $ctx->stash('entries', delay(sub{\@entries}));
    } elsif ($at eq 'Weekly') {
        my($start, $end) = start_end_week($entry->created_on, $blog);
        $ctx->{current_timestamp} = $start;
        $ctx->{current_timestamp_end} = $end;
        my @entries = MT::Entry->load({ created_on => [ $start, $end ],
                                        blog_id => $blog->id,
                                        status => MT::Entry::RELEASE() },
                                      { range_incl => { created_on => 1 } });
        $ctx->stash('entries', delay(sub{\@entries}));
    } elsif ($at eq 'Monthly') {
        my($start, $end) = start_end_month($entry->created_on, $blog);
        $ctx->{current_timestamp} = $start;
        $ctx->{current_timestamp_end} = $end;
        my @entries = MT::Entry->load({ created_on => [ $start, $end ],
                                        blog_id => $blog->id,
                                        status => MT::Entry::RELEASE() },
                                      { range_incl => { created_on => 1 } });
        $ctx->stash('entries', delay(sub{\@entries}));
    } elsif ($at eq 'Category') {
        my $cat;
        unless ($cat = $param{Category}) {
            return $mt->error($mt->translate(
                "Building category archives, but no category provided."));
        }
        require MT::Placement;
        $ctx->stash('archive_category', $cat);
        my @entries = MT::Entry->load({ blog_id => $blog->id,
                                        status => MT::Entry::RELEASE() },
                         { 'join' => [ 'MT::Placement', 'entry_id',
                                     { category_id => $cat->id } ] });
        $ctx->stash('entries', delay(sub{\@entries}));
    }
    
    $mt->{fmgr} = $blog->file_mgr;  # FIXME: non-local variables cnsdrd hmfl
    my $arch_root = $blog->archive_path;
    return $mt->error($mt->translate("You did not set your Local Archive Path"))
        unless $arch_root;
    
    my ($start, $end) = ($at ne 'Category') ? 
        start_end_period($at, $entry->created_on) : ();
    
    ## For each mapping, we need to rebuild the entries we loaded above in
    ## the particular template map, and write it to the specified archive
    ## file template.
    require MT::Template;
    for my $map (@map) {
        $mt->rebuild_file($blog, $arch_root, $map, $at, $ctx, \%cond,
                          !$param{NoStatic},
                          Category => $param{Category},
                          Entry => $entry,
                          StartDate => $start,
                          ) or return;
    }
    1;
}

sub rebuild_file {
    my $mt = shift;
    my ($blog, $arch_root, $map, $at, $ctx, $cond, 
        $build_static, %specifier) = @_;
    my $entry;
    my $start;
    my $category;
    if ($at eq 'Category') {
        $category = $specifier{Category};
        die "Category archive type requires Categry parameter "
            unless $specifier{Category};
        $category = MT::Category->load($category) unless ref $category;
    } elsif ($at eq 'Individual') {
        $entry = $specifier{Entry};
        $entry = MT::Entry->load($entry) if !ref $entry;
        die "Individual archive type requires Entry parameter"
            unless $specifier{Entry};
    } else {
        # Date-based archive type
        $start = $specifier{StartDate};
        die "Date-based archive types require StartDate parameter" 
            unless $specifier{StartDate};
    }
    my $fmgr = $mt->{fmgr};
    {   # (silly ruse to make the diff more transparent.)
        # Calculate file path and URL for the new entry.
        my $file = File::Spec->catfile($arch_root, $map->{__saved_output_file});
        my $url = $blog->archive_url;
        $url .= '/' unless $url =~ m|/$|;
        $url .= $map->{__saved_output_file};
        
        my $tmpl = $mt->{__cached_templates}{$map->template_id};
        unless ($tmpl) {
            $tmpl = MT::Template->load($map->template_id);
            if ($mt->{cache_templates}) {
                $mt->{__cached_templates}{$tmpl->id} = $tmpl;
            }
        }
        
        my $needs_fileinfo = $blog->needs_fileinfo;
        if ($needs_fileinfo) {
            # Clear out all the FileInfo records that might point at the page 
            # we're about to create
            # MBE: select based on target file rather than source specifier?
            # FYI: if it's an individual entry, we don't use the date as a 
            #      criterion, since this could actually have changed since
            #      the FileInfo was last built.
            # Note: when the date does change, the old date-based archive
            #      doesn't necessarily get fixed, but if another comes along
            #      it will get corrected
            require MT::FileInfo;
            my @finfos = MT::FileInfo->load({ blog_id => $blog->id,
                                              ($at eq 'Category') ?
                                                  (category_id =>
                                                      $category->id)
                                                : (),
                                              ($at eq 'Individual') ?
                                                  (entry_id => $entry->id) :
                                                  ($at ne 'Category') ?
                                                      (startdate => $start) : (),
                                              templatemap_id => $map->id,
                                              archive_type => $at,
                                            });
            for my $finfo (@finfos) {
                $finfo->remove();
            }
        }

        ## Untaint. We have to assume that we can trust the user's setting of
        ## the archive_path, and nothing else is based on user input.
        ($file) = $file =~ /(.+)/s;
        
        my ($rel_url) = ($url =~ m|^(?:[^:]*\:\/\/)?[^/]*(.*)|);
        $rel_url =~ s|//+|/|g;

        my $finfo;
        if ($needs_fileinfo) {
            $finfo = MT::FileInfo->set_info_for_url($rel_url, $file, $at,
                                                  { Blog => $blog->id,
                                                    TemplateMap => $map->id,
                                                    Template => $map->template_id,
                                                    ($at eq 'Individual' && $entry)
                                                        ? (Entry => $entry->id): (),
                                                    StartDate => $start,
                                                    ($category ?
                                                       (Category => $category->id) : ())
                                                   })
                || die "Couldn't create FileInfo because " . MT::FileInfo->errstr();

        # If you rebuild when you've just switched to dynamic pages,
        # we move the file that might be there so that the custom
        # 404 will be triggered.
        if ($tmpl->build_dynamic) {
            rename($finfo->file_path,
                   $finfo->file_path . '.static');        # FIXME: Use filemgr
            $finfo->virtual(1); $finfo->save();
            }
        }
        if (!$tmpl->build_dynamic) {
            if ( $build_static &&
                 MT->run_callbacks('BuildFileFilter', Context => $ctx,
                                   ArchiveType => $at, TemplateMap => $map, 
                                   Blog => $blog, Entry => $entry, 
                                   PeriodStart => $start, Category => $category))
            {
                my $html = undef;
                $html = $tmpl->build($ctx, $cond);
                defined($html) or
                    return $mt->error(($category ?
                                      $mt->translate("Building category '[_1]' failed: [_2]",
                                                     $category->id, $tmpl->errstr) :
                                      $entry ?
                                      $mt->translate("Building entry '[_1]' failed: [_2]",
                                                     $entry->title, $tmpl->errstr):
                                      $mt->translate("Building date-based archive '[_1]' failed: [_2]", $at . $start, $tmpl->errstr)));
                ## First check whether the content is actually
                ## changed. If not, we won't update the published
                ## file, so as not to modify the mtime.  
                # TBD: turn this into a real return.
                $mt->{done}->{$map->{__saved_output_file}}++, next
                    unless $fmgr->content_is_updated($file, \$html);

                ## Determine if we need to build directory structure,
                ## and build it if we do. DirUmask determines
                ## directory permissions.
                my $path = dirname($file);
                $path =~ s!/$!!;  ## OS X doesn't like / at the end in mkdir().
                unless ($fmgr->exists($path)) {
                    $fmgr->mkpath($path)
                        or return $mt->error($mt->translate(
                                                            "Error making path '[_1]': [_2]",
                                                            $path, $fmgr->errstr));
                }
                
                ## By default we write all data to temp files, then rename
                ## the temp files to the real files (an atomic
                ## operation). Some users don't like this (requires too
                ## liberal directory permissions). So we have a config
                ## option to turn it off (NoTempFiles).
                my $use_temp_files = !$mt->{cfg}->NoTempFiles;
                my $temp_file = $use_temp_files ? "$file.new" : $file;
                defined($fmgr->put_data($html, $temp_file))
                    or return $mt->trans_error("Writing to '[_1]' failed: [_2]",
                                               $temp_file, $fmgr->errstr);
                if ($use_temp_files) {
                    $fmgr->rename($temp_file, $file)
                        or return $mt->trans_error("Renaming tempfile '[_1]' failed: [_2]",
                                                   $temp_file, $fmgr->errstr);
                }
                if ($finfo) {
                    $finfo->virtual(0); $finfo->save();
                }
                MT->run_callbacks('BuildFile', Context => $ctx,
                                  ArchiveType => $at, TemplateMap => $map,
                                  FileInfo => $finfo, Blog => $blog,
                                  Entry => $entry, PeriodStart => $start,
                                  Category => $category);
            }
        }
        $mt->{done}->{$map->{__saved_output_file}}++;
    }
    1;
}

sub rebuild_indexes {
    my $mt = shift;
    my %param = @_;
    require MT::Template;
    require MT::Template::Context;
    require MT::Entry;
    my $blog;
    unless ($blog = $param{Blog}) {
        my $blog_id = $param{BlogID};
        $blog = MT::Blog->load($blog_id) or
            return $mt->error($mt->translate("Load of blog '[_1]' failed: [_2]",
                $blog_id, MT::Blog->errstr));
    }
    return 1 if $blog->is_dynamic;
    my $iter;
    if (my $tmpl = $param{Template}) {
        my $i = 0;
        $iter = sub { $i++ < 1 ? $tmpl : undef };
    } else {
        $iter = MT::Template->load_iter({ type => 'index',
            blog_id => $blog->id });
    }
    local *FH;
    my $site_root = $blog->site_path;
    return $mt->error($mt->translate("You did not set your Local Site Path"))
        unless $site_root;
    my $fmgr = $blog->file_mgr;
    while (my $tmpl = $iter->()) {
        ## Skip index templates that the user has designated not to be
        ## rebuilt automatically. We need to do the defined-ness check
        ## because we added the flag in 2.01, and for templates saved
        ## before that time, the rebuild_me flag will be undefined. But
        ## we assume that these templates should be rebuilt, since that
        ## was the previous behavior.
        next if !$param{Force} && (
                (defined $tmpl->rebuild_me && !$tmpl->rebuild_me)
                                   && !$tmpl->build_dynamic);

        my $index = $tmpl->outfile
            or return $mt->error($mt->translate(
                "Template '[_1]' does not have an Output File.", $tmpl->name));
        my $url = join('/', $blog->site_url, $index);
        unless (File::Spec->file_name_is_absolute($index)) {
            $index = File::Spec->catfile($site_root, $index);
        }
        my ($rel_url) = ($url =~ m|^(?:[^:]*\:\/\/)?[^/]*(.*)|);
        $rel_url =~ s|//+|/|g;
        my $needs_fileinfo = $blog->needs_fileinfo;
        if ($needs_fileinfo) {
            require MT::FileInfo;
            my @finfos = MT::FileInfo->load({blog_id => $tmpl->blog_id,
                                             template_id => $tmpl->id,
                                      # ?    #Category => $entry->category_id
                                         } );
            foreach ( @finfos ) { $_->remove(); }
            my $finfo = MT::FileInfo->set_info_for_url($rel_url, $index, 'index',
                                                  { Blog => $tmpl->blog_id,
                                                    Template => $tmpl->id,
                                             # ?    #Category => $entry->category_id
                                                    })
                || die "Couldn't create FileInfo because " . MT::FileInfo->errstr();
            if ($tmpl->build_dynamic) {
                rename($index, $index . ".static");
            }
        }

        ## Untaint. We have to assume that we can trust the user's setting of
        ## the site_path and the template outfile.
        ($index) = $index =~ /(.+)/s;

        if (!$tmpl->build_dynamic) {
            my $ctx = MT::Template::Context->new;
            my $html = $tmpl->build($ctx);
            return $mt->error( $tmpl->errstr ) unless defined $html;

            ## First check whether the content is actually changed. If not,
            ## we won't update the published file, so as not to modify the mtime.
            next unless $fmgr->content_is_updated($index, \$html);

            ## Update the published file.
            my $use_temp_files = !$mt->{cfg}->NoTempFiles;
            my $temp_file = $use_temp_files ? "$index.new" : $index;
            defined($fmgr->put_data($html, $temp_file))
                or return $mt->trans_error("Writing to '[_1]' failed: [_2]",
                                           $temp_file, $fmgr->errstr);
            if ($use_temp_files) {
                $fmgr->rename($temp_file, $index)
                    or return $mt->trans_error("Renaming tempfile '[_1]' failed: [_2]",
                                               $temp_file, $fmgr->errstr);
            }
        }
    }
    1;
}

sub ping {
    my $mt = shift;
    my %param = @_;
    my $blog;
    unless ($blog = $param{Blog}) {
        my $blog_id = $param{BlogID};
        $blog = MT::Blog->load($blog_id) or
            return $mt->error(
                $mt->translate("Load of blog '[_1]' failed: [_2]",
                    $blog_id, MT::Blog->errstr));
    }

    my(@res);

    my $send_updates = 1;
    if (exists $param{OldStatus}) {
        ## If this is a new entry (!$old_status) OR the status was previously
        ## set to draft, and is now set to publish, send the update pings.
        my $old_status = $param{OldStatus};
        if ($old_status && $old_status eq MT::Entry::RELEASE()) {
            $send_updates = 0;
        }
    }

    if ($send_updates) {
        ## Send update pings.
        my @updates = $mt->update_ping_list($blog);
        for my $url (@updates) {
            require MT::XMLRPC;
            if (MT::XMLRPC->ping_update('weblogUpdates.ping', $blog, $url)) {
                push @res, { good => 1, url => $url, type => "update" };
            } else {
                push @res, { good => 0, url => $url, type => "update",
                             error => MT::XMLRPC->errstr };
            }
        }
        if ($blog->mt_update_key) {
            require MT::XMLRPC;
            if (MT::XMLRPC->mt_ping($blog)) {
                push @res, { good => 1, url => $mt->{cfg}->MTPingURL,
                             type => "update" };
            } else {
                push @res, { good => 0, url => $mt->{cfg}->MTPingURL,
                             type => "update", error => MT::XMLRPC->errstr };
            }
        }
    }

    ## Send TrackBack pings.
    if (my $entry = $param{Entry}) {
        my $pings = $entry->to_ping_url_list;

        my %pinged = map { $_ => 1 } @{ $entry->pinged_url_list };
        my $cats = $entry->categories;
        for my $cat (@$cats) {
            push @$pings, grep !$pinged{$_}, @{ $cat->ping_url_list };
        }

        my $ua = MT->new_ua;

        ## Build query string to be sent on each ping.
        my @qs;
        push @qs, 'title=' . MT::Util::encode_url($entry->title);
        push @qs, 'url=' . MT::Util::encode_url($entry->permalink);
        push @qs, 'excerpt=' . MT::Util::encode_url($entry->get_excerpt);
        push @qs, 'blog_name=' . MT::Util::encode_url($blog->name);
        my $qs = join '&', @qs;

        ## Character encoding--best guess. Default to iso-8859-1, just as we
        ## do in MT::Template::Context::_hdlr_publish_charset.
        my $enc = $mt->{cfg}->PublishCharset || 'iso-8859-1';

        for my $url (@$pings) {
            $url =~ s/^\s*//;
            $url =~ s/\s*$//;
            my $req = HTTP::Request->new(POST => $url);
	    $req->content_type("application/x-www-form-urlencoded; charset=$enc");
	    $req->content($qs);
            my $res = $ua->request($req);
            if (substr($res->code, 0, 1) eq '2') {
                my $c = $res->content;
                my($error, $msg) = $c =~
                    m!<error>(\d+).*<message>(.+?)</message>!s;
                if ($error) {
                    push @res, { good => 0, url => $url, type => 'trackback',
                                 error => $msg };
                } else {
                    push @res, { good => 1, url => $url, type => 'trackback' };
                }
            } else {
                push @res, { good => 0, url => $url, type => 'trackback',
                             error => "HTTP error: " . $res->status_line };
            }
        }
    }
    \@res;
}

sub ping_and_save {
    my $mt = shift;
    my %param = @_;
    if (my $entry = $param{Entry}) {
        my $results = $mt->ping(@_) or return;
        my %still_ping;
        my $pinged = $entry->pinged_url_list;
        for my $res (@$results) {
            next if $res->{type} ne 'trackback';
            if (!$res->{good}) {
                $still_ping{ $res->{url} } = 1;
            } else {
                push @$pinged, $res->{url};
            }
        }
        $entry->pinged_urls(join "\n", @$pinged);
        $entry->to_ping_urls(join "\n", keys %still_ping);
        $entry->save or return $mt->error($entry->errstr);
        return $results;
    }
    1;
}

sub needs_ping {
    my $mt = shift;
    my %param = @_;
    my $blog = $param{Blog};
    my $entry = $param{Entry};
    return unless $entry->status == MT::Entry::RELEASE();
    my $old_status = $param{OldStatus};
    my %list;
    ## If this is a new entry (!$old_status) OR the status was previously
    ## set to draft, and is now set to publish, send the update pings.
    if (!$old_status || $old_status ne MT::Entry::RELEASE()) {
        my @updates = $mt->update_ping_list($blog);
        @list{ @updates } = (1) x @updates;
        $list{$mt->{cfg}->MTPingURL} = 1 if $blog && $blog->mt_update_key;
    }
    if ($entry) {
        @list{ @{ $entry->to_ping_url_list } } = ();
        my %pinged = map { $_ => 1 } @{ $entry->pinged_url_list };
        my $cats = $entry->categories;
        for my $cat (@$cats) {
            @list{ grep !$pinged{$_}, @{ $cat->ping_url_list } } = ();
        }
    }
    my @list = keys %list;
    return unless @list;
    \@list;
}

sub update_ping_list {
    my $mt = shift;
    my($blog) = @_;
    my @updates;
    if ($blog->ping_weblogs) {
        push @updates, $mt->{cfg}->WeblogsPingURL;
    }
    if ($blog->ping_blogs) {
        push @updates, $mt->{cfg}->BlogsPingURL;
    }
    if ($blog->ping_technorati) {
        push @updates, $mt->{cfg}->TechnoratiPingURL;
    }
    if (my $others = $blog->ping_others) {
        push @updates, split /\r?\n/, $others;
    }
    my %updates;
    for my $url (@updates) {
        for ($url) {
            s/^\s*//; s/\s*$//;
        }
        next unless $url =~ /\S/;
        $updates{$url}++;
    }
    keys %updates;
}

{
    my $LH;
    sub set_language {
        require MT::L10N;
        $LH = MT::L10N->get_handle($_[1]);
    }

    sub translate {
        my $this = shift;
        my ($format, @args) = @_;
        my $enc = MT::ConfigMgr->instance()->PublishCharset;
        $format = MT::I18N::encode_text($format, $enc, 'utf-8');
        MT::I18N::encode_text($LH->maketext($format, map {MT::I18N::encode_text($_, $enc, 'utf-8')} @args),'utf-8', $enc);
    }

    sub translate_templatized {
        my $mt = shift;
        my($text) = @_;
        $text =~ s!<MT_TRANS ([^>]+)>!
            my($msg, %args) = ($1);
            while ($msg =~ /(\w+)\s*=\s*(["'])(.*?)\2/g) {  #"
                $args{$1} = $3;
            }
            $args{params} = '' unless defined $args{params};
            my @p = map MT::Util::decode_html($_),
                    split /\s*%%\s*/, $args{params};
            @p = ('') unless @p;
            $mt->translate($args{phrase}, @p);
        !ge;
        $text;
    }

    sub current_language { $LH->language_tag }
    sub language_handle { $LH }
}

sub supported_languages {
    my $mt = shift;
    require MT::L10N;
    require File::Basename;
    ## Determine full path to lib/MT/L10N directory...
    my $lib = 
        File::Spec->catdir(File::Basename::dirname($INC{'MT/L10N.pm'}), 'L10N');
    ## ... From that, determine full path to extlib/MT/L10N.
    ## To do that, we look for the last instance of the string 'lib'
    ## in $lib and replace it with 'extlib'. reverse is a nice tricky
    ## way of doing that.
    (my $extlib = reverse $lib) =~ s!bil!biltxe!;
    $extlib = reverse $extlib;
    my @dirs = ( $lib, $extlib );
    my %langs;
    for my $dir (@dirs) {
        opendir DH, $dir or next;
        for my $f (readdir DH) {
            my($tag) = $f =~ /^(\w+)\.pm$/;
            next unless $tag;
            my $lh = MT::L10N->get_handle($tag);
            $langs{$lh->language_tag} = $lh->language_name;
        }
        closedir DH;
    } 
    \%langs;
}

# For your convenience
sub trans_error {
    my $app = shift;
    $app->error($app->translate(@_));
}

sub add_text_filter {
    my $mt = shift;
    my($key, $cfg) = @_;
    $cfg->{label} ||= $key;
    return $mt->error("No executable code") unless $cfg->{on_format};
    $Text_filters{$key} = $cfg;
}

sub all_text_filters { \%Text_filters }

sub apply_text_filters {
    my $mt = shift;
    my($str, $filters, @extra) = @_;
    for my $filter (@$filters) {
        next unless $Text_filters{$filter};
        $str = $Text_filters{$filter}{on_format}->($str, @extra);
    }
    $str;
}

sub new_ua {
    my $class = shift;
    require LWP::UserAgent;
    my $cfg = MT::ConfigMgr->instance;
    if (my $localaddr = $cfg->PingInterface) {
        @LWP::Protocol::http::EXTRA_SOCK_OPTS = (
              LocalAddr => $localaddr,
              Reuse => 1 );
    }
    my $ua = LWP::UserAgent->new;
    $ua->max_size(100_000) if $ua->can('max_size');
    $ua->agent('MovableType/' . MT->VERSION);
    $ua->timeout($cfg->PingTimeout);
    if (my $proxy = $cfg->PingProxy) {
        $ua->proxy(http => $proxy);
        my @domains = split(/,\s*/, $cfg->PingNoProxy);
        $ua->no_proxy(@domains);
    }
    $ua;        
}

sub build_email {
    my $class = shift;
    my($file, $param) = @_;
    my $cfg = MT::ConfigMgr->instance;
    my @paths = (File::Spec->catdir($cfg->TemplatePath, 'email'));
    require HTML::Template;
    my $tmpl;
    eval {
        local $1; ## This seems to fix a utf8 bug (of course).
        $tmpl = HTML::Template->new_file(
            $file,
            path => \@paths,
            search_path_on_include => 1,
            die_on_bad_params => 0,
            global_vars => 1);
    };
    return $class->error("Loading template '$file' failed: $@") if $@;
    for my $key (keys %$param) {
        $tmpl->param($key, $param->{$key});
    }
    $class->translate_templatized($tmpl->output);
}

use MT::Entry 'FUTURE';

sub get_next_sched_post_for_user {
    my ($author_id, @further_blog_ids) = @_;
    require MT::Permission;
    my @perms = MT::Permission->load({author_id => $author_id}, {});
    my @blogs = @further_blog_ids;
    for my $perm (@perms) {
	next unless ($perm->can_edit_config
		     || $perm->can_post
		     || $perm->can_edit_all_posts);
	push @blogs, $perm->blog_id;
    }
    my $next_sched_utc = undef;
    for my $blog_id (@blogs) {
	my $blog = MT::Blog->load($blog_id);
	my $earliest_entry = MT::Entry->load({status => MT::Entry::FUTURE,
					      blog_id => $blog_id},
					     {sort => 'created_on'});
	if ($earliest_entry) {
	    my $entry_utc =MT::Util::ts2iso($blog,$earliest_entry->created_on);
	    if ($entry_utc < $next_sched_utc || !defined($next_sched_utc))
	    {
		$next_sched_utc = $entry_utc;
	    }
	}
    }
    return $next_sched_utc;
}

1;
__END__

=head1 NAME

MT - Movable Type

=head1 SYNOPSIS

    use MT;
    my $mt = MT->new;
    $mt->rebuild(BlogID => 1)
        or die $mt->errstr;

=head1 DESCRIPTION

The I<MT> class is the main high-level rebuilding/pinging interface in the
Movable Type library. It handles all rebuilding operations. It does B<not>
handle any of the application functionality--for that, look to I<MT::App> and
I<MT::App::CMS>, both of which subclass I<MT> to handle application requests.

=head1 USAGE

I<MT> has the following interface. On failure, all methods return C<undef>
and set the I<errstr> for the object or class (depending on whether the
method is an object or class method, respectively); look below at the section
L<ERROR HANDLING> for more information.

=head2 MT->new( %args )

Constructs a new I<MT> instance and returns that object. Returns C<undef>
on failure.

I<new> will also read your F<mt.cfg> file (provided that it can find it--if
you find that it can't, take a look at the I<Config> directive, below). It
will also initialize the chosen object driver; the default is the C<DBM>
object driver.

I<%args> can contain:

=over 4

=item * Config

Path to the F<mt.cfg> file.

If you do not specify a path, I<MT> will try to find your F<mt.cfg> file
in the current working directory.

=back

=head2 $mt->rebuild( %args )

Rebuilds your entire blog, indexes and archives; or some subset of your blog,
as specified in the arguments.

I<%args> can contain:

=over 4

=item * Blog

An I<MT::Blog> object corresponding to the blog that you would like to
rebuild.

Either this or C<BlogID> is required.

=item * BlogID

The ID of the blog that you would like to rebuild.

Either this or C<Blog> is required.

=item * ArchiveType

The archive type that you would like to rebuild. This should be one of the
following values: C<Individual>, C<Daily>, C<Weekly>, C<Monthly>, or
C<Category>.

This argument is optional; if not provided, all archive types will be rebuilt.

=item * EntryCallback

A callback that will be called for each entry that is rebuilt. If provided,
the value should be a subroutine reference; the subroutine will be handed
the I<MT::Entry> object for the entry that is about to be rebuilt. You could
use this to keep a running log of which entry is being rebuilt, for example:

    $mt->rebuild(
              BlogID => $blog_id,
              EntryCallback => sub { print $_[0]->title, "\n" },
          );

Or to provide a status indicator:

    use MT::Entry;
    my $total = MT::Entry->count({ blog_id => $blog_id });
    my $i = 0;
    local $| = 1;
    $mt->rebuild(
              BlogID => $blog_id,
              EntryCallback => sub { printf "%d/%d\r", ++$i, $total },
          );
    print "\n";

This argument is optional; by default no callbacks are executed.

=item * NoIndexes

By default I<rebuild> will rebuild the index templates after rebuilding all
of the entries; if you do not want to rebuild the index templates, set the
value for this argument to a true value.

This argument is optional.

=item * Limit

Limit the number of entries to be rebuilt to the last C<N> entries in the
blog. For example, if you set this to C<20> and do not provide an offset (see
L<Offset>, below), the 20 most recent entries in the blog will be rebuilt.

This is only useful if you are rebuilding C<Individual> archives.

This argument is optional; by default all entries will be rebuilt.

=item * Offset

When used with C<Limit>, specifies the entry at which to start rebuilding
your individual entry archives. For example, if you set this to C<10>, and
set a C<Limit> of C<5> (see L<Limit>, above), entries 10-14 (inclusive) will
be rebuilt. The offset starts at C<0>, and the ordering is reverse
chronological.

This is only useful if you are rebuilding C<Individual> archives, and if you
are using C<Limit>.

This argument is optional; by default all entries will be rebuilt, starting
at the first entry.

=back

=head2 $mt->rebuild_entry( %args )

Rebuilds a particular entry in your blog (and its dependencies, if specified).

I<%args> can contain:

=over 4

=item * Entry

An I<MT::Entry> object corresponding to the object you would like to rebuild.

This argument is required.

=item * Blog

An I<MT::Blog> object corresponding to the blog to which the I<Entry> belongs.

This argument is optional; if not provided, the I<MT::Blog> object will be
loaded in I<rebuild_entry> from the I<$entry-E<gt>blog_id> column of the
I<MT::Entry> object passed in. If you already have the I<MT::Blog> object
loaded, however, it makes sense to pass it in yourself, as it will skip one
small step in I<rebuild_entry> (loading the object).

=item * BuildDependencies

Saving an entry can have effects on other entries; so after saving, it is
often necessary to rebuild other entries, to reflect the changes onto all
of the affected archive pages, indexes, etc.

If you supply this parameter with a true value, I<rebuild_indexes> will
rebuild: the archives for the next and previous entries, chronologically;
all of the index templates; the archives for the next and previous daily,
weekly, and monthly archives.

=item * OldPrevious, OldNext

TBD

=item * NoStatic

TBD

=back

=head2 $mt->rebuild_indexes( %args )

Rebuilds all of the index templates in your blog, or just one, if you use
the I<Template> argument (below). Only rebuilds templates that are set to
be rebuilt automatically, unless you use the I<Force> (below).

I<%args> can contain:

=over 4

=item * Blog

An I<MT::Blog> object corresponding to the blog whose indexes you would like
to rebuild.

Either this or C<BlogID> is required.

=item * BlogID

The ID of the blog whose indexes you would like to rebuild.

Either this or C<Blog> is required.

=item * Template

An I<MT::Template> object specifying the index template to rebuild; if you use
this argument, I<only> this index template will be rebuilt.

Note that if the template that you specify here is set to not rebuild
automatically, you I<must> specify the I<Force> argument in order to force it
to be rebuilt.

=item * Force

A boolean flag specifying whether or not to rebuild index templates who have
been marked not to be rebuilt automatically.

The default is C<0> (do not rebuild such templates).

=back

=head2 $mt->ping( %args )

Sends all configured XML-RPC pings as a way of notifying other community
sites that your blog has been updated.

I<%args> can contain:

=over 4

=item * Blog

An I<MT::Blog> object corresponding to the blog for which you would like to
send the pings.

Either this or C<BlogID> is required.

=item * BlogID

The ID of the blog for which you would like to send the pings.

Either this or C<Blog> is required.

=back

=head2 $mt->set_language($tag)

Loads the localization plugin for the language specified by I<$tag>, which
should be a valid and supported language tag--see I<supported_languages> to
obtain a list of supported languages.

The language is set on a global level, and affects error messages and all
text in the administration system.

This method can be called as either a class method or an object method; in
other words,

    MT->set_language($tag)

will also work. However, the setting will still be global--it will not be
specified to the I<$mt> object.

The default setting--set when I<MT::new> is called--is U.S. English. If a
I<DefaultLanguage> is set in F<mt.cfg>, the default is then set to that
language.

=head2 $mt->translate($str)

Translates I<$str> into the currently-set language (set by I<set_language>),
and returns the translated string.

=head2 $mt->current_language

Returns the language tag for the currently-set language.

=head2 MT->supported_languages

Returns a reference to an associative array mapping language tags to their
proper names. For example:

    use MT;
    my $langs = MT->supported_languages;
    print map { $_ . " => " . $langs->{$_} . "\n" } keys %$langs;

=head2 MT->add_plugin($plugin)

Adds the plugin described by $plugin to the list of plugins displayed
on the welcome page. The argument should be an object of the
I<MT::Plugin> class.

=head2 MT->add_plugin_action($where, $action_link, $link_text)

* EXPERIMENTAL *

Adds a link to the given plugin action from the location specified by
$where. This allows plugins to create actions that apply to, for
example, the entry which the user is editing. The type of object the
user was editing, and its ID, are passed as parameters.

Values that are used from  the $where parameter are as follows:

=over 4

=item * list_entries

=item * list_commenters

=item * list_comments

=item * <type>
(Where <type> is any object that the user can already edit, such as
'entry,' 'comment,' 'commenter,' 'blog,' etc.)

=back

The C<$where> value will be passed to the given action_link as a CGI
parameter called C<from>. For example, on the list_entries page, a
link will appear to:

    <action_link>&from=list_entries

If the $where is a single-item page, such as an entry-editing page,
then the action_link will also receive a CGI parameter C<id> whose
value is the ID of the object under consideration:

    <action_link>&from=entry&id=<entry-id>

Note that the link is always formed by appending an ampersand. Thus,
if your $action_link is simply the name of a CGI script, such as
my-plugin.cgi, you'll want to append a '?' to the argument you pass:

    MT->add_plugin_action('entry', 'my-plugin.cgi?', \
                          'Touch this entry with MyPlugin')

Finally, the $link_text parameter specifies the text of the link; this
value will be wrapped in E<lt>a> tags that point to the $action_link.

=head2 MT->add_text_filter($key, \%options)

Adds a text filter with the short name I<$key> and the options in
I<\%options>.

The text filter will be added to MT's list of text filtering options in
the new/edit entry screen, and will be used for filtering all of the entry
fields, if the user has enabled filtering for those fields in the template
(for example, by default the entry body and extended text are both run
through the filter, but the excerpt is not).

I<$key> should be a lower-case identifier containing only
alphanumerics and C<_> (that is, matching C</\w+/>). Since I<$key> is
stored as the filter name on a per-entry basis, it B<should not change>.
(In other words, don't call if I<foo> in one version and I<foo_bar> in
the next, if the filter does the same thing in each version.)

The flip side of this, though, is that if your filter acts differently
from one version to the next, you B<should> change I<$key>, and you
should also change the filename of your plugin, so that the old
implementation--which may be associated with all of the entries in the user's
system--still works as usual. For example, if your C<foo> plugin changes
semantics drastically so that paragraph breaks are represented as two
C<E<lt>br /E<gt>> tags, rather than C<E<lt>pE<gt>> tags, you should change
the key of the new version to C<foo_2> (for example), and the filename to
F<foo_2.pl>.

I<%options> can contain:

=over 4

=item * label

The short-but-descriptive label for the filter. This will be displayed in
the Movable Type UI as the name of the text filter.

=item * on_format

A reference to a subroutine that will be executed to filter a string of
text. The subroutine will always receive one argument, the string of text to
filter, and should return the filtered string. In some cases--for example,
when called while building a template--the subroutine will receive a
second argument, the I<MT::Template::Context> object handling the build.

See the example below.

=item * docs

The URL (or filename) of a document containing documentation on your filter.
This will be displayed in a popup window when the user selects your filter
on the New/Edit Entry screen, then clicks the Help link (C<(?)>).

If the value is a full URL (starting with C<http://>), the popup window
will open with that URL; otherwise, it is treated as a filename, assumed to
be in the user's F<docs> folder.

=back

Here's an example of adding a text filter for Wiki formatting, using the
I<Text::WikiFormat> CPAN module:

    MT->add_text_filter(wiki => {
        label => 'Wiki',
        on_format => sub {
            require Text::WikiFormat;
            Text::WikiFormat::format($_[0]);
        },
        docs => 'http://www.foo.com/mt/wiki.html',
    });

=head2 MT->apply_text_filters($str, \@filters)

Applies the set of filters I<\@filters> to the string I<$str> and returns
the result (the filtered string).

I<\@filters> should be a reference to an array of filter keynames--these
are the short names passed in as the first argument to I<add_text_filter>.
I<$str> should be a scalar string to be filtered.

If one of the filters listed in I<\@filters> is not found in the list of
registered filters (that is, filters added through I<add_text_filter>),
it will be skipped silently. Filters are executed in the order in which they
appear in I<\@filters>.

As it turns out, the I<MT::Entry::text_filters> method returns a reference
to the list of text filters to be used for that entry. So, for example, to
use this method to apply filters to the main entry text for an entry
I<$entry>, you would use

    my $out = MT->apply_text_filters($entry->text, $entry->text_filters);

=head2 MT->VERSION

Returns the version of MT (including any beta/alpha designations).

=head2 MT->version_number

Returns the numeric version of MT (without any beta/alpha designations).
For example, if I<VERSION> returned C<2.5b1>, I<version_number> would
return C<2.5>.

=head1 ERROR HANDLING

On an error, all of the above methods return C<undef>, and the error message
can be obtained by calling the method I<errstr> on the class or the object
(depending on whether the method called was a class method or an instance
method).

For example, called on a class name:

    my $mt = MT->new or die MT->errstr;

Or, called on an object:

    $mt->rebuild(BlogID => $blog_id)
        or die $mt->errstr;

=head1 CALLBACKS

Movable Type has a variety of hook points at which a plugin can attach
a callback. The context and calling conventions of each one are
documented here.

In each case, the first parameter is an MT::ErrorHandler object which
can be used to pass error information back to the caller.

The app-level callbacks related to rebuilding are documented
below. The specific apps document the callbacks which they invoke.

=over 4

=item BuildFileFilter

This filter gives plugins the chance to determine whether a given file
should be rebuilt as part of a given rebuild event.

A BuildFileFilter callback has the following signature:

    sub build_file_filter($eh, %args)
    {
        ...
        return <boolean>;
    }

As with other callback funcions, the first parameter is an
C<MT::ErrorHandler> object. This can be used by the callback to
propagate an error message to the surrounding context.

The C<%args> parameters identify the page to be built. See
L<MT::FileInfo> for more information on how a page is determined by
these parameters. Elements in C<%args> are as follows:

=over 4

=item C<Context>

Holds the template context that has been constructed for building (see
C<MT::Template::Context>).

=item C<ArchiveType> 

The archive type of the file, usually one of C<'Index'>,
C<'Individual'>, C<'Category'>, C<'Daily'>, C<'Monthly'>, or
C<'Weekly'>.

=item C<Templatemap>

An C<MT::TemplateMap> object; this singles out which template is being
built, and the filesystem path of the file to be written.

=item C<Blog>

The C<MT::Blog> object representing the blog whose pages are being
rebuilt.

=item C<Entry>

In the case of an individual archive page, this points to the
C<MT::Entry> object whose page is being rebuilt. In the case of an
archive page other than an individual page, this parameter is not
necessarily undefined. It is best to rely on the C<$at> parameter to
determine whether a single entry is on deck to be built.

=item C<PeriodStart> 

In the case of a date-based archive page, this is a timestamp at the
beginning of the period from which entries will be included on this
page, in Movable Type's standard 14-digit "timestamp" format. For
example, if the page is a Daily archive for April 17, 1796, this value
would be 17960417000000. If the page were a Monthly archive for March,
2003, C<$start> would be 20030301000000. Again, this parameter may be
defined even when the page on deck is not a date-based archive page.

=item C<Category>

In the case of a Category archive, this parameter identifies the
category which will be built on the page.

=back

=item BuildFile

BuildFile callbacks are invoked just after a file has been built.

    sub build_file($eh, %args)
    {
    }

Parameters in %args are as with BuildFileFilter. There is one
additional key-value pair, C<FileInfo>, an C<MT::FileInfo> object which
contains information about the file. See L<MT::FileInfo> for more
information about what a C<MT::FileInfo> contains. Chief amongst all
the members of C<MT::FileInfo>, for these purposes, will be the
C<virtual> member. This is a boolean value which will be false if a
page was actually created on disk for this "page," and false if no
page was created (because the corresponding template is set to be
built dynamically).

=back

=head1 LICENSE

Please see the file F<LICENSE> in the Movable Type distribution.

=head1 AUTHOR & COPYRIGHT

Except where otherwise noted, MT is Copyright 2001-2004 Six Apart.
ben@movabletype.org, and Mena Trott, mena@movabletype.org. All rights
reserved.

=cut
