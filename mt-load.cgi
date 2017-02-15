#!/usr/bin/perl -w

# Copyright 2001-2004 Six Apart. This code cannot be redistributed without
# permission from www.movabletype.org.
#
# $Id: mt-load-ja.cgi,v 1.3 2004/12/22 01:52:03 sekine Exp $
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

local $| = 1;

print "Content-Type: text/html\n\n";
print <<HTML unless (grep {$_ eq '--nostyle' } @ARGV);

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<meta http-equiv="content-language" content="ja" />
	
	<title>Movable Type システムの初期設定 [mt-load.cgi]</title>
	
	<style type=\"text/css\">
		<!--
		
			body {
				font-family : Trebuchet MS, Tahoma, Verdana, Arial, Helvetica, Sans Serif;
				font-size : smaller;
				padding-top : 0px;
				padding-left : 0px;
				margin : 0px;
				padding-bottom : 40px;
				width : 80%;
				border-right : 1px dotted #8faebe;
			}
			
			h1 {
				background : #8faebe;
				font-size: large;
				color : white;
				padding : 10px;
				margin-top : 0px;
				margin-bottom : 20px;
				text-align : center;
			}
			
			h2 {
				color: #fff;
				font-size: small;
				background : #8faebe;
				padding : 5px 10px 5px 10px;
				margin-top : 30px;
				margin-left : 40px;
				margin-right : 40px;
			}
			
			h3 {
				color: #333;
				font-size: small;
				margin-left : 40px;
				margin-bottom : 0px;
				padding-left : 20px;
			}
	
			p {
				padding-left : 20px;
				margin-left : 40px;
				margin-right : 60px;
				color : #666;
			}
			
			ul {
				padding-left : 40px;
				margin-left : 40px;
			}
			
			code {
				font-size : small;
			}
			.info {
				margin-left : 60px;
				margin-right : 60px;
				padding : 20px;
				border : 1px solid #666;
				background : #eaf2ff;
				color : black;
			}
		
			.alert {
				margin-left : 60px;
				margin-right : 60px;
				padding : 20px;
				border : 1px solid #666;
				background : #ff9;
				color : black;
			}
			

			.ready {
				color: #fff;
				background-color: #9C6;
			}

			.bad {
				padding-top : 0px;
				margin-top : 4px;
				border-left : 1px solid red;
				padding-left : 10px;
				margin-left : 60px;
			}
			
			.good {
				color: #93b06b;
				padding-top : 0px;
				margin-top : 0px;
			}
		
		//-->
	</style>

</head>

<body>

<h1>Movable Type システムの初期設定 [mt-load.cgi]</h1>

<p class="info">設定の間に問題が発生した場合は、表示を参考に修正してください。</p>

<h2>Movable Typeのシステム設定</h2>

HTML


use File::Spec;

