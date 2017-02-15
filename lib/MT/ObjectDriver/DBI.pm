# Copyright 2001-2004 Six Apart. This code cannot be redistributed without
# permission from www.movabletype.org.
#
# $Id: DBI.pm,v 1.17 2004/09/09 00:27:24 ezra Exp $

package MT::ObjectDriver::DBI;
use strict;

use DBI;

use MT::Util qw( offset_time_list );
use MT::ObjectDriver;
@MT::ObjectDriver::DBI::ISA = qw( MT::ObjectDriver );

sub generate_id { undef }
sub fetch_id { undef }
sub ts2db { $_[1] }
sub db2ts { $_[1] }

my %Date_Cols = map { $_ => 1 } qw( created_on modified_on children_modified_on );
sub is_date_col { $Date_Cols{$_[1]} }
sub date_cols { keys %Date_Cols }

# Override in DB Driver to pass correct attributes to bind_param call
sub bind_param_attributes { return undef; }

sub on_load_complete { }

sub load_iter {
    my $driver = shift;
    $driver->run_callbacks($_[0] . '::pre_load', \@_);
    my($class, $terms, $args) = @_;
    my($tbl, $sql, $bind) =
        $driver->_prepare_from_where($class, $terms, $args);
    my(%rec, @bind, @cols);
    my $cols = $class->column_names;
    for my $col (@$cols) {
        push @cols, $col;
        push @bind, \$rec{$col};
    }
    my $tmp = "select ";
    $tmp .= "distinct " if $args->{join} && $args->{join}[3]{unique};
    $tmp .= join(', ', map "${tbl}_$_", @cols) . "\n";
    $sql = $tmp . $sql;
    my $dbh = $driver->{dbh};
    my $sth = $dbh->prepare($sql) or return sub { $driver->error($dbh->errstr) };
    $sth->execute(@$bind) or return sub { $driver->error($sth->errstr) };
    $sth->bind_columns(undef, @bind);
    sub {
        unless ($sth->fetch) {
            $sth->finish;
            $driver->on_load_complete($sth);
            return;
        }
        my $obj = $class->new;
        ## Convert DB timestamp format to our timestamp format.
        for my $col ($driver->date_cols) {
            $rec{$col} = $driver->db2ts($rec{$col}) if $rec{$col};
        }
        $obj->set_values(\%rec);
	$driver->run_callbacks($class . '::post_load', \@_, $obj);
        $obj;
    };
}

sub load {
    my $driver = shift;
    $driver->run_callbacks($_[0] . '::pre_load', \@_);
    my($class, $terms, $args) = @_;
    my($tbl, $sql, $bind) =
        $driver->_prepare_from_where($class, $terms, $args);
    my(%rec, @bind, @cols);
    my $cols = $class->column_names;
    for my $col (@$cols) {
        push @cols, $col;
        push @bind, \$rec{$col};
    }
    my $tmp = "select ";
    $tmp .= "distinct " if $args->{join} && $args->{join}[3]{unique};
    $tmp .= join(', ', map "${tbl}_$_", @cols) . "\n";
    $sql = $tmp . $sql;
    my $dbh = $driver->{dbh};
    my $sth = $dbh->prepare($sql) || return $driver->error("Loading data failed with SQL error " . $dbh->errstr);
    my $result = $sth->execute(@$bind)
	|| return $driver->error("Loading data failed with SQL error " .
				 $sth->errstr);
    $sth->bind_columns(undef, @bind); 
    my @objs;
    while ($sth->fetch) {
        my $obj = $class->new;
        ## Convert DB timestamp format to our timestamp format.
        for my $col ($driver->date_cols) {
            $rec{$col} = $driver->db2ts($rec{$col}) if $rec{$col};
        }
        $obj->set_values(\%rec);
	$driver->run_callbacks($class . '::post_load', \@_, $obj);
        return $obj unless wantarray;
        push @objs, $obj;
    }
    $sth->finish;
    $driver->on_load_complete($sth);
    @objs;
}

sub count {
    my $driver = shift;
    my($class, $terms, $args) = @_;
    my($tbl, $sql, $bind) = $driver->_prepare_from_where($class, $terms, $args);
    ## Remove any order by clauses, because they will cause errors in
    ## some drivers (and they're not necessary)
    $sql =~ s/order by \w+ (?:asc|desc)//;
    $sql = "select count(*)\n" . $sql;
    my $dbh = $driver->{dbh};
    my $sth = $dbh->prepare($sql) or return;
    $sth->execute(@$bind) or return $driver->error("Count $class failed on SQL error " . $sth->errstr);
    $sth->bind_columns(undef, \my($count));
    $sth->fetch or return;
    $sth->finish;
    $driver->on_load_complete($sth);
    $count;
}

