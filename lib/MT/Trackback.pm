# Copyright 2001-2004 Six Apart. This code cannot be redistributed without
# permission from www.movabletype.org.
#
# $Id: Trackback.pm,v 1.7 2004/04/29 02:42:57 ezra Exp $

package MT::Trackback;
use strict;

use MT::Object;
@MT::Trackback::ISA = qw( MT::Object );
__PACKAGE__->install_properties({
    columns => [
        'id', 'blog_id', 'title', 'description', 'rss_file', 'url',
        'entry_id', 'category_id', 'is_disabled', 'passphrase',
    ],
    indexes => {
        blog_id => 1,
        entry_id => 1,
        category_id => 1,
        created_on => 1,
    },
    audit => 1,
    datasource => 'trackback',
    primary_key => 'id',
});

sub remove {
    my $tb = shift;
    require MT::TBPing;
    my @pings = MT::TBPing->load({ tb_id => $tb->id });
    for my $ping (@pings) {
        $ping->remove;
    }
    $tb->SUPER::remove;
}

1;