eval {

my $tmpl_list;
eval { $tmpl_list = require 'MT/default-templates.pl' };
die "デフォルト・テンプレート・ファイル「default-templates.pl」が見付かりません。\n" .
    "エラー： $@\n"
    if $@ || !$tmpl_list || ref($tmpl_list) ne 'ARRAY' || !@$tmpl_list;

print "<h3>Movable Type の初期データをシステムに読み込んでいます...</h3>\n";

require MT;
my $mt = MT->new( Config => $MT_DIR . 'mt.cfg', Directory => $MT_DIR )
    or die MT->errstr;

if ($mt->{cfg}->ObjectDriver =~ /^DBI::(.*)$/) {
    my $type = $1;
    my $dbh = MT::Object->driver->{dbh};
    my $schema = File::Spec->catfile($MT_DIR, 'schemas', $type . '.dump');
    open FH, $schema or die "<p class=\"bad\">データベース・スキーマ・ファイル'$schema'を開くことができません: $!</p>";
    my $ddl;
    { local $/; $ddl = <FH> }
    close FH;
    my @stmts = split /;/, $ddl;
    print "<h3>データベース・スキーマを読み込んでいます...</h3>\n\n";
    for my $stmt (@stmts) {
        $stmt =~ s!^\s*!!;
        $stmt =~ s!\s*$!!;
        next unless $stmt =~ /\S/;
        $dbh->do($stmt) or die $dbh->errstr;
    }
}

use MT::Author qw(AUTHOR COMMENTER);
require MT::Blog;

## First check if there are any authors or blogs currently--if there
## are, don't run the rest of the script, because we don't want to add
## the default author back in (hack).
if (MT::Author->count || MT::Blog->count) {
    print <<MSG, security_notice();

<h2>すでに設定済みのようです!</h2>

<p class="bad">あなたのデータベースは既にmt-load.cgiで初期化されているようです。このスクリプトを再び実行すると、セキュリティ上の問題が発生するかもしれませんので、これ以上、実行しません。</p>

MSG
    exit;
}

print "<h3>ウェブログを設定しています...</h3>\n";
my $blog = MT::Blog->new;
$blog->name('First Weblog');
$blog->archive_type('Individual,Monthly,Category');
$blog->archive_type_preferred('Individual');
$blog->days_on_index(7);
$blog->words_in_excerpt(40);
$blog->file_extension('html');
$blog->convert_paras(1);
$blog->convert_paras_comments(1);
$blog->sanitize_spec(0);
$blog->allow_unreg_comments(1);
$blog->moderate_unreg_comments(1);
$blog->ping_weblogs(0);
$blog->ping_blogs(0);
$blog->ping_technorati(0);
$blog->server_offset(9);
$blog->allow_reg_comments(1);
$blog->allow_comments_default(1);
$blog->language('jp');
$blog->sort_order_posts('descend');
$blog->sort_order_comments('ascend');
$blog->status_default(1);
$blog->custom_dynamic_templates('none');
$blog->children_modified_on('20040101000000');
$blog->save or die $blog->errstr;

print "<h3>投稿者を設定しています...</h3>";
my $author = MT::Author->new;
$author->name('Melody');
$author->type(AUTHOR);
$author->set_password('Nelson');
$author->email('');
$author->can_create_blog(1);
$author->can_view_log(1);
$author->preferred_language('ja');
$author->save or die $author->errstr;

print "<h3>ユーザーの権限を設定しています...</h3>\n";
require MT::Permission;
my $perms = MT::Permission->new;
$perms->author_id($author->id);
$perms->blog_id($blog->id);
$perms->set_full_permissions;
$perms->save or die $perms->errstr;

print "<h3>テンプレートを設定しています...</h3>\n";
require MT::Template;

my @arch_tmpl;
for my $val (@$tmpl_list) {
    $val->{name} = $mt->translate($val->{name});
    $val->{text} = $mt->translate_templatized($val->{text});
    my $obj = MT::Template->new;
    $obj->build_dynamic(0);
    $obj->set_values($val);
    $obj->blog_id($blog->id);
    $obj->save or die $obj->errstr;
    if ($val->{type} eq 'archive' || $val->{type} eq 'individual' ||
        $val->{type} eq 'category') {
        push @arch_tmpl, $obj;
    }
}

print "<h3>テンプレートをウェブログのアーカイブ種別ごとに設定しています...</h3>\n";
require MT::TemplateMap;

for my $tmpl (@arch_tmpl) {
    my(@at);
    if ($tmpl->type eq 'archive') {
        @at = qw( Daily Weekly Monthly );
    } elsif ($tmpl->type eq 'category') {
        @at = qw( Category );
    } elsif ($tmpl->type eq 'individual') {
        @at = qw( Individual );
    }
    for my $at (@at) {
        print "<p class=\"good\">テンプレートID'", $tmpl->id, "'を'$at'に設定</p>\n";
        my $map = MT::TemplateMap->new;
        $map->archive_type($at);
        $map->is_preferred(1);
        $map->template_id($tmpl->id);
        $map->blog_id($tmpl->blog_id);
        $map->save
            or die "設定に失敗しました: ", $map->errstr;
    }
}

};
if ($@) {
    print <<HTML;

<p class="bad">データの設定中に以下のエラーが発生しました:</p>

<p class="alert">$@</p>

HTML
} else {
    print <<HTML, security_notice();

	<h2 class="ready">システムの設定、初期化が完了しました。</h2>

	<p>引き続き、インストール手順に従って Movable Type の設定を行ってください。</p>

HTML
}


sub security_notice {
    return <<TEXT;
    
<h2>重要</h2>

<p class="info">必ず、ウェブサーバから<strong><code>mt-load.cgi</code>を削除</strong>してください</p>

<p class="alert"><strong><code>mt-load.cgi</code>を削除しない場合、再度初期化されるなど、重大なセキュリティ上のリスクになるかもしれません。</strong></p>
TEXT
}


print "</body>\n\n</html>\n";