sub count_group_by {
    my $driver = shift;
    my ($class, $terms, $args) = @_;
    my($tbl, $sql, $bind) = $driver->_prepare_from_where($class, $terms,
					       {%$args, suppress_order_by => 1});
    ## Remove any order by clauses, because the _prepare_from_where
    ## routine isn't savvy about function-based order-by clauses (yet)
    $sql =~ s/order\s+by\s+[\w)(]+\s*(?:asc|desc)//;
    my $group_by_terms = (join ", ", @{$args->{group}});
    foreach my $col (@{$class->new()->column_names}) {
	$group_by_terms =~ s/$col/${tbl}_$col/g;
	$args->{sort} =~ s/$col/${tbl}_$col/g;
    }
    $sql = "select count(*), " . $group_by_terms . " " . $sql
	. " group by " . $group_by_terms
	. ($args->{sort} ? " order by " . $args->{sort} : "");
    my $dbh = $driver->{dbh};
    my $sth = $dbh->prepare($sql) or return $driver->error("Prepare failed");
    $sth->execute(@$bind) or return $driver->error("Execute failed");
    my @bindvars = ();
    for (@{$args->{group}}) {
	push @bindvars, \my($var);
    }
    $sth->bind_columns(undef, \my($count), @bindvars);
    sub {
	$sth->fetch or return;
	if (!defined($count)) {
	    $sth->finish;
	    $driver->on_load_complete($sth);
	} else {
	    my @returnvals = map { $$_ } @bindvars;
	    return ($count, @returnvals);
	}
    }
}

sub exists {
    my $driver = shift;
    my($obj) = @_;
    return unless $obj->id;
    my $tbl = $obj->datasource;
    my $sql = "select 1 from mt_$tbl where ${tbl}_id = ?";
    my $dbh = $driver->{dbh};
    my $sth = $dbh->prepare($sql) or return;
    $sth->execute($obj->id)
	or return $driver->error("existence test failed on SQL error " 
				 . $sth->errstr);
    my $exists = $sth->fetch;
    $sth->finish;
    $exists;
}

sub save {
    my $driver = shift;
    my($obj) = @_;
    my $original;
    ($original, $obj) = ($obj, $obj->clone());
    my $class = ref($_[0]);
    $driver->run_callbacks($class . '::pre_save', $obj, $original);
    my $result;
    if ($driver->exists($obj)) {
	$result = $driver->update($obj);
    } else {
	$result = $driver->insert($obj);
    }
    $original->id($obj->id);
    $original->created_on($obj->created_on);
    $original->modified_on($obj->modified_on);
    $driver->run_callbacks($class . '::post_save', $obj);
    return $result;
}

sub insert {
    my $driver = shift;
    my($obj) = @_;
    my $cols = $obj->column_names;
    unless ($obj->id) {
        ## If we don't already have an ID assigned for this object, we
        ## may need to generate one (depending on the underlying DB
        ## driver). If the driver gives us a new ID, we insert that into
        ## the new record; otherwise, we assume that the DB is using an
        ## auto-increment column of some sort, so we don't specify an ID
        ## at all.
        my $id = $driver->generate_id($obj);
        if ($id) {
            $obj->id($id);
        } else {
            $cols = [ grep $_ ne 'id', @$cols ];
        }
    }
    my $tbl = $obj->datasource;
    my $sql = "insert into mt_$tbl\n";
    $sql .= '(' . join(', ', map "${tbl}_$_", @$cols) . ')' . "\n" .
            'values (' . join(', ', ('?') x @$cols) . ')' . "\n";
    if ($obj->properties->{audit}) {
        my $blog_id = $obj->blog_id;
        my @ts = offset_time_list(time, $blog_id);
        my $ts = sprintf '%04d%02d%02d%02d%02d%02d',
            $ts[5]+1900, $ts[4]+1, @ts[3,2,1,0];
        $obj->created_on($ts) unless $obj->created_on;
        $obj->modified_on($ts);
    }
    my $dbh = $driver->{dbh};
    my $sth = $dbh->prepare($sql)
        or return $driver->error($dbh->errstr);
    my $i = 1;
    my $col_defs = $obj->properties->{column_defs};
    for my $col (@$cols) {
        my $val = $obj->column($col);
        my $type = $col_defs->{$col} || 'char';
        if ($type eq 'date' || $driver->is_date_col($col)) {
            $val = $driver->ts2db($val);
        }
        my $attr = $driver->bind_param_attributes($type);

        $sth->bind_param($i++, $val, $attr);
    }
    $sth->execute()
        or return $driver->error("Insertion test failed on SQL error " 
				 . $dbh->errstr);
    $sth->finish;

    ## Now, if we didn't have an object ID, we need to grab the
    ## newly-assigned ID.
    unless ($obj->id) {
        $obj->id($driver->fetch_id($sth));
    }
    1;
}

