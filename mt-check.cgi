#!/usr/bin/perl -w

# Copyright 2001-2004 Six Apart Ltd. This code cannot be redistributed without
# permission from www.movabletype.org.
#
# $Id: mt-check-ja.cgi,v 1.1 2004/10/13 13:57:27 hirata Exp $
use strict;

local $|=1;

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

print "Content-Type: text/html\n\n";
print <<HTML;

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<meta http-equiv="content-language" content="en" />
	
	<title>Movable Type システム・チェック [mt-check.cgi]</title>
	
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
			
			.info {
				margin-left : 60px;
				margin-right : 60px;
				padding : 20px;
				border : 1px solid #666;
				background : #eaf2ff;
				color : black;
			}
		
			.alert {
				padding : 15px;
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

<h1>Movable Type システム・チェック [mt-check.cgi]</h1>

<p class="info">Movable Type が動作するために必要な Perl モジュールのインストールについての確認と、設定に関するシステムの情報を表示します。</p>


HTML


my $is_good = 1;

my @REQ = (
    [ 'HTML::Template', 2, 1, 'HTML::Tempalte は Movable Type のすべての機能で必要とされます。' ],

    [ 'Image::Size', 0, 1, 'Image::Size はファイルのアップロード機能を利用するために必要です。アップロードされる画像のサイズを調べるために使われています。' ],

    [ 'File::Spec', 0.8, 1, 'File::Spec はオペレーション・システムに依存しないファイル・アクセスを実現するために必要です。' ],

    [ 'CGI::Cookie', 0, 1, 'CGI::Cookie は Cookie での認証のために必要です。' ],
);

my @DATA = (
    [ 'DB_File', 0, 0, 'DB_File はバークレイ DB\/DB_File を使ってウェブログのデータを管理したい場合に必要です。' ],

    [ 'DBD::mysql', 0, 0, 'DBI と DBD::mysql は MySQL を使ってウェブログのデータを管理したい場合に必要です。' ],

    [ 'DBD::Pg', 0, 0, 'DBI と DBD::Pg は PostgreSQL を使ってデータを管理したい場合に必要です。' ],

    [ 'DBD::SQLite', 0, 0, 'DBI と DBD::SQLite は SQLite を使ってデータを管理したい場合に必要です。' ],
);

my @OPT = (
    [ 'HTML::Entities', 0, 0, 'HTML::Entities はいくつかの文字を変換するために必要です。この機能を使わないように、 mt.cfg に設定することもできます。' ],

    [ 'LWP::UserAgent', 0, 0, 'LWP::UserAgent はトラックバックや更新 Ping を送信するなら必要です。' ],

    [ 'SOAP::Lite', 0.50, 0, 'SOAP::Lite は XML-RPC API や Atom API を利用するときに必要にです。' ],

    [ 'File::Temp', 0, 0, 'File::Temp はファイルをアップロードするときに上書きを行うなら必要です。' ],

    [ 'Image::Magick', 0, 0, 'Image::Magick は画像をアップロードするときに、サムネイル画像を自動的に作成するなら必要です。' ],

    [ 'Storable', 0, 0, 'Storable は、いろいろな方が作った MT プラグインを実行するときに必要になることがあります。'],

    [ 'Crypt::DSA', 0, 0, 'Crypt::DSA がインストールされていると、コメント登録機能を利用するときに、TypeKey を利用したサイン・インの動作が高速になります。'],

    [ 'MIME::Base64', 0, 0, 'MIME::Base64 はコメント登録機能を利用するために必要です。'],

    [ 'XML::Atom', 0, 0, 'XML::Atom は Atom API を利用するときに必要です。'],
);

use Cwd;
my $cwd = '';
{
    my($bad);
    local $SIG{__WARN__} = sub { $bad++ };
    eval { $cwd = Cwd::getcwd() };
    if ($bad || $@) {
        eval { $cwd = Cwd::cwd() };
        if ($@ && $@ !~ /Insecure \$ENV{PATH}/) {
            die $@;
        }
    }
}

my $ver = $^V ? join('.', unpack 'C*', $^V) : $];
print <<INFO;
<h2>システムの情報:</h2>
<ul>
	<li><strong>CGI が動作しているディレクトリ:</strong> <code>$cwd</code></li>
	<li><strong>オペレーション・システム:</strong> $^O</li>
	<li><strong>Perl のバージョン:</strong> <code>$ver</code></li>
INFO

## Try to create a new file in the current working directory. This
## isn't a perfect test for running under cgiwrap/suexec, but it
## is a pretty good test.
my $TMP = "test$$.tmp";
local *FH;
if (open(FH, ">$TMP")) {
    print "	<li>\(おそらく\) cgiwrap もしくは suexec が有効になっています</li>\n";
    unlink($TMP);
}

print "\n\n</ul>\n";

exit if $ENV{QUERY_STRING} && $ENV{QUERY_STRING} eq 'sys-check';

use Text::Wrap;
$Text::Wrap::columns = 72;

for my $list (\@REQ, \@DATA, \@OPT) {
    my $data = ($list == \@DATA);
    my $req = ($list == \@REQ);
    printf "<h2>確認:  %s モジュール:</h2>\n\t<div>\n", $req ? "必須" :
        $data ? "データ管理" : "推奨";
    if (!$req && !$data) {
        print <<MSG;
		<p class="info">以下のモジュールはインストールすることを <strong>推奨</strong> します。なくても動作しますが、関連する機能を利用するためにはインストールしておく必要があります。 </p>

MSG
    }
    if ($data) {
        print <<MSG;
		<p class="info">以下のモジュールは Movable Type がデータの保管、管理のために利用します。Movable Type を利用するためには、以下のモジュールのうち <strong>少なくとも一つ</strong> はインストールされている必要があります。</p>

MSG
    }
    my $got_one_data = 0;
    for my $ref (@$list) {
        my($mod, $ver, $req, $desc) = @$ref;
        print "    <h3>$mod" .
            ($ver ? " (version &gt;= $ver)" : "") . "</h3>";
        eval("use $mod" . ($ver ? " $ver;" : ";"));
        if ($@) {
            $is_good = 0 if $req;
            my $msg = $ver ?
                      "<p class=\"bad\">$mod がインストールされていないか、もしくは" .
                      "バージョンが古い、もしくは、$mod を" . 
		      "動作させるために必要なモジュールがインストールされていません。. ":
                      "<p class=\"bad\">サーバには、 $mod がインストールされていない、もしくは、" . 
		      "動作させるために必要なモジュールが" . 
		      "インストールされていません。";
            $msg   .= $desc .
                      "$mod をインストールするのであれば、インストールの説明を" .
                      "参考にしてください。</p>\n\n";
            print wrap("        ", "        ", $msg), "\n\n";
        } else {
            print "<p class=\"good\">サーバには $mod がインストールされていました。\(バージョン:  @{[ $mod->VERSION ]}).</p>\n\n";
            $got_one_data = 1 if $data;
        }
    }
    $is_good &= $got_one_data if $data;
    print "\n\t</div>\n\n";
}

if ($is_good) {
    print <<HTML;
    
	<h2 class="ready">Movable Type のシステム・チェックは無事に完了しました</h2>

	<p><strong>準備が整いました!</strong> サーバには必要なモジュールがすべて揃っています。追加のモジュールのインストールは必要ありません。インストールの説明に従って、次の手順に進んでください。 <!-- もし、初めて Movable Type をインストールするのであれば、 <a href="./mt-load.cgi">mt-load.cgi</a> を実行する準備が整っています。実行後に削除するのを忘れないでください。 --> </p>

</div>


HTML
}

print "</body>\n\n</html>\n";
