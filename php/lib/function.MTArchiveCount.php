<?php
function smarty_function_MTArchiveCount($args, &$ctx) {
    if ($ctx->stash('inside_mt_categories')) {
        return $ctx->tag('MTCategoryCount', $args);
    } else {
        return $ctx->stash('archive_count');
    }
}
/*
sub _hdlr_archive_count {
    my $ctx = $_[0];
    if ($ctx->{inside_mt_categories}) {
        return _hdlr_category_count($ctx);
    } elsif (my $count = $ctx->stash('archive_count')) {
        return $count;
    } else {
        my $e = force($_[0]->stash('entries'));
        my @entries = @$e if ref($e) eq 'ARRAY';
        return scalar @entries;
    }
}   
*/
?>