sub update {
    my $driver = shift;
    my($obj) = @_;
    my $cols = $obj->column_names;
    $cols = [ grep $_ ne 'id', @$cols ];
    my $tbl = $obj->datasource;
    my $sql = "update mt_$tbl set\n";
    $sql .= join(', ', map "${tbl}_$_ = ?", @$cols) . "\n";
    $sql .= "where ${tbl}_id = '" . $obj->id . "'";
    if ($obj->properties->{audit}) {
        my $blog_id = $obj->blog_id;
        my @ts = offset_time_list(time, $blog_id);
        my $ts = sprintf "%04d%02d%02d%02d%02d%02d",
            $ts[5]+1900, $ts[4]+1, @ts[3,2,1,0];
        $obj->modified_on($ts);
    }
    my $dbh = $driver->{dbh};

    my $sth = $dbh->prepare($sql)
        or return $driver->error($dbh->errstr);
    my $i = 1;
    my $col_defs = $obj->properties->{column_defs};
    for my $col (@$cols) {
        my $val = $obj->column($col);
        my $type = $col_defs->{$col} || 'char';
        if ($type eq 'date' || $driver->is_date_col($col)) {
            $val = $driver->ts2db($val);
        }
        my $attr = $driver->bind_param_attributes($type);
        $sth->bind_param($i++, $val, $attr);
    }

    $sth->execute()
        or return $driver->error("Update failed on SQL error " . $dbh->errstr);
    $sth->finish;
    1;
}

sub remove {
    my $driver = shift;
    my($obj) = @_;
    my $class = ref $obj;
    $driver->run_callbacks($class . '::pre_remove', $obj);
    my $id = $obj->id();
    return $driver->error("No such object.") unless defined($id);
    my $tbl = $obj->datasource;
    my $sql = "delete from mt_$tbl where ${tbl}_id = ?";
    my $dbh = $driver->{dbh};
    my $sth = $dbh->prepare($sql)
        or return $driver->error($dbh->errstr);
    $sth->execute($id)
        or return $driver->error("Remove failed on SQL error " . $dbh->errstr);
    $sth->finish;
    $driver->run_callbacks($class . '::post_remove', $obj);
    1;
}

sub remove_all {
    my $driver = shift;
    my($class) = @_;
    $driver->run_callbacks($class . '::pre_remove_all', @_);
    my $sql = "delete from mt_" . $class->datasource;
    my $dbh = $driver->{dbh};
    my $sth = $dbh->prepare($sql)
        or return $driver->error($dbh->errstr);
    $sth->execute
        or return $driver->error("Remove-all failed on SQL error "
				 . $dbh->errstr);
    $sth->finish;
    $driver->run_callbacks($class . '::post_remove_all', @_);
    1;
}

sub DESTROY {
    $_[0]->{dbh}->disconnect if $_[0]->{dbh};
}

sub build_sql {
    my($driver, $class, $terms, $args, $tbl) = @_;
    my(@bind, @terms);
    if ($terms) {
        if (!ref($terms)) {
            return('', [ "${tbl}_id = ?" ], [ $terms ]);
        }
        for my $col (keys %$terms) {
            my $term = '';
            if (ref($terms->{$col}) eq 'ARRAY') {
                if ($args->{range} && $args->{range}{$col}
                    || $args->{range_incl} && $args->{range_incl}{$col}) {
                    my($start, $end) = @{ $terms->{$col} };
                    if ($start) {
                        if ($args->{range}) {
                            $term = "${tbl}_$col > ?";
                        } else {
                            $term = "${tbl}_$col >= ?";
                        }
                        push @bind,
                          $driver->is_date_col($col) ? $driver->ts2db($start) : $start;
                    }
                    $term .= " and " if $start && $end;
                    if ($end) {
                        if ($args->{range}) {
                            $term .= "${tbl}_$col < ?";
                        } else {
                            $term .= "${tbl}_$col <= ?";
                        }
                        push @bind,
                          $driver->is_date_col($col) ? $driver->ts2db($end) : $end;
                    }
                }
            } else {
                $term = "${tbl}_$col = ?";
                push @bind, $driver->is_date_col($col) ?
                    $driver->ts2db($terms->{$col}) : $terms->{$col};
            }
            push @terms, "($term)";
        }
    }
    if (my $sv = $args->{start_val}) {
        my $col = $args->{sort} || $driver->primary_key;
        my $cmp = $args->{direction} eq 'descend' ? '<' : '>';
        push @terms, "(${tbl}_$col $cmp ?)";
        push @bind, $driver->is_date_col($col) ? $driver->ts2db($sv) : $sv;
    }
    my $sql = '';
    unless ($args->{suppress_order_by}) {
	if ($args->{'sort'} || $args->{direction}) {
	    my $order = $args->{'sort'} || 'id';
	    my $dir = $args->{direction} &&
		$args->{direction} eq 'descend' ? 'desc' : 'asc';
	    $sql .= "order by ${tbl}_$order $dir\n";
	}
    }
    ($sql, \@terms, \@bind);
}

1;
