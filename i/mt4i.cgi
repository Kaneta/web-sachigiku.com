#!/usr/bin/perl
##################################################
#
# MovableType用 i-mode変換スクリプト
# 「MT4i」
my $version = "2.0";
# Copyright (C) 太鉄 All rights reserved.
# Special Thanks
#           ヴァリウム男爵 & Tonkey
#
# About MT4i
#  →http://www.hazama.nu/t2o2/mt4i.shtml
# TonkeyさんのTonkey Magic
#  →http://tonkey.mails.ne.jp/
# ヴァリウム男爵の人生迷い箸
#  →http://valium.oops.jp/
#
# -- 言い訳ここから --
# ぶっちゃけ、行き当たりばったりの「動けばいいや」で
# コーディングしてますし、Perlに関しては素人同然なので、
# ソースが汚い＆技術的に未熟な点はご容赦ください。
# -- 言い訳ここまで --
#
##################################################

use strict 'vars';
use strict 'subs';
use CGI;

# 設定読み込み
# Config.plをrequire及び存在確認
eval {require 'mt4ilib/Config.pl'; 1} || die &errorout('"./mt4ilib/Config.pl"が見付かりません。');
my %cfg = Config::Read("./mt4icfg.cgi");

### valium add start
# MT4i対応リンクの前に表示する文字(付けたくない場合は空文字列にする）
my @ainori_str = (
	  "<font color=\"#FFCC33\">&#63862;</font>",	# i-mode および EZWeb
	  "\x1B\$Fu\x0F",								# J-SKY
	  "(MT4i)"										# other
);
# 携帯対応リンクの前に表示する文字(付けたくない場合は空文字列にする）
my @ExitChtmlTrans_Str = (
	  "<font color=\"#FFCC33\">&#63862;</font>",	# i-mode および EZWeb
	  "\x1B\$Fu\x0F",								# J-SKY
	  "(携帯対応)"									# other
);
### valium add end

unshift @INC, $cfg{MT_DIR} . 'lib';
unshift @INC, $cfg{MT_DIR} . 'extlib';

####################
# Encode.pmの有無調査
my $ecd;
eval 'use Encode;';
if($@){
	$ecd = 0;
}else{
	$ecd = 1;
}

####################
# Jcode.pmの有無調査
my $jcnv;
my $jcd;
eval 'use Jcode;';
if($@){
	require 'jcode.pl';
	$jcnv = 'jcode::convert';
	$jcd = 0;
}else{
	$jcnv = 'Jcode::convert';
	$jcd = 1;
}

####################
# User Agent によるキャリア判別
# 参考：http://specters.net/cgipon/labo/c_dist.html
my $ua;
my @user_agent = split(/\//,$ENV{'HTTP_USER_AGENT'});
my $png_flag;
if ($user_agent[0] eq 'ASTEL') {
	# ドットi 用の処理
	$ua = 'other';
} elsif ($user_agent[0] eq 'UP.Browser') {
	# EZweb 旧端末用の処理
	$ua = 'ezweb';
} elsif ($user_agent[0] =~ /^KDDI/) {
	# EZweb WAP2.0 対応端末用の処理
	$ua = 'ezweb';
} elsif ($user_agent[0] eq 'PDXGW') {
	# H" 用の処理
	$ua = 'other';
} elsif ($user_agent[0] eq 'DoCoMo') {
	# i-mode 用の処理
	$ua = 'i-mode';
} elsif ($user_agent[0] eq 'J-PHONE') {
	# J-SKY 用の処理
	$ua = 'j-sky';
	
	# PNGしか表示できない機種はこれだけなので事前にチェックする
	if (($user_agent[2] =~ /^J-DN02/) ||
		($user_agent[2] =~ /^J-P02/) ||
		($user_agent[2] =~ /^J-P03/) ||
		($user_agent[2] =~ /^J-T04/) ||
		($user_agent[2] =~ /^J-SA02/) ||
		($user_agent[2] =~ /^J-SH02/) ||
		($user_agent[2] =~ /^J-SH03/)){
			$png_flag = 1;
	}
} elsif ($user_agent[1] =~ 'DDIPOCKET') {
	# AirH"PHONE用の処理
	$ua = 'i-mode';
} elsif ($user_agent[0] eq 'L-mode') {
	# L-mode 用の処理
	$ua = 'other';
} else {
	# それ以外
	$ua = 'other';
}

####################
# AccessKey用文字列生成
my @nostr;
my @akstr;
for (my $i = 0; $i <= 9; $i++)  {
	$nostr[$i] = "";
	$akstr[$i] = "";
}
### valium add start
my $mt4ilinkstr = $ainori_str[2];
my $ExitChtmlTransStr = $ExitChtmlTrans_Str[2];
### valium add end
if ($cfg{AccessKey} eq "yes") {
	if ($ua eq "i-mode" || $ua eq "ezweb") {
    # i-mode 及び EZweb
		### valium add start
		$mt4ilinkstr = $ainori_str[0];
		$ExitChtmlTransStr = $ExitChtmlTrans_Str[0];
		### valium add end
		for (my $i = 1; $i <= 10; $i++) {
			if ($i < 10) {
				my $code = 63878 + $i;
				$nostr[$i] = "&#$code;";
				$akstr[$i] = ", accesskey=\"$i\"";
			} else {
				$nostr[0] = "&#63888;";
				$akstr[0] = ", accesskey=\"0\"";
			}
		}
	} elsif ($ua eq "j-sky") {
		# J-SKY
		### valium add start
		$mt4ilinkstr = $ainori_str[1];
		$ExitChtmlTransStr = $ExitChtmlTrans_Str[1];
		### valium add end
		$nostr[1] = "\x1B\$F<\x0F";
		$nostr[2] = "\x1B\$F=\x0F";
		$nostr[3] = "\x1B\$F>\x0F";
		$nostr[4] = "\x1B\$F?\x0F";
		$nostr[5] = "\x1B\$F@\x0F";
		$nostr[6] = "\x1B\$FA\x0F";
		$nostr[7] = "\x1B\$FB\x0F";
		$nostr[8] = "\x1B\$FC\x0F";
		$nostr[9] = "\x1B\$FD\x0F";
		$nostr[0] = "\x1B\$FE\x0F";
		for (my $i = 1; $i <= 10; $i++) {
			if ($i < 10) {
				$akstr[$i] = ", directkey=\"$i\" nonumber";
			} else {
				$akstr[0] = ", directkey=\"0\" nonumber";
			}
		}
	}
}

####################
# 引数の取得
my $q = new CGI();

if (!$cfg{Blog_ID}) {
	$cfg{Blog_ID} = $q->param("id");	# blog ID
}
my $mode = $q->param("mode");			# 処理モード
my $no = $q->param("no");				# エントリーNO
my $eid = $q->param("eid");				# エントリーID
my $ref_eid = $q->param("ref_eid");		# 元記事のエントリーID
my $page = $q->param("page");			# ページNO
my $sprtpage = $q->param("sprtpage");	# 分割ページ数
my $sprtbyte = $q->param("sprtbyte");	# ページ分割byte数
my $img = $q->param("img");				# 画像のURL
my $cat = $q->param("cat");				# カテゴリID
my $post_from = $q->param("from");		# 投稿者
my $post_mail = $q->param("mail");		# メール
my $post_text = $q->param("text");		# コメント

my $pw_text = $q->param("pw_text");		# 暗号化パスワード
my $key = $q->param("key");				# 暗号化キー
my $entry_cat = $q->param("entry_cat");					# エントリーのカテゴリー
my $entry_title = $q->param("entry_title");				# エントリーのタイトル
my $entry_text = $q->param("entry_text");				# エントリーの内容
my $entry_text_more = $q->param("entry_text_more");		# エントリーの追記
my $entry_excerpt = $q->param("entry_excerpt");			# エントリーの概要
my $entry_keywords = $q->param("entry_keywords");		# エントリーのキーワード
my $post_status = $q->param("post_status");				# エントリーのステータス
my $allow_comments = $q->param("allow_comments");		# エントリーのコメント許可チェック
my $allow_pings = $q->param("allow_pings");				# エントリーのping許可チェック
my $text_format = $q->param("convert_breaks");			# エントリーのテキストフォーマット
my $entry_created_on = $q->param("entry_created_on");	# エントリーの作成日時

# PerlMagick の有無調査
my $imk = 0;
if ($mode eq 'image' || $mode eq 'img_cut') {
	eval 'use Image::Magick;';

	if ($cfg{ImageAutoReduce} eq "yes"){
		if($@){
			$imk = 0;
		}else{
			$imk = 1;
		}
	}else{
		$imk = 0;
	}
}

my $data;	# 表示文字列用の変数を宣言する

#管理者用暗号化キーをチェック
my $admin_mode;
if (($key ne "")&&(&check_crypt($cfg{AdminPassword}.$cfg{Blog_ID},$key))){
	$admin_mode = 'yes';
}else{
	$admin_mode = 'no';
	$key = "";
}

####################
# mt.cfgの読み込み
require MT;
my $mt = MT->new( Config => $cfg{MT_DIR} . 'mt.cfg', Directory => $cfg{MT_DIR} )
	or die MT->errstr;

####################
# blog IDが指定されていなかった場合はエラー
if (!$cfg{Blog_ID}) {
	$data = "Error：引数にblog IDを指定してください。<br>";
	# blog一覧表示
	$data .= "<br>";
	require MT::Blog;
	my @blogs = MT::Blog->load(undef,
							{unique => 1});

	# ソート
	@blogs = sort {$a->id <=> $b->id} @blogs;
	
	$data .= '<table border="1">';
	$data .= '<tr><th style="color:#FF0000;">blog ID</th><th>blog Name</th><th>Description</th></tr>';
	
	# 表示
	for my $blog (@blogs) {
		my $blog_id = $blog->id;
		my $blog_name = &conv_euc_z2h($blog->name);
		my $blog_description = &conv_euc_z2h($blog->description);
		$data .= "<tr><th style=\"color:#FF0000;\">$blog_id</th><td><a href=\"./$cfg{MyName}?id=$blog_id\">$blog_name</a></td><td>$blog_description</td></tr>";
	}

	$data .= '</table><br><span style="font-weight:bold;">blog ID の指定方法：</span><br>　MT4i.cgi の設定にて "<span style="font-weight:bold;">$blog_id</span>" に上記 <span style="color:#FF0000;font-weight:bold;">blog ID</span> を指定するか、<br>　もしくは上記 <span style="color:#FF0000;font-weight:bold;">blog Name</span> にﾘﾝｸされている URL でｱｸｾｽする。';
	
	&errorout;
	exit;      # exitする
}

####################
# PublishCharsetの取得
my $conv_in;
if (lc $mt->{cfg}->PublishCharset eq lc "Shift_JIS") {
	$conv_in = "sjis";
} elsif (lc $mt->{cfg}->PublishCharset eq lc "ISO-2022-JP") {
	$conv_in = "jis";
} elsif (lc $mt->{cfg}->PublishCharset eq lc "UTF-8") {
	$conv_in = "utf8";
} elsif (lc $mt->{cfg}->PublishCharset eq lc "EUC-JP") {
	$conv_in = "euc";
}

####################
# blog名及び概要の取得
require MT::Blog;
my $blog = MT::Blog->load($cfg{Blog_ID},
					  {unique => 1});

# 不正なblog ID
if (!$blog) {
	$data = "ID '$cfg{Blog_ID}' のblogは存在しません。";
	&errorout;
	exit;      # exitする
}

# blog名、概要、コメント関連設定を変数に格納
my $blog_name = &conv_euc_z2h($blog->name);
my $description = &conv_euc_z2h($blog->description);
my $sort_order_comments = $blog->sort_order_comments;
my $email_new_comments = $blog->email_new_comments;
my $email_new_pings = $blog->email_new_pings;
my $convert_paras = $blog->convert_paras;
my $convert_paras_comments = $blog->convert_paras_comments;

####################
# 引数$modeの判断
if (!$mode)						{ &main }
if ($mode eq 'individual')		{ &individual }
if ($mode eq 'individual_rcm')	{ &individual }
if ($mode eq 'individual_lnk')	{ &individual }
if ($mode eq 'ainori')			{ &individual }
if ($mode eq 'comment')			{ &comment }
if ($mode eq 'comment_rcm')		{ &comment }
if ($mode eq 'comment_lnk')		{ &comment }
if ($mode eq 'image')			{ &image }
if ($mode eq 'img_cut')			{ &image_cut }
if ($mode eq 'postform')		{ &postform }
if ($mode eq 'postform_rcm')	{ &postform }
if ($mode eq 'postform_lnk')	{ &postform }
if ($mode eq 'post')			{ &post }
if ($mode eq 'post_rcm')		{ &post }
if ($mode eq 'post_lnk')		{ &post }
if ($mode eq 'recentcomment')	{ &recent_comment }
if ($mode eq 'trackback')		{ &trackback }


# 管理者用バックドアの表示
if ($cfg{AdminDoor} eq "yes"){
	if ($mode eq 'admindoor')	{ &admindoor }
}

#--- ここから先は管理モードでしか実行できない ---

	if ($admin_mode eq "yes") {
		if ($mode eq 'entryform')				{ &entryform }
		if ($mode eq 'entry')					{ &entry }
		if ($mode eq 'comment_del')				{ &comment_del }
		if ($mode eq 'entry_del')  				{ &entry_del }
		if ($mode eq 'trackback_del')			{ &trackback_del }
		if ($mode eq 'trackback_ipban')			{ &trackback_ipban }
		if ($mode eq 'comment_ipban')			{ &comment_ipban }
		if ($mode eq 'email_comments')			{ &email_comments }
		
		if ($mode eq 'confirm_comment_del')		{ &confirm }
		if ($mode eq 'confirm_entry_del')		{ &confirm }
		if ($mode eq 'confirm_trackback_del')	{ &confirm }
		if ($mode eq 'confirm_trackback_ipban')	{ &confirm }
		if ($mode eq 'confirm_comment_ipban')	{ &confirm }
	}

########################################
# Sub Main - トップページの描画
########################################

sub main {
	if(!$mode && !$page) { $page = 0 }
	if ($cfg{AccessKey} eq "yes" && ($ua eq "i-mode" || $ua eq "j-sky" || $ua eq "ezweb")) {
		# 携帯電話からのアクセスかつアクセスキー有効の場合は$cfg{DispNum}を6以下にする
		if ($cfg{DispNum} > 6) {
			$cfg{DispNum} = 6;
		}
	}
	my $rowid;
	if($page == 0) { $rowid = 0 } else { $rowid = $page * $cfg{DispNum} }
	
	####################
	# 総件数の取得
	my $ttlcnt = &get_ttlcnt;
	
	####################
	# 一覧の取得
	my @entries = &get_entries($rowid, $cfg{DispNum});
	
	# 検索結果が0件の場合はメッセージ表示してSTOP
	if (@entries <= 0) {
		$data = "検索結果が0件です。<br>";
		&errorout;
		exit;      # exitする
	}
	
	# 一覧件数取得（$cfg{DispNum}より少ない可能性がある為）
	my $rowcnt = @entries + 1;
	
	####################
	# 表示文字列生成
	$data .= "<h1 align=\"center\"><font color=\"$cfg{TitleColor}\">";
	if ($cfg{Logo_i} && $cfg{Logo_i}) {
		if ($ua eq 'i-mode') {
			$data .= "<img src=\"$cfg{Logo_i}\" alt=\"$blog_name mobile ver.\">";
		} else {
			$data .= "<img src=\"$cfg{Logo_o}\" alt=\"$blog_name mobile ver.\">";
		}
		$data .= "</font></h1>";
	} else {
		$data .= "$blog_name</font></h1><center>mobile ver.</center>";
	}
	
	# 管理者モード
	if ($admin_mode eq 'yes'){
		$data .= "<h2 align=\"center\"><font color=\"$cfg{TitleColor}\">管理者モード</font></h2>";
	}
	
	if ($cfg{Dscrptn} eq "yes" && $page == 0 && $description) {
		my $tmp_data .= "<hr><center>$description</center>";
		#単なる改行を<br>タグに置換
		#(「ウェブログの説明」に改行が混ざるとauで表示されない不具合への対処)
		$tmp_data=~s/\r\n/<br>/g;
		$tmp_data=~s/\r/<br>/g;
		$tmp_data=~s/\n/<br>/g;
		$data .= $tmp_data;
	}
	$data .= "<hr>";
	
	# カテゴリセレクタ
	$data .= "<center><form action=\"$cfg{MyName}\">";
	if ($key){
		$data .= "<input type=hidden name=\"key\" value=\"$key\">";
	}
	$data .= "<select name=\"cat\">";
	$data .= "<option value=0>すべて";

	my @cat_datas = ();
	require MT::Category;
	my @categories = MT::Category->load({blog_id => $cfg{Blog_ID}},
											{unique => 1});
	for my $category (@categories) {
		my $label;
		
		# カテゴリ名の日本語化を$MTCategoryDescriptionで表示している場合に
		# カテゴリセレクタの内容を置換する
		if ($cfg{CatDescReplace} eq "yes"){
			$label = &conv_euc_z2h($category->description);
		}else{
			$label = &conv_euc_z2h($category->label);
		}
		my $cat_id = $category->id;
		require MT::Entry;
		require MT::Placement;
		# エントリーが1以上のもののみ列挙
		my $count = MT::Entry->count( { blog_id => $cfg{Blog_ID}, status => 2 },
									{ join => [ 'MT::Placement', 'entry_id',
									{ blog_id => $cfg{Blog_ID}, category_id => $cat_id } ] });
		if ($count > 0) {
			if ($cat != 0 && $cat_id == $cat) {
				@cat_datas = (@cat_datas,"$cat_id,$label,$count");
			} else {
				@cat_datas = (@cat_datas,"$cat_id,$label,$count");
			}
		}
	}
	
	if ($cfg{CatDescSort} eq "asc"){
		@cat_datas = sort { (split(/\,/,$a))[1] cmp (split(/\,/,$b))[1] } @cat_datas;
	}elsif ($cfg{CatDescSort} eq "desc"){
		@cat_datas = reverse sort { (split(/\,/,$a))[1] cmp (split(/\,/,$b))[1] } @cat_datas;
	}
	
	for my $cat_data (@cat_datas) {
		my @cd_tmp = split(",", $cat_data);
		
		if ($cat == $cd_tmp[0]){
			$data .= "<option value=$cd_tmp[0] selected>$cd_tmp[1]($cd_tmp[2])";
		}else{
			$data .= "<option value=$cd_tmp[0]>$cd_tmp[1]($cd_tmp[2])";
		}
	}
	$data .= "</select>";
	$data .= "<input type=hidden name=\"id\" value=\"$cfg{Blog_ID}\">";
	$data .= "<input type=submit value=\"選択\"></form></center>";
	$data .= "<hr>";
	
	# 記事本文
	my $i = 0;
	for my $entry (@entries){ # 結果のフェッチと表示
		my $title = &conv_euc_z2h($entry->title);
		$title = "untitled" if($title eq '');
		my $created_on = &conv_euc_z2h(&conv_datetime($entry->created_on));
		my $comment_cnt = $entry->comment_count;
		my $ping_cnt = $entry->ping_count;
		$rowid++;
		$i++;
		my $href = &make_href("individual", $rowid, 0, $entry->id, 0);
		if ($cfg{AccessKey} eq "no" || ($cfg{AccessKey} eq "yes" && $ua ne "i-mode" && $ua ne "ezweb" && $ua ne "j-sky")) {
			$data .= "$rowid.<a href=\"$href\">$title</a>$created_on";
		} else {
			$data .= "$nostr[$i]<a href=\"$href\"$akstr[$i]>$title</a>$created_on";
		}
		if ($comment_cnt > 0 && $cfg{CommentColor} ne 'no'){ #コメント数を一覧に付加
			$data .= "<font color=\"$cfg{CommentColor}\">[$comment_cnt]</font>";
		}
		if ($ping_cnt > 0 && $cfg{TbColor} ne 'no'){ #トラックバック数を一覧に付加
			$data .= "<font color=\"$cfg{TbColor}\">[$ping_cnt]</font>";
		}
		$data .= "<br>";
	}
	
	# 最終ページの算出
	if ($ttlcnt >= $cfg{DispNum}) {
		my $lastpage = int($ttlcnt / $cfg{DispNum});	# int()で小数点以下は切り捨て
		my $amari = $ttlcnt % $cfg{DispNum};			# 余りの算出
		if ($amari > 0) { $lastpage++ }				# あまりがあったら+1
		my $ttl = $lastpage;						# 下のページ数表示用に値取得
		$lastpage--;								# でもページは0から始まってるので-1（なんか間抜け）
		
		# ページ数表示
		my $here = $page + 1;
		$data .= "<center>$here/$ttl</center><hr>";
	
		# 引数用ページ数計算
		my $nextpage = $page + 1;
		my $prevpage = $page - 1;
		
		# 次、前、最初
		if ($rowid < $ttlcnt) {
			my $href = &make_href("", 0, $nextpage, 0, 0);
			if ($page == $lastpage - 1 && $amari > 0) {
				$data .= "$nostr[9]<a href=\"$href\"$akstr[9]>次の$amari件 &gt;</a><br>";
			} else {
				$data .= "$nostr[9]<a href=\"$href\"$akstr[9]>次の$cfg{DispNum}件 &gt;</a><br>";
			}
		}
		$rowid = $rowid - $rowcnt;
		if ($rowid > 0) {
			my $href = &make_href("", 0, $prevpage, 0, 0);
			$data .= "$nostr[7]<a href=\"$href\"$akstr[7]>&lt; 前の$cfg{DispNum}件</a><br>";
		}
		if ($page > 1) {
			my $href = &make_href("", 0, 0, 0, 0);
			$data .= "$nostr[0]<a href=\"$href\"$akstr[0]>&lt;&lt; 最初の$cfg{DispNum}件</a><br>";
		}
		
		# 「最後」リンクの表示判定
		if ($page < $lastpage - 1) {
			my $href = &make_href("", 0, $lastpage, 0, 0);
			if ($amari > 0) {
				$data .= "$nostr[8]<a href=\"$href\"$akstr[8]>最後の$amari件 &gt;&gt;</a><br>";
			} else {
				$data .= "$nostr[8]<a href=\"$href\"$akstr[8]>最後の$cfg{DispNum}件 &gt;&gt;</a><br>";
			}
		}
	} else {
		$data .= "<center>1/1</center>";
	}

	# 最近のコメント一覧へのリンク
	if ($page == 0) {
		require MT::Comment;
		my $blog_comment_cnt = MT::Comment->count({ blog_id => $cfg{Blog_ID} });
		if ($blog_comment_cnt) {
			my $href = &make_href("recentcomment", 0, 0, 0, 0);
			$data .= "<hr><a href=\"$href\">最近のｺﾒﾝﾄ$cfg{RecentComment}件</a>";
		}
	}
	
	# 管理者用URLへのリンクを表示する
	if ($cfg{AdminDoor} eq "yes"){
		$data .= "<hr>";
		my $href = &make_href("admindoor", 0, 0, 0);
		$data .= "<form method=\"post\" action=\"$href\">";
		$data .= "管理者用URLを取得<br>";
		$data .= "\AdminPasswordの値";
		$data .= "<br><input type=\"text\" name=\"pw_text\" istyle=3><br>";
		$data .= "<input type=\"hidden\" name=\"id\" value=\"$cfg{Blog_ID}\">";
		$data .= "<input type=\"hidden\" name=\"mode\" value=\"admindoor\">";
		$data .= "<input type=\"submit\" value=\"送信\">";
		if ($key){
			$data .= "<input type=hidden name=\"key\" value=\"$key\">";
		}
		$data .= "</form>";
		
		if ($admin_mode eq "yes"){
			$data .= '<font color="red">あなたは管理者用URLを入手済みです。このURLをﾌﾞｯｸﾏｰｸした後、速やかに「MT4i Manager」にて"AdminDoor"の値を"no"に変更してください。</font><br>';
		}
		if ($cfg{AdminPassword} eq "password"){
			$data .= '<font color="red">"AdminPassword"がﾃﾞﾌｫﾙﾄ値"password"から変更されていません。このままだと他人に管理者URLを推測される可能性が非常に高くなります。速やかに変更してください。</font><br>';
		}
	}
	
	#管理者用メニュー
	if ($admin_mode eq "yes"){
		$data .= "<hr>";
		my $href = &make_href("entryform", 0, 0, 0, 0);
		$data .= "<a href='$href'>[管]Entryの新規作成</a><br>";
		
		my $href = &make_href("email_comments", 0, 0, 0, 0);
		if ($email_new_comments){
			$data .= "<a href='$href'>[管]ｺﾒﾝﾄのﾒｰﾙ通知を停止する</a><br>";
		}else{
			$data .= "<a href='$href'>[管]ｺﾒﾝﾄのﾒｰﾙ通知を再開する</a><br>";
		}
		$data .= "<hr>";
	}
	
	&htmlout;
}

########################################
# Sub Individual - 単記事ページの描画
########################################

sub individual {
	my $rowid;
	if ($no) {
		$rowid = $no;
		$no--;
	} else {
		$no = 0;
		### valium add start
		my $ttlcnt = &get_ttlcnt;
		FOUND: while ($ttlcnt > 0) {
			my @entries = &get_entries($no, $cfg{DispNum});
			if (@entries <= 0) {
				last;
			}
			for my $entry (@entries) {
				$no++;
				if ($entry->id == $eid) {
					last FOUND;
				}
			}
			$ttlcnt -= $cfg{DispNum};
		}
		$rowid = $no;
		$no--;
		### valium add end
	}
	
	####################
	# 記事の取得
	require MT::Entry;
	my $entry = MT::Entry->load($eid);

	# 検索結果が0件の場合はメッセージ表示してSTOP（有り得ないけどな）
	if (!$entry) {
		$data = "Entry ID '$eid' は不正です。";
		&errorout;
		exit;      # exitする
	}

	# 結果を変数に格納
	my $title = &conv_euc_z2h($entry->title);
	#my $text = &conv_euc_z2h($entry->text);
	#my $text_more = &conv_euc_z2h($entry->text_more);
	my $text = &conv_euc_z2h(MT->apply_text_filters($entry->text, $entry->text_filters));
	my $text_more = &conv_euc_z2h(MT->apply_text_filters($entry->text_more, $entry->text_filters));
	my $convert_breaks = &conv_euc_z2h($entry->convert_breaks);
	my $created_on = &conv_euc_z2h(&conv_datetime($entry->created_on));
	my $comment_cnt = $entry->comment_count;
	my $ping_cnt = $entry->ping_count;
	my $ent_allow_comments = $entry->allow_comments;
	my $ent_status = $entry->status;
	
	# 本文と追記を一つにまとめる
	if($text_more){
		$text = "<p>$text</p><p>$text_more</p>";
	}
	
	####################
	# リンクのURLをchtmltrans経由に変換
	$text = &chtmltrans($text, $rowid, $eid);
	
	####################
	# <img>タグソースURLのスラッシュを%2Fに変換
	$text = &img_url_conv($text);
	
	####################
	# 画像の除去（退避）
	
	# aタグを含めた除去、ALTの表示、画像へのリンク
	my $href = &make_href("image", $rowid, 0, $eid, 0);
	$text =~ s/<a[^>]*><img[^>]*src=["']([^"'>]*)["'][^>]*alt=["']([^"'>]*)["'][^>]*><\/a>/&lt;<a href="$href&amp;img=$1">画像：$2<\/a>&gt;/ig;
	$text =~ s/<a[^>]*><img[^>]*alt=["']([^"'>]*)["'][^>]*src=["']([^"'>]*)["'][^>]*><\/a>/&lt;<a href="$href&amp;img=$2">画像：$1<\/a>&gt;/ig;
	
	# imgタグのみの除去、ALTの表示、画像へのリンク
	$text =~ s/<img[^>]*src=["']([^"'>]*)["'][^>]*alt=["']([^"'>]*)["'][^>]*>/&lt;<a href="$href&amp;img=$1">画像：$2<\/a>&gt;/ig;
	$text =~ s/<img[^>]*alt=["']([^"'>]*)["'][^>]*src=["']([^"'>]*)["'][^>]*>/&lt;<a href="$href&amp;img=$2">画像：$1<\/a>&gt;/ig;
	
	# aタグを含めた除去、画像へのリンク
	$text =~ s/<a[^>]*><img[^>]*src=["']([^"'>]*)["'][^>]*><\/a>/&lt;<a href="$href&amp;img=$1">画像<\/a>&gt;/ig;
	
	# imgタグのみの除去、画像へのリンク
	$text =~ s/<img[^>]*src=["']([^"'>]*)["'][^>]*>/&lt;<a href="$href&amp;img=$1">画像<\/a>&gt;/ig;
	
	####################
	# タグ変換等
	if($convert_breaks eq '__default__' || ($convert_breaks ne '__default__' && $convert_breaks ne '0' && $convert_paras eq '__default__')) {
		# bqタグ部の色変更
		if ($cfg{BqColor}) {
			$text=~s/<blockquote>/<blockquote><font color="$cfg{BqColor}">/ig;
			$text=~s/<\/blockquote>/<\/font><\/blockquote>/ig;
		}
		# bqタグのpタグへの変換
		if ($cfg{BQ2P} eq "yes") {
			$text=~s/<blockquote>/<p>/ig;
			$text=~s/<\/blockquote>/<\/p>/ig;
		} else {
			# bqタグ周りの余計なbrタグ除去
			$text=~s/<br><br><blockquote>/<blockquote>/ig;
			$text=~s/<br><blockquote>/<blockquote>/ig;
			$text=~s/<\/blockquote><br><br>/<\/blockquote>/ig;
			$text=~s/<p><blockquote>/<blockquote>/ig;
			$text=~s/<\/blockquote><\/p>/<\/blockquote>/ig;
		}
		# pタグ周りの余計なbrタグ除去
		$text=~s/<br \/><br \/><p>/<p>/ig;
		$text=~s/<br \/><p>/<p>/ig;
		$text=~s/<\/p><br \/><br \/>/<\/p>/ig;
		$text=~s/<br \/><\/p>/<\/p>/ig;
		# ulタグ周りの余計なbrタグ除去
		$text=~s/<br \/><br \/><ul>/<ul>/ig;
		$text=~s/<br \/><ul>/<ul>/ig;
		$text=~s/<ul><br \/>/<ul>/ig;
		$text=~s/<\/ul><br \/><br \/>/<\/ul>/ig;
		# olタグ周りの余計なbrタグ除去
		$text=~s/<br \/><br \/><ol>/<ol>/ig;
		$text=~s/<br \/><ol>/<ol>/ig;
		$text=~s/<ol><br \/>/<ol>/ig;
		$text=~s/<\/ol><br \/><br \/>/<\/ol>/ig;
	}
	
	####################
	# 本文分割処理
	if (&lenb_euc($text) > $cfg{SprtLimit}) {
		$text = &separate($text, $rowid);
	}
	
	####################
	# 表示文字列生成
	$data .= "<h4>";
	
	# 記事一覧からの閲覧なら記事番号を振る
	if ($mode eq 'individual') {
		$data .= "$rowid.";
	}
	
	# 下書き／指定日かどうかを調べる
	my $d_f;
	if ($ent_status == 1) {
		$d_f = '(下書き)';
	} elsif ($ent_status == 3) {
		$d_f = '(指定日)';
	}
	
	$data .= "$d_f$title";
	
	# カテゴリ名の表示
	if ($cfg{IndividualCatLabelDisp} eq 'yes') {
		my $cat_label = &check_category($entry);
		$data .= "[$cat_label]";
	}
	
	if ($cfg{IndividualAuthorDisp} eq 'yes') {
		# Authorのnicknameがあれば、それを表示。無ければnameを表示する
		require MT::Author;
		my $author = MT::Author->load({ id => $entry->author_id });
		my $author_name;
		
		if ($author){
			if ($author->nickname){
				$author_name = conv_euc_z2h($author->nickname);
			}else{
				$author_name = $author->name;
			}
			$data .= " by ".$author_name;
		}
	}
	
	$data .= "$created_on</h4>";
	$data .= "<hr>";
	$data .= "$text";
	
	my $ttlcnt;
	# 記事一覧からの閲覧なら記事番号を振る
	if ($mode eq 'individual') {
		# 総件数取得
		$ttlcnt = &get_ttlcnt;
		
		# エントリー数表示
		$data .= "<center>$rowid/$ttlcnt</center><hr>";
	} else {
		$data .= "<hr>";
	}
	
	#####################
	# Noneでは投稿も表示も無し、Openなら両方OK、Closedは表示のみ
	# $comment_cntの値 None=0,Open=1,Closed=2
	if ($ent_allow_comments > 0){
		if ($comment_cnt > 0) {
			if ($mode eq 'individual') {
				$href = &make_href("comment", $rowid, 0, $eid, 0);
			} elsif ($mode eq 'individual_rcm') {
				$href = &make_href("comment_rcm", $rowid, 0, $eid, 0);
			} elsif ($mode eq 'individual_lnk') {
				$href = &make_href("comment_lnk", $rowid, 0, $eid, $ref_eid);
			}
			if ($mode ne 'ainori') {
				# あいのり時はコメント参照できないように。
				# 何故って色々面倒だからさっ。
				$data .= "$nostr[8]<a href=\"$href\"$akstr[8]>ｺﾒﾝﾄ($comment_cnt)</a><hr>";
			}
		} elsif ($ent_allow_comments == 1) {
			if ($mode eq 'individual') {
				$href = &make_href("postform", $rowid, 0, $eid, 0);
				$data .= "$nostr[8]<a href=\"$href\"$akstr[8]>ｺﾒﾝﾄ投稿</a><hr>";
			} elsif ($mode eq 'individual_rcm') {
				$href = &make_href("postform_rcm", $rowid, 0, $eid, 0);
				$data .= "$nostr[8]<a href=\"$href\"$akstr[8]>ｺﾒﾝﾄ投稿</a><hr>";
			}
				# ※モード「comment_lnk」の時はコメント投稿できない。
				# ※参照目的なんだからコメント書くこと無いでしょ、たぶん。
		}
	}
	
	# Trackback
	if ($ping_cnt > 0) {
		$href = &make_href("trackback", $rowid, 0, $eid);
		$data .= "$nostr[9]<a href=\"$href\"$akstr[9]>ﾄﾗｯｸﾊﾞｯｸ($ping_cnt)</a><hr>";
	}

	# 管理者のみ「Entry編集・消去」が可能
	if ($admin_mode eq "yes"){
		$href = &make_href("entryform", $rowid, 0,$eid, 0);
		$data .="<a href='$href'>[管]このEntryを編集</a><br>";
		$href = &make_href("confirm_entry_del", $rowid, 0,$eid, 0);
		$data .="<a href='$href'>[管]このEntryを削除</a><hr>";
	}
	
	if ($mode eq 'individual') {
		# 記事一覧からの閲覧
		# 引数用エントリーNO算出
		my $nextno = $rowid + 1;
		my $prevno = $rowid - 1;
		
		# 引数用エントリーID算出（prevとnextが引っ繰り返っているので注意）
		my $nextid;
		my $previd;
		if (my $next = $entry->previous(1)) {
			$nextid = $next->id;
		}
		if (my $prev = $entry->next(1)) {
			$previd = $prev->id;
		}
		
		if($rowid < $ttlcnt) {
			$href = &make_href("individual", $nextno, 0, $nextid, 0);
			$data .= "$nostr[9]<a href=\"$href\"$akstr[9]>次の記事へ &gt;</a><br>";
		}
		if($rowid > 1) {
			$href = &make_href("individual", $prevno, 0, $previd, 0);
			$data .= "$nostr[7]<a href=\"$href\"$akstr[7]>&lt; 前の記事へ</a><br>";
		}
		# ページ数算出
		$page = int($no / $cfg{DispNum});	# int()で小数点以下は切り捨て
		
		$href = &make_href("", 0, $page, 0, 0);
		$data .= "$nostr[0]<a href=\"$href\"$akstr[0]>一覧へ戻る</a>";
	} elsif ($mode eq 'individual_rcm') {
		# 最近コメント一覧からの閲覧
		$href = &make_href("recentcomment", 0, 0, 0, 0);
		$data .= "$nostr[0]<a href=\"$href\"$akstr[0]>最近ｺﾒﾝﾄ一覧へ戻る</a>";
	} elsif ($mode eq 'individual_lnk') {
		# 記事中リンクからの閲覧
		$href = &make_href("individual", $rowid, 0, $ref_eid, 0);
		$data .= "$nostr[0]<a href=\"$href\"$akstr[0]>ﾘﾝｸ元の記事へ戻る</a>";
	} elsif ($mode eq 'ainori') {
		# あいのり時はリファラへ戻る
		$href = $ENV{'HTTP_REFERER'};
		$data .= "$nostr[0]<a href=\"$href\"$akstr[0]>ﾘﾝｸ元へ戻る</a>";
	}
	
	&htmlout;
}

########################################
# Sub Comment - コメント描画
########################################

sub comment {
	my $rowid = $no;
	
	####################
	# entry idの取得
	require MT::Entry;
	my $entry = MT::Entry->load($eid);

	# 検索結果が0件の場合はメッセージ表示してSTOP（有り得ないけどな）
	if ($entry <= 0) {
		$data = "Entry ID '$eid' は不正です。";
		&errorout;
		exit;      # exitする
	}

	# 結果を変数に格納
	my $ent_title = &conv_euc_z2h($entry->title);
	my $ent_created_on = &conv_euc_z2h(&conv_datetime($entry->created_on));
	my $ent_id = $entry->id;
	my $ent_allow_comments = $entry->allow_comments;
	
	####################
	# コメントの取得
	my @comments;
	# 管理者モードではコメントを逆順表示する
	if ($admin_mode eq "yes"){
		@comments = get_comments($ent_id, '', 'descend', 1);
	}else{
		@comments = get_comments($ent_id, '', $sort_order_comments, 1);
	}
	
	my $author;
	my $txt;
	my $created_on;
	my $text;
	for my $comment (@comments) {
		$author = &conv_euc_z2h($comment->author);
		$txt = &conv_euc_z2h($comment->text);
		$created_on = &conv_euc_z2h(&conv_datetime($comment->created_on));
		$text .= "<hr>by $author$created_on<br><br>$txt";
		
		# 管理者のみ「コメント消去」等が可能
		if ($admin_mode eq "yes"){
			my $href = &make_href("confirm_comment_del", $rowid, $comment->id, $eid, 0);
			$text .="<br><_ahref=\'$href\'>[管]このｺﾒﾝﾄを削除</a><br>";
			#$href = &make_href("confirm_comment_ipban", $rowid, $comment->id, $eid, 0);
			#$text .="<_ahref=\'$href\'>[管]このIPからのコメントを禁止＆全削除</a>";
		}
	}

	####################
	# タグ変換等
	if($convert_paras_comments eq '__default__'){
		# 改行のbrタグへの変換
		$text=~s/\r\n/<br>/g;
		$text=~s/\r/<br>/g;
		$text=~s/\n/<br>/g;
	}

	####################
	# リンクのURLをchtmltrans経由に変換
	$text = &chtmltrans($text, $rowid, $eid);
	
	####################
	# <_ahref>を<a href>に戻す
	$text=~s/_ahref/a href/g;
	
	####################
	# 本文分割処理
	if (&lenb_euc($text) > $cfg{SprtLimit}) {
		$text = &separate($text, $rowid);
	}
	
	####################
	# 表示文字列生成
	$data .= "<h4>";
	if ($rowid) {
		$data .= "$rowid.";
	}
	if ($admin_mode eq "yes"){
		$data .= "$ent_title$ent_created_onへのｺﾒﾝﾄ(新しい順)</h4>";
	}else{
		$data .= "$ent_title$ent_created_onへのｺﾒﾝﾄ</h4>";
	}
	$data .= "$text<hr>";
	if ($ent_allow_comments == 1){
		if ($mode eq 'comment') {
			my $href = &make_href("postform", $rowid, 0, $eid, 0);
			$data .= "$nostr[8]<a href=\"$href\"$akstr[8]>ｺﾒﾝﾄ投稿</a><hr>";
		} elsif ($mode eq 'comment_rcm') {
			my $href = &make_href("postform_rcm", $rowid, 0, $eid, 0);
			$data .= "$nostr[8]<a href=\"$href\"$akstr[8]>ｺﾒﾝﾄ投稿</a><hr>";
		}
			# ※モード「comment_lnk」の時はコメント投稿できない。
			# ※参照目的なんだからコメント書くこと無いでしょ、たぶん。
	}
	my $href = &make_href("individual", $rowid, 0, $eid, 0);
	if ($mode eq 'comment') {
		$data .= "$nostr[0]<a href=\"$href\"$akstr[0]>記事へ戻る</a>";
	} else {
		if ($mode eq 'comment_rcm') {
			$href =~ s/individual/individual_rcm/ig;
		} elsif ($mode eq 'comment_lnk') {
			$href = &make_href("individual_lnk", $rowid, 0, $eid, $ref_eid);
		}
		$data .= "$nostr[7]<a href=\"$href\"$akstr[7]>元記事を読む</a><hr>";
		if ($mode eq 'comment_rcm') {
			my $href = &make_href("recentcomment", 0, 0, 0, 0);
			$data .= "$nostr[0]<a href=\"$href\"$akstr[0]>最近ｺﾒﾝﾄ一覧へ戻る</a>";
		} elsif ($mode eq 'comment_lnk') {
			my $href = &make_href("individual", $rowid, 0, $ref_eid, 0);
			$data .= "$nostr[0]<a href=\"$href\"$akstr[0]>ﾘﾝｸ元の記事へ戻る</a>";
		}
	}

	&htmlout;
}

########################################
# Sub Recent_Comment - コメントまとめ読み
########################################

sub recent_comment {
	
	####################
	# コメントの取得
	my @comments = get_comments('', $cfg{RecentComment}, 'descend', 1);
	
	my $text;
	require MT::Entry;
	for my $comment (@comments) {
		my $author = &conv_euc_z2h($comment->author);
		my $created_on = &conv_euc_z2h(&conv_datetime($comment->created_on));
		my $eid = $comment->entry_id;
		
		my $entry = MT::Entry->load($eid);
		my $entry_title = &conv_euc_z2h($entry->title);
		
		my $href = &make_href("comment_rcm", 0, 0, $eid, 0);
		$text .= "<hr>Re:<a href=\"$href\">$entry_title</a><br>by $author$created_on";
	}

	####################
	# 表示文字列生成
	$data .= "<h4>最近のコメント$cfg{RecentComment}件</h4>";
	$data .= "$text<hr>";
	
	my $href = &make_href("", 0, 0, 0, 0);
	$data .= "<br>$nostr[0]<a href='$href'$akstr[0]>一覧へ戻る</a>";

	&htmlout;
}

########################################
# Sub Trackback - トラックバック表示
########################################

sub trackback {
	
	my $rowid = $no;
	
	####################
	# トラックバックの取得
	require MT::Trackback;
	my $tb = MT::Trackback->load(
	        { blog_id => $cfg{Blog_ID} , entry_id => $eid},
	        { sort => 'created_on',
	          direction => 'descend',
	          unique => 1,
	          limit => 1 });
	
	require MT::TBPing;
	my @tbpings = MT::TBPing->load({ blog_id => $cfg{Blog_ID} , tb_id => $tb->id},
	        { sort => 'created_on',
	          direction => 'descend',
	          unique => 1,
	          limit => $cfg{RecentTB} });
	
	my $text;
	for my $tbping (@tbpings) {
		my $ping_title = &conv_euc_z2h($tbping->title);
		my $ping_excerpt = &conv_euc_z2h($tbping->excerpt);
		my $ping_name = &conv_euc_z2h($tbping->blog_name);
		my $ping_tracked = &conv_euc_z2h($tbping->created_on);
		my $ping_sourceurl = &conv_euc_z2h($tbping->source_url);
		my $ping_id = &conv_euc_z2h($tbping->id);
		
		$text .= "<hr>$ping_title<br>$ping_excerpt<br><a href=\"$ping_sourceurl\">Weblog:$ping_name</a><br>Tracked:$ping_tracked<br>";
		# 管理者のみ「トラックバック削除」等が可能
		if ($admin_mode eq "yes"){
			my $href = &make_href("confirm_trackback_del", $rowid, $ping_id, $eid, 0);
			$text .="<_ahref=\'$href\'>[管]このTBを削除</a><br>";
			#$href = &make_href("confirm_trackback_ipban", $rowid, $ping_id, $eid, 0);
			#$text .="<_ahref=\'$href\'>[管]このIPからのTBを禁止＆全削除</a>";
		}
	}
	
	####################
	# リンクのURLをchtmltrans経由に変換
	$text = &chtmltrans($text);
	
	####################
	# <_ahref>を<a href>に戻す
	$text=~s/_ahref/a href/g;
	
	####################
	# 表示文字列生成
	if (@tbpings < $cfg{RecentTB}){
		$cfg{RecentTB} = @tbpings;
	}
	
	$data .= "<h4>このEntryへの最近のﾄﾗｯｸﾊﾞｯｸ$cfg{RecentTB}件(新しい順)</h4>";
	$data .= "$text<hr>";
	
	my $href = &make_href("individual", $rowid, 0, $eid);
	$data .= "$nostr[0]<a href=\"$href\"$akstr[0]>記事へ戻る</a>";
	
	&htmlout;
}

#############################################
# Sub Get_Entries - エントリの取得
# 第一引数 : オフセット
# 第二引数 : 取得個数
# 管理者の場合には、statusの限定解除
#############################################
sub get_entries {
	my @ent;
	require MT::Entry;
	
	if ($admin_mode eq "yes"){
		if ($cat == 0) {
			# カテゴリ指定なし
			@ent = MT::Entry->load(
				 { blog_id => $cfg{Blog_ID} },
				 { limit => $_[1],
				   offset => $_[0],
				   sort => 'created_on',
				   direction => 'descend' });
		} else {
			# カテゴリ指定あり
			@ent = MT::Entry->load(
				 { blog_id => $cfg{Blog_ID} },
				 { join =>
					   [ 'MT::Placement',
						 'entry_id',
						 { blog_id => $cfg{Blog_ID},
						   category_id => $cat } ],
				   limit => $_[1],
				   offset => $_[0],
				   sort => 'created_on',
				   direction => 'descend' });
		}
	} else {
		if ($cat == 0) {
			# カテゴリ指定なし
			@ent = MT::Entry->load(
				 { blog_id => $cfg{Blog_ID},
				   status => 2 },
				 { limit => $_[1],
				   offset => $_[0],
				   sort => 'created_on',
				   direction => 'descend' });
		} else {
			# カテゴリ指定あり
			@ent = MT::Entry->load(
				 { blog_id => $cfg{Blog_ID},
				   status => 2 },
				 { join =>
					   [ 'MT::Placement',
						 'entry_id',
						 { blog_id => $cfg{Blog_ID},
						   category_id => $cat } ],
				   limit => $_[1],
				   offset => $_[0],
				   sort => 'created_on',
				   direction => 'descend' });
		}
	}
	
	return @ent;
}

#############################################
# Sub Get_Comments - コメントの取得
# 第一引数 : エントリーID
# 第二引数 : 取得個数
# 第三引数 : ソート降順／昇順
# 第四引数 : visible値チェックの有無 1:有 0:無
#############################################
sub get_comments {
	my %arg1;
	my %arg2;
	
	$arg1{'blog_id'} = $cfg{Blog_ID};
	if ($_[0] ne '') {
		$arg1{'entry_id'} = $_[0];
	}
	if ($mt->version_number() >= 3.0 && $_[3] == 1) {
		$arg1{'visible'} = 1;
	}
	
	$arg2{'sort'} = 'created_on';
	$arg2{'direction'} = $_[2];
	$arg2{'unique'} = 1;
	if ($_[1] ne '') {
		$arg2{'limit'} = $_[1];
	}
	
	require MT::Comment;
	my @cmnt = MT::Comment->load(\%arg1, \%arg2);
	
	return @cmnt;
}

##############################################
# Sub Get_Ttlcnt - 記事総数の取得
##############################################
sub get_ttlcnt {
	require MT::Entry;
	require MT::Placement;
	if ($cat == 0) {
		#カテゴリなし
		return MT::Entry->count({blog_id => $cfg{Blog_ID}, status => 2},
				{sort => 'created_on',
				 direction => 'descend',
				 unique => 1});
	} else {
		#カテゴリあり
		return MT::Entry->count({blog_id => $cfg{Blog_ID}, status => 2}, {
				join => [ 'MT::Placement', 'entry_id', { blog_id => $cfg{Blog_ID},
														   category_id => $cat } ],
				sort => 'created_on',
				direction => 'descend',
				unique => 1});
	}
}

##############################################
# Sub Make_Href - HREF文字列の作成
# 第一引数 : mode
# 第二引数 : no
# 第三引数 : page
# 第四引数 : eid
# 第五引数 : ref_eid
#
# 例外として、$modeが"post"の場合には
# idを出力しません
##############################################
sub make_href
{
	my $h = "$cfg{MyName}";
	if ($_[0] ne "post" && $_[0] ne "post_rcm" && $_[0] ne "post_lnk"){
		$h .= "?id=$cfg{Blog_ID}";
		if ($cat != 0) {
			$h .= "&amp;cat=$cat";
		}
		if ($_[0] ne "" && $_[0] ne "main") {
			$h .= "&amp;mode=$_[0]";
		}
		if ($_[1] != 0) {
			$h .= "&amp;no=$_[1]";
		}
		if ($_[2] != 0) {
			$h .= "&amp;page=$_[2]";
		}
		if ($_[3] != 0) {
			$h .= "&amp;eid=$_[3]";
		}
		if ($_[4] != 0) {
			$h .= "&amp;ref_eid=$_[4]";
		}
		if ($key){
			$h .= "&amp;key=$key";
		}
	}
	return $h;
}

########################################
# Sub Image - 画像表示
########################################

sub image {
	# PerlMagick が無ければ画像縮小表示処理はしない
	if ($imk == 0){
		$img =~ s/\%2F/\//ig;
		$data .="<p><img src=\"$img\"></p>";
	}else{
        # /を%2Fに再エンコード
		$img =~ s/\//\%2F/ig;
		$data .="<p><img src=\"./$cfg{MyName}?mode=img_cut&amp;id=$cfg{Blog_ID}&amp;img=$img\"></p>";
	}
	my $href = &make_href("individual", $no, 0, $eid, 0);
	$data .="$nostr[0]<a href=\"$href\"$akstr[0]>戻る</a>";
	
	&htmlout;
}

########################################
# Sub Image_Cut - 画像縮小表示
########################################

sub image_cut {
	$img =~ s/\%2F/\//ig;
	my $url = $img;
	$url =~ s/http:\/\///;
	my $host = substr($url, 0, index($url, "/"));
	my $path = substr($url, index($url, "/"));
	$data = "";

	####################
	# ホスト名置換
	if ($host eq $cfg{Photo_Host_Original}){
		$host = $cfg{Photo_Host_Replace};
	}
	
	####################
	# 画像読み込みをLWPモジュール使用に変更
	require HTTP::Request;
	require LWP::UserAgent;
	my $ua = LWP::UserAgent->new;
	$url = 'http://'.$host.$path;
	my $request = HTTP::Request->new(GET => $url);
	my $response = $ua->request($request);
	
	if ($response->is_success) {
		$data = $response->as_string;
		$data =~ /(.*?\r?\n)\r?\n(.*)/s;
		$data = $2;
	} else {
		print "Content-type: text/html\n\nHTTP Error:LWP";
		return;
	}
	
	my @blob = $data;
	
	####################
	# vodafoneの特定機種に限りpng、それ以外はjpgに変換
	# サイズに関わらず、pngもしくはjpgに変換するように変更
	my $image = Image::Magick->new;
	$image->BlobToImage(@blob);
	
	# デジカメなどのアプリケーション情報の削除
	if (Image::Magick->VERSION >= 6.0) {
		$image->Strip();
	} else {
		$image->Profile( name=>'*' );
		$image->Comment('');
	}
	
	my $format;
	
	if ($png_flag){
		$image->Set(magick=>'png');
		$format = 'png';
		$cfg{PhotoWidth} = $cfg{PngWidth};
	}else{
		$image->Set(magick=>'jpg');
		$format = 'jpeg';
	}
	
	# 参考：http://deneb.jp/Perl/mobile/
	my $start_pos = 0;
	my $user_agent = $ENV{'HTTP_USER_AGENT'};
	my $cache_limit = -1024 + &calc_cache_size( $user_agent );
	# 画像が既にキャッシュ許容範囲内なら縮小処理しない
	@blob = $image->ImageToBlob();
	if ( $cache_limit <  length($blob[0]) ) {
		foreach my $i ( $start_pos ..19 ) {
			my $img2 = $image->Clone();
			my $ratio = 1-$i*0.05;
			my $x = $cfg{PhotoWidth} * $ratio;
			$img2->Scale($x);
			@blob = $img2->ImageToBlob();
			if ( $cache_limit >=  length($blob[0]) ) {
				last;
			}
		}
	}

	print "Content-type: image/$format\n";
	print "Content-length: ",length($blob[0]),"\n\n";
	binmode STDOUT;
	print STDOUT $blob[0];
}

########################################
# Sub Postform - コメント投稿フォーム
########################################

sub postform {
	my $rowid = $no;
	
	# Entry検索
	require MT::Entry;
	my $entry = MT::Entry->load($eid);

	# 検索結果が0件の場合はメッセージ表示してSTOP（有り得ないけどな）
	if ($entry <= 0) {
		$data = "Entry ID '$eid' は不正です。";
		&errorout;
		exit;      # exitする
	}

	# 結果を変数に格納
	my $ent_title = &conv_euc_z2h($entry->title);
	my $ent_created_on = &conv_euc_z2h(&conv_datetime($entry->created_on));

	####################
	# 表示文字列生成
	$data = "<h4>";
	if ($rowid) {
		$data .= "$rowid.";
	}
	$data .= "$ent_title$ent_created_onへのｺﾒﾝﾄ投稿</h4><hr>";
	if ($mt->version_number() >= 3.0 && $cfg{ApproveComment} eq 'no') {
		$data .= "ｺﾒﾝﾄは投稿後、掲載を保留されます。<br>管理人による承諾後、掲載されます。<br>";
	}
	$data .= $cfg{CommentNotes};
	my $href;
	if ($mode eq 'postform') {
		$href = &make_href("post", 0, 0, $eid, 0);
	} elsif ($mode eq 'postform_rcm') {
		$href = &make_href("post_rcm", 0, 0, $eid, 0);
	} elsif ($mode eq 'postform_lnk') {
		$href = &make_href("post_lnk", 0, 0, $eid, 0);
	}
	$data .= "<form method=post action=\"$href\">";
	$data .= "名前";
	if ($cfg{PostFromEssential} ne "yes"){
		$data .= "(省略可)";
	}
	$data .= "<br><input type=text name=from><br>";
	$data .= "ﾒｰﾙｱﾄﾞﾚｽ";
	if ($cfg{PostMailEssential} ne "yes"){
		$data .= "(省略可)";
	}
	$data .= "<br><input type=text name=mail><br>";
	$data .= "ｺﾒﾝﾄ";
	if ($cfg{PostTextEssential} ne "yes"){
		$data .= "(省略可)";
	}
	$data .= "<br><textarea rows=4 name=text></textarea><br>";
	$data .= "<input type=hidden name=id value=$cfg{Blog_ID}>";
	if ($mode eq 'postform') {
		$data .= "<input type=hidden name=mode value=post>";
	} elsif ($mode eq 'postform_rcm') {
		$data .= "<input type=hidden name=mode value=post_rcm>";
	} elsif ($mode eq 'postform_lnk') {
		$data .= "<input type=hidden name=mode value=post_lnk>";
	}
	$data .= "「送信」を押してから書き込み完了まで多少時間がかかります。<br>環境によってはﾀｲﾑｱｳﾄが出ることがありますが、書き込みは完了しています。<br>「送信」の二度押しは絶対にしないで下さい。<br>";
	$data .= "<input type=hidden name=no value=$rowid>";
	$data .= "<input type=hidden name=eid value=$eid>";
	if ($key){
		$data .= "<input type=hidden name=\"key\" value=\"$key\">";
	}
	$data .= "<input type=submit value='送信'>";
	$data .= "</form>";
	$data .= "<hr>";
	if ($mode eq 'postform') {
		$href = &make_href("individual", $rowid, 0, $eid, 0);
	} elsif ($mode eq 'postform_rcm') {
		$href = &make_href("individual_rcm", $rowid, 0, $eid, 0);
	} elsif ($mode eq 'postform_lnk') {
		$href = &make_href("individual_lnk", $rowid, 0, $eid, 0);
	}
	$data .="$nostr[0]<a href='$href'$akstr[0]>戻る</a>";
	&htmlout;
}

########################################
# Sub Post - コメント投稿->表示処理
########################################
sub post {
	require MT::Comment;
	require MT::App;
	

	my $rowid = $no;
	$no--;
	
	# 投稿内容を一旦EUC-JPに変換
	&$jcnv(\$post_from, 'euc', 'sjis');
	&$jcnv(\$post_mail, 'euc', 'sjis');
	&$jcnv(\$post_text, 'euc', 'sjis');
	
	####################
	# admin_helperをチェック(管理者モード時のみ)
	my $post_from_org = $post_from;
	if (($cfg{AdminHelper} eq 'yes') && ($admin_mode eq 'yes')){
		if ($post_from_org eq $cfg{AdminHelperID}){
			$post_from = $cfg{AdminHelperNM};
			$post_mail = $cfg{AdminHelperML};
		}
	}
	
	####################
	# 必須入力項目をチェック
	# 名前,mail,textのどれも入力が無ければエラー
	if(((!$post_from)&&(!$post_text)&&(!$post_mail))||
       ((!$post_from)&&($cfg{PostFromEssential} eq "yes"))||
       ((!$post_mail)&&($cfg{PostMailEssential} eq "yes"))||
       ((!$post_text)&&($cfg{PostTextEssential} eq "yes")))
	{
		$data .="Error!<br>未入力項目があります.<br>";
		my $href = &make_href("postform", $rowid, 0, $eid, 0);
		$data .="$nostr[0]<a href='$href'$akstr[0]>戻る</a>";
		&errorout;
		return;
	}
	
	####################
	# メールアドレスチェック
	if ($post_mail){
		unless($post_mail=~/^[\w\-+\.]+\@[\w\-+\.]+$/i){
			$data .="Error!<br>ﾒｰﾙｱﾄﾞﾚｽが不正です.<br>";
			my $href = &make_href("postform", $rowid, 0, $eid, 0);
			$data .="$nostr[0]<a href='$href'$akstr[0]>戻る</a>";
			&errorout;
			return;
		}
	}

	# 投稿された文字列の半角文字を全角に変換
	if ($jcd == 0) {
		&jcode::h2z_euc($post_from);
		&jcode::h2z_euc($post_mail);
		&jcode::h2z_euc($post_text);
	} else {
		Jcode->new(\$post_from,'euc')->h2z;
		Jcode->new(\$post_mail,'euc')->h2z;
		Jcode->new(\$post_text,'euc')->h2z;
	}

	# PublishCharsetに変換
	if ($conv_in ne 'euc') {
		if ($conv_in eq 'utf8' && $ecd == 1) {
			$post_from = encode("shiftjis",decode("euc-jp",$post_from));
			$post_mail = encode("shiftjis",decode("euc-jp",$post_mail));
			$post_text = encode("shiftjis",decode("euc-jp",$post_text));
			$post_from = encode("utf8",decode("cp932",$post_from));
			$post_mail = encode("utf8",decode("cp932",$post_mail));
			$post_text = encode("utf8",decode("cp932",$post_text));
		} else {
			&$jcnv(\$post_from, $conv_in, 'euc');
			&$jcnv(\$post_mail, $conv_in, 'euc');
			&$jcnv(\$post_text, $conv_in, 'euc');
		}
	}
	
	# 連続投稿防止
	# （直前のコメントと比較して同内容であれば
	# 　連続投稿とみなしエラーとする。
	# 　悪意ある連続投稿防止というよりは、
	# 　タイムアウト後などの不作為の過失防止。）
	my @comments = get_comments($eid, 1, 'descend', 0);
	
	for my $tmp (@comments) {
		if ($post_from eq $tmp->author &&
			$post_mail eq $tmp->email &&
			$post_text eq $tmp->text) {
			$data .="Error!<br>同内容のｺﾒﾝﾄが既に投稿されています<hr>";
			my $href = &make_href("comment", $rowid, 0, $eid, 0);
			$data .="$nostr[0]<a href='$href'$akstr[0]>投稿されたｺﾒﾝﾄを確認する</a>";
			&errorout;
			return;
		}
	}
	
	# Entry ID、Entry Titleの取得
	require MT::Entry;
	my $entry = MT::Entry->load($eid);

	# 検索結果が0件の場合はメッセージ表示してSTOP（有り得ないけどな）
	if ($entry <= 0) {
		$data = "Entry ID '$eid' は不正です。";
		&errorout;
		exit;      # exitする
	}

	# DB更新
    my $comment = MT::Comment->new;
    my $rm_ip = $ENV{'REMOTE_ADDR'};
    $comment->ip($rm_ip);
    $comment->blog_id($cfg{Blog_ID});
    $comment->entry_id($entry->id);
    $comment->author($post_from);
    $comment->email($post_mail);
    $comment->text($post_text);
	#if ($admin_data[3]){
	#    $comment->url($admin_data[3]);
	#}
	
	# MT3.0以上ならvisible値設定
	if ($mt->version_number() >= 3.0) {
		# $cfg{ApproveComment}='yes'の場合には、書き込みと同時に掲載を承諾する
		if ($cfg{ApproveComment} eq 'yes') {
			$comment->visible(1);
		} else {
			$comment->visible(0);
		}
	}
	
    $comment->save
        or die $comment->errstr;

	# メール送信
    if ($blog->email_new_comments) {
        require MT::Mail;
        my $author = $entry->author;
        $mt->set_language($author->preferred_language)
            if $author && $author->preferred_language;
        if ($author && $author->email) {
            my %head = (	To => $author->email,
							From => $comment->email || $author->email,
							Subject =>
								'[' . $blog->name . '] ' .
								$entry->title . &conv_euc2utf8(' への新しいコメント from MT4i')
                       );
            my $charset = $mt->{cfg}->PublishCharset || 'iso-8859-1';
            $head{'Content-Type'} = qq(text/plain; charset="$charset");
            my $body = &conv_euc2utf8('新しいコメントがウェブログ ') .
						$blog->name  . ' ' .
						&conv_euc2utf8('のエントリー #') . $entry->id . " (" .
						$entry->title . &conv_euc2utf8(') にありました');
			
			# 元記事へのリンク作成
			my $link_url = $entry->permalink;
			
            use Text::Wrap;
            $Text::Wrap::cols = 72;
            $body = Text::Wrap::wrap('', '', $body) . "\n$link_url\n\n" .
            $body = $body . "\n$link_url\n\n" .
              &conv_euc2utf8('IPアドレス:') . ' ' . $comment->ip . "\n" .
              &conv_euc2utf8('名前:') . ' ' . $comment->author . "\n" .
              &conv_euc2utf8('メールアドレス:') . ' ' . $comment->email . "\n" .
              &conv_euc2utf8('URL:') . ' ' . $comment->url . "\n\n" .
              &conv_euc2utf8('コメント:') . "\n\n" . $comment->text . "\n\n" .
              &conv_euc2utf8("-- \nfrom MT4i v$version\n");
            MT::Mail->send(\%head, $body);
        }
    }

	####################
	# リビルド
	
	# Indexテンプレート
	if ($cfg{RIT_ID} eq 'ALL') {
		$mt->rebuild_indexes( BlogID => $cfg{Blog_ID} )
			or die $mt->errstr;
	} else {
		my @tmp_RIT_ID = split(",", $cfg{RIT_ID});
		foreach my $indx_tmpl_id (@tmp_RIT_ID) {
			require MT::Template;
			my $tmpl_saved = MT::Template->load($indx_tmpl_id);
			$mt->rebuild_indexes( BlogID => $cfg{Blog_ID}, Template => $tmpl_saved, Force => 1 )
				or die $mt->errstr;
		}
	}
	
	# Archiveテンプレート
	if ($cfg{RAT_ID} eq 'ALL') {
		$mt->rebuild_entry( Entry => $entry )
			or die $mt->errstr;
	} else {
		my @tmp_RAT_ID = split(",", $cfg{RAT_ID});
		foreach my $arc_tmpl_id (@tmp_RAT_ID) {
			$mt->_rebuild_entry_archive_type( Entry => $entry,
											  Blog => $blog,
											  ArchiveType => $arc_tmpl_id )
				or die $mt->errstr;
		}
	}

	# 画面表示
	if ($mt->version_number() >= 3.0 && $cfg{ApproveComment} eq 'no') {
		$data = "ｺﾒﾝﾄが投稿されましたが、掲載は保留されています。<br>管理人による承諾後、掲載されます。<hr>";
	} else {
		$data = "ｺﾒﾝﾄが投稿されました<hr>";
	}
	my $href;
	if ($mode eq 'post') {
		$href = &make_href("comment", $rowid, 0, $eid, 0);
	} elsif ($mode eq 'post_rcm') {
		$href = &make_href("comment_rcm", $rowid, 0, $eid, 0);
	} elsif ($mode eq 'post_lnk') {
		$href = &make_href("comment_lnk", $rowid, 0, $eid, 0);
	}
	$data .="$nostr[0]<a href='$href'$akstr[0]>戻る</a>";
	&htmlout;
}

########################################
# Sub entryform - 新規Entry/Entry編集 フォーム
########################################
sub entryform {
	
	my ($org_title,$org_text,$org_text_more,$org_excerpt,$org_keywords,$org_convert_breaks,$org_created_on,$org_comment_cnt,$org_ent_status,$org_ent_allow_comments,$org_ent_allow_pings);
	my $rowid = $no;
	
	if ($eid == 0){
		$data = "<h4>新規Entryの作成</h4><hr>";
		
		# 現在日時の取得
		$ENV{TZ} = 'JST-9';
		my $time = time;
		my ($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime($time);
		$mon++;
		$year = 1900+$year;
		$mon = sprintf("%.2d",$mon);
		$mday = sprintf("%.2d",$mday);
		$hour = sprintf("%.2d",$hour);
		$sec = sprintf("%.2d",$sec);
		$min = sprintf("%.2d",$min);
		#$wday = sprintf("%s", ("日", "月", "火", "水", "木", "金", "土")[$wday]);
		$org_created_on = "$year-$mon-$mday $hour:$min:$sec";
	}else{
		
		$data = "<h4>Entryの編集</h4><hr>";
		
		# Entry検索
		require MT::Entry;
		my $entry = MT::Entry->load($eid);
		
		# 検索結果が0件の場合はメッセージ表示してSTOP（有り得ないけどな）
		if (!$entry) {
			$data = "Entry ID '".$eid."' は不正です。";
			&errorout;
			exit;      # exitする
		}
		
		# 編集なので、過去のデータを得る
		$org_title = &conv_euc_z2h($entry->title);
		$org_text = &conv_euc_z2h($entry->text);
		$org_text_more = &conv_euc_z2h($entry->text_more);
		$org_excerpt = &conv_euc_z2h($entry->excerpt);
		$org_keywords = &conv_euc_z2h($entry->keywords);
		$org_convert_breaks = &conv_euc_z2h($entry->convert_breaks);
		$org_created_on = $entry->created_on;
		$org_created_on =~ s/(\d\d\d\d)(\d\d)(\d\d)(\d\d)(\d\d)(\d\d)/$1-$2-$3 $4:$5:$6/;
		$org_comment_cnt = $entry->comment_count;
		$org_ent_status = $entry->status;
		$org_ent_allow_comments = $entry->allow_comments;
		$org_ent_allow_pings = $entry->allow_pings;
		
		# タイトルをエンコード
		$org_title =~ s/&/&amp;/g;
		$org_title =~ s/ /&nbsp;/g;
		$org_title =~ s/\</&lt;/g;
		$org_title =~ s/\>/&gt;/g;
		# 本文をエンコード
		$org_text =~ s/&/&amp;/g;
		$org_text =~ s/ /&nbsp;/g;
		$org_text =~ s/\</&lt;/g;
		$org_text =~ s/\>/&gt;/g;
		# 追記をエンコード
		$org_text_more =~ s/&/&amp;/g;
		$org_text_more =~ s/ /&nbsp;/g;
		$org_text_more =~ s/\</&lt;/g;
		$org_text_more =~ s/\>/&gt;/g;
		# 概要をエンコード
		$org_excerpt =~ s/&/&amp;/g;
		$org_excerpt =~ s/ /&nbsp;/g;
		$org_excerpt =~ s/\</&lt;/g;
		$org_excerpt =~ s/\>/&gt;/g;
		# キーワードをエンコード
		$org_keywords =~ s/&/&amp;/g;
		$org_keywords =~ s/ /&nbsp;/g;
		$org_keywords =~ s/\</&lt;/g;
		$org_keywords =~ s/\>/&gt;/g;
	}
	
	####################
	# 表示文字列生成
	my $href = &make_href("post", 0, 0, $eid, 0);
	$data .= "<form method=\"post\" action=\"$href\">";
	
	# カテゴリセレクタ
	my $cat_label;
	if ($eid){
		$cat_label = &check_category(MT::Entry->load($eid));
	}
	$data .= "ｶﾃｺﾞﾘ<br>";
	$data .= "<select name=\"entry_cat\">";
	$data .= "<option value=0>";
	require MT::Category;
	my @categories = MT::Category->load({blog_id => $cfg{Blog_ID}},
											{unique => 1});
	for my $category (@categories) {
		my $label;
		if ($cfg{CatDescReplace} eq "yes"){
			$label = &conv_euc_z2h($category->description);
		}else{
			$label = &conv_euc_z2h($category->label);
		}
		my $cat_id = $category->id;
		
		if ($cat_label eq $label){
			$data .= "<option value=$cat_id selected>$label<br>";
		}else{
			$data .= "<option value=$cat_id>$label<br>";
		}
	}
	$data .= "</select><br>";
	
	$data .= "ﾀｲﾄﾙ";
	$data .= "<br><input type=\"text\" name=\"entry_title\" value=\"$org_title\"><br>";
	$data .= "Entryの内容";
	$data .= "<br><textarea rows=\"4\" name=\"entry_text\">$org_text</textarea><br>";
	$data .= "Extended(追記)";
	$data .= "<br><textarea rows=\"4\" name=\"entry_text_more\">$org_text_more</textarea><br>";
	$data .= "Excerpt(概要)";
	$data .= "<br><textarea rows=\"4\" name=\"entry_excerpt\">$org_excerpt</textarea><br>";
	$data .= "ｷｰﾜｰﾄﾞ";
	$data .= "<br><textarea rows=\"4\" name=\"entry_keywords\">$org_keywords</textarea><br>";
	$data .= "投稿の状態<br>";
	$data .= "<select name=\"post_status\">";
	if (($eid && $org_ent_status == 1) || (!$eid && $blog->status_default == 1)) {
		$data .= "<option value=1 selected>下書き<br>";
		$data .= "<option value=2>公開<br>";
		if ($mt->version_number() >= 3.1) {
			$data .= "<option value=3>指定日<br>";
		}
	} elsif (($eid && $org_ent_status == 2) || (!$eid && $blog->status_default == 2)) {
		$data .= "<option value=1>下書き<br>";
		$data .= "<option value=2 selected>公開<br>";
		if ($mt->version_number() >= 3.1) {
			$data .= "<option value=3>指定日<br>";
		}
	} elsif (($eid && $org_ent_status == 3)) {
		$data .= "<option value=1>下書き<br>";
		$data .= "<option value=2>公開<br>";
		if ($mt->version_number() >= 3.1) {
			$data .= "<option value=3 selected>指定日<br>";
		}
	} else {
		$data .= "<option value=1>下書き<br>";
		$data .= "<option value=2 selected>公開<br>";
		if ($mt->version_number() >= 3.1) {
			$data .= "<option value=3>指定日<br>";
		}
	}
	$data .= "</select><br>";	
	
	$data .= "ｺﾒﾝﾄ<br>";
	$data .= "<select name=\"allow_comments\">";
	
	if (($eid && $org_ent_allow_comments == 0) || (!$eid && $blog->allow_comments_default == 0)) {
			$data .= "<option value=0 selected>なし<br>";
			$data .= "<option value=1>ｵｰﾌﾟﾝ<br>";
			$data .= "<option value=2>ｸﾛｰｽﾞ<br>";
	} elsif (($eid && $org_ent_allow_comments == 1) || (!$eid && $blog->allow_comments_default == 1)) {
			$data .= "<option value=0>なし<br>";
			$data .= "<option value=1 selected>ｵｰﾌﾟﾝ<br>";
			$data .= "<option value=2>ｸﾛｰｽﾞ<br>";
	} else {
			$data .= "<option value=0>なし<br>";
			$data .= "<option value=1>ｵｰﾌﾟﾝ<br>";
			$data .= "<option value=2 selected>ｸﾛｰｽﾞ<br>";
	}
	$data .= "</select><br>";
	
	$data .= "ﾄﾗｯｸﾊﾞｯｸを受けつける<br>";
	if (($eid && $org_ent_allow_pings) || (!$eid && $blog->allow_pings_default == 1)) {
		$data .= "<INPUT TYPE=checkbox name=\"allow_pings\" value=\"1\" CHECKED><br>";
	}else{
		$data .= "<INPUT TYPE=checkbox name=\"allow_pings\" value=\"1\"><br>";
	}
	
	## テキストフォーマットのロード
	my $filters = $mt->all_text_filters;
	my $text_filters = [];
	for my $filter (keys %$filters) {
		push @{ $text_filters }, {
			filter_key => $filter,
			filter_label => $filters->{$filter}{label},
		};
	}
	# ソート
	$text_filters = [ sort { $a->{filter_key} cmp $b->{filter_key} } @{ $text_filters } ];
	# 「なし」を追加
	unshift @{ $text_filters }, {
		filter_key => '0',
		filter_label => 'なし',
	};
	# 描画
	$data .= "ﾃｷｽﾄﾌｫｰﾏｯﾄ<br>";
	$data .= '<select name="convert_breaks">';
	foreach my $filter ( @{ $text_filters } ) {
		my $selected;
		if (($org_convert_breaks eq $filter->{filter_key}) || (!$org_convert_breaks && $convert_paras eq $filter->{filter_key})) {
			$selected = ' selected';
		}
		$data .= "<option value=\"$filter->{filter_key}\"$selected>$filter->{filter_label}</option>";
	}
	$data .= '</select><br>';
	
	$data .= "作成日時<br>";
	$data .= "<input type=\"text\" name=\"entry_created_on\" value=\"$org_created_on\"><br>";
	
	$data .= "<input type=\"hidden\" name=\"id\" value=\"$cfg{Blog_ID}\">";
	$data .= "<input type=\"hidden\" name=\"mode\" value=\"entry\">";
	$data .= "<input type=\"hidden\" name=\"no\" value=\"$rowid\">";
	$data .= "<input type=\"hidden\" name=\"eid\" value=\"$eid\">";
	if ($key){
		$data .= "<input type=\"hidden\" name=\"key\" value=\"$key\">";
	}
	$data .= "<input type=\"submit\" value=\"送信\">";
	$data .= "</form>";
	$data .= "<hr>";
	$href = &make_href("", 0, 0, 0, 0);
	$data .= "$nostr[0]<a href='$href'$akstr[0]>一覧へ戻る</a>";
	&htmlout;
}

########################################
# Sub Entry - 新規Entry投稿->表示処理
########################################
sub entry {
	
	my $rowid = $no;
	$no--;
	
	# 投稿内容を一旦EUC-JPに変換
	&$jcnv(\$entry_title, 'euc', 'sjis');
	&$jcnv(\$entry_text, 'euc', 'sjis');
	&$jcnv(\$entry_text_more, 'euc', 'sjis');
	&$jcnv(\$entry_excerpt, 'euc', 'sjis');
	&$jcnv(\$entry_keywords, 'euc', 'sjis');
	
	# 半角スペース'&nbsp;'をデコード
	$entry_title =~ s/&nbsp;/ /g;
	$entry_text =~ s/&nbsp;/ /g;
	$entry_text_more =~ s/&nbsp;/ /g;
	$entry_excerpt =~ s/&nbsp;/ /g;
	$entry_keywords =~ s/&nbsp;/ /g;

	####################
	# 必須入力項目をチェック
	# タイトル、テキストのどちらかの入力が無ければエラー
	if((!$entry_title)||(!$entry_text))
	{
		$data .="Error!<br>未入力項目があります。「タイトル」と「Entryの内容」は必須です。<br>";
		my $href = &make_href("entryform", 0, 0, $eid, 0);
		$data .="$nostr[0]<a href=\"$href\"$akstr[0]>戻る</a>";
		&errorout;
		return;
	}
	# 作成日時の入力が無ければエラー
	if (!$entry_created_on) {
		$data .="Error!<br>未入力項目があります。「作成日時」は必須です。<br>";
		my $href = &make_href("entryform", 0, 0, $eid, 0);
		$data .="$nostr[0]<a href=\"$href\"$akstr[0]>戻る</a>";
		&errorout;
		return;
	}
	require MT::Author;
	my $author = MT::Author->load({ name => $cfg{AuthorName} });	
	if (!$author) {
		$data = "\"$cfg{AuthorName}\"がAuthorとして登録されていません。<br>";
		&errorout;
		exit;      # exitする
	}
	
	# 投稿された文字列の半角カナを全角に変換
	if ($jcd == 0) {
		&jcode::h2z_euc($entry_title);
		&jcode::h2z_euc($entry_text);
		&jcode::h2z_euc($entry_text_more);
		&jcode::h2z_euc($entry_excerpt);
		&jcode::h2z_euc($entry_keywords);
	} else {
		Jcode->new(\$entry_title, 'euc')->h2z;
		Jcode->new(\$entry_text, 'euc')->h2z;
		Jcode->new(\$entry_text_more, 'euc')->h2z;
		Jcode->new(\$entry_excerpt, 'euc')->h2z;
		Jcode->new(\$entry_keywords, 'euc')->h2z;
	}
	# PublishCharsetに変換
	if ($conv_in ne 'euc') {
		&$jcnv(\$entry_title, $conv_in, 'euc');
		&$jcnv(\$entry_text, $conv_in, 'euc');
		&$jcnv(\$entry_text_more, $conv_in, 'euc');
		&$jcnv(\$entry_excerpt, $conv_in, 'euc');
		&$jcnv(\$entry_keywords, $conv_in, 'euc');
	}
	
	require MT::Entry;
	my $entry;
	if ($eid){
		$entry = MT::Entry->load($eid);
	}else{
		$entry = MT::Entry->new;
	}
	$entry->blog_id($blog->id);
	$entry->status($post_status);
	$entry->author_id($author->id);
	$entry->title($entry_title);
	$entry->text($entry_text);
	$entry->text_more($entry_text_more);
	$entry->excerpt($entry_excerpt);
	$entry->keywords($entry_keywords);
	if ($allow_pings == 1){
		$entry->allow_pings(1);
	}else{
		$entry->allow_pings(0);
	}
	$entry->allow_comments($allow_comments);
	$entry->convert_breaks($text_format);
	$entry_created_on =~ s/(\d\d\d\d)-(\d\d)-(\d\d) (\d\d):(\d\d):(\d\d)/$1$2$3$4$5$6/;
	$entry->created_on($entry_created_on);
	$entry->save
		or die $entry->errstr;
	
	if ($entry_cat) {
		require MT::Placement;
		my $place = MT::Placement->load({ blog_id => $cfg{Blog_ID} , entry_id => $entry->id });
		
		if (!$place){
			$place = MT::Placement->new;
		}
		$place->entry_id($entry->id);
		$place->blog_id($cfg{Blog_ID});
		$place->category_id($entry_cat);
		$place->is_primary(1);
		$place->save
			or die $place->errstr;
	}
	if ($eid){
		$data = "Entryは修正されました<hr>";
	}else{
		$data = "新規Entryが作成されました<hr>";
	}
	
	# リビルド
    $mt->rebuild_indexes( Blog => $blog )
        or die $mt->errstr;
    $mt->rebuild_entry( Entry => $entry )
        or die $mt->errstr;
	
	####################
	# 更新ping送信
	# statusがpublishの場合のみping送信
	if ($post_status == 2){
		require MT::XMLRPC;
		if ($blog->ping_others){
			my (@updateping_urls) = split(/\n/,$blog->ping_others);
			for my $url (@updateping_urls) {
				MT::XMLRPC->ping_update('weblogUpdates.ping', $blog,
					$url)
					or die MT::XMLRPC->errstr;
			}
		}
	}
	
	my $href = &make_href("", 0, 0, 0, 0);
	$data .= "$nostr[0]<a href=\"$href\"$akstr[0]>一覧へ戻る</a>";
	&htmlout;
}

########################################
# Sub Entry_del - Entry削除
########################################
sub entry_del {
	
	my $rowid = $no;
	$no--;
	
	require MT::Entry;
	my $entry = MT::Entry->load($eid);
	if (!$entry) {
		$data = "entry_del::Entry ID '".$eid."' は不正です。";
		&errorout;
		exit;      # exitする
	}
	
	$entry->remove;
	
	# リビルド
    $mt->rebuild_indexes( Blog => $blog )
        or die $mt->errstr;
    $mt->rebuild_entry( Entry => $entry )
        or die $mt->errstr;
	
	$data = "Entryが削除されました<hr>";
	my $href = &make_href("", 0, 0, 0, 0);
	$data .= "$nostr[0]<a href='$href'$akstr[0]>一覧へ戻る</a>";
	&htmlout;
}

########################################
# Sub Comment_del - コメント削除
########################################
sub comment_del {
	
	my $rowid = $no;
	$no--;
	
	####################
	# commentを探す
	require MT::Comment;
	my $comment = MT::Comment->load($page);	# コメント番号は$pageで渡す
	if (!$comment) {
		$data = "comment_del::Comment ID '".$page."' は不正です。";
		&errorout;
		exit;      # exitする
	}
	$comment->remove()
		or die $comment->errstr;
	
	#このcommentが属するEntryを探す
	require MT::Entry;
	my $entry = MT::Entry->load($comment->entry_id);
	if (!$entry) {
		$data = "comment_del::Entry ID '".$comment->entry_id."' は不正です。";
		&errorout;
		exit;      # exitする
	}
	
	# リビルド
    $mt->rebuild_indexes( Blog => $blog )
        or die $mt->errstr;
    $mt->rebuild_entry( Entry => $entry )
        or die $mt->errstr;
	
	$data = "コメントが削除されました<hr>";
	my $href = &make_href("comment", $rowid, 0, $eid, 0);
	$data .= "$nostr[0]<a href=\'$href\'$akstr[0]>コメント一覧へ戻る</a>";
	&htmlout;
}

########################################
# Sub Trackback_del - トラックバック削除
########################################
sub trackback_del {
	
	my $rowid = $no;
	$no--;
	
	####################
	# pingを探す
	require MT::TBPing;
	my $tbping = MT::TBPing->load($page);	# トラックバック番号は$pageで渡す
	if (!$tbping) {
		$data = "trackback_del::MTPing ID '".$page."' は不正です。";
		&errorout;
		exit;      # exitする
	}
	$tbping->remove()
		or die $tbping->errstr;
	
	#このtbpingが属するTrackbackを探す
	require MT::Trackback;
	my $trackback = MT::Trackback->load($tbping->tb_id);
	if (!$trackback) {
		$data = "trackback_del::Trackback ID '".$tbping->tb_id."' は不正です。";
		&errorout;
		exit;      # exitする
	}
	
	#このTrackbackが属するEntryを探す
	require MT::Entry;
	my $entry = MT::Entry->load($trackback->entry_id);
	if (!$entry) {
		$data = "trackback_del::Entry ID '".$trackback->entry_id."' は不正です。";
		&errorout;
		exit;      # exitする
	}
	
	# リビルド
    $mt->rebuild_indexes( Blog => $blog )
        or die $mt->errstr;
    $mt->rebuild_entry( Entry => $entry )
        or die $mt->errstr;
	
	$data = "ﾄﾗｯｸﾊﾞｯｸが削除されました<hr>";
	my $href = &make_href("trackback", $rowid, 0, $eid, 0);
	$data .= "$nostr[0]<a href=\'$href\'$akstr[0]>ﾄﾗｯｸﾊﾞｯｸ一覧へ戻る</a>";
	&htmlout;
}

########################################
# Sub Trackback_ipban - このIPからのトラックバックを禁止＆全削除
########################################
sub trackback_ipban {
	
	my $rowid = $no;
	$no--;
	
	####################
	# pingを探す
	require MT::TBPing;
	my $tbping = MT::TBPing->load($page);	# トラックバック番号は$pageで渡す
	if (!$tbping) {
		$data = "trackback_ipban::MTPing ID '".$page."' は不正です。";
		&errorout;
		exit;      # exitする
	}
	
	require MT::IPBanList;
	my $ban = MT::IPBanList->new;
	$ban->blog_id($blog->id);
	$ban->ip($tbping->ip);
	$ban->save
		or die $ban->errstr;
	
	####################
	# そのIPから送信されたトラックバックを全て探す
	my @tbpings = MT::TBPing->load(
			{ blog_id => $cfg{Blog_ID}, ip => $tbping->ip});	
	
	for my $tbping (@tbpings) {
		
		#このtbpingが属するTrackbackを探す
		require MT::Trackback;
		my $trackback = MT::Trackback->load($tbping->tb_id);
		if (!$trackback) {
			$data = "trackback_ipban::Trackback ID '".$tbping->tb_id."' は不正です。";
			&errorout;
			exit;      # exitする
		}
		
		#このTrackbackが属するEntryを探す
		require MT::Entry;
		my $entry = MT::Entry->load($trackback->entry_id);
		if (!$entry) {
			$data = "trackback_ipban::Entry ID '".$trackback->entry_id."' は不正です。";
			&errorout;
			exit;      # exitする
		}
		
		$data .= &conv_euc_z2h($tbping->excerpt)."<hr>";
		
		# トラックバックping削除
		$tbping->remove()
			or die $tbping->errstr;

		# entryのリビルド
		$mt->rebuild_entry( Entry => $entry )
			or die $mt->errstr;
	}
	
	$data = "IPを禁止リストに追加し、".@tbpings."件のﾄﾗｯｸﾊﾞｯｸを削除しました。<hr>";
	my $href = &make_href("trackback", $rowid, 0, $eid ,0);
	$data .= "$nostr[0]<a href=\'$href\'$akstr[0]>ﾄﾗｯｸﾊﾞｯｸ一覧へ戻る</a>";
	&htmlout;
	
	# indexのリビルド
	$mt->rebuild_indexes( Blog => $blog )
		or die $mt->errstr;
}

########################################
# Sub Comment_ipban - このIPからのコメントを禁止＆全削除
########################################
sub comment_ipban {
	
	my $rowid = $no;
	$no--;
	
	####################
	# commentを探す
	require MT::Comment;
	my $comment = MT::Comment->load($page);	# コメント番号は$pageで渡す
	if (!$comment) {
		$data = "comment_ipban::Comment ID '".$page."' は不正です。";
		&errorout;
		exit;      # exitする
	}
	
	require MT::IPBanList;
	my $ban = MT::IPBanList->new;
	$ban->blog_id($blog->id);
	$ban->ip($comment->ip);
	$ban->save
		or die $ban->errstr;
	
	####################
	# そのIPから送信されたコメントを全て探す
	my @comments = MT::Comment->load(
			{ blog_id => $cfg{Blog_ID}, ip => $comment->ip});
	
	for my $comment (@comments) {
		
		require MT::Entry;
		my $entry = MT::Entry->load($comment->entry_id);
		if (!$entry) {
			$data = "comment_ipban::Entry ID '".$comment->entry_id."' は不正です。";
			&errorout;
			exit;      # exitする
		}
		
		# コメント削除
		$comment->remove()
			or die $comment->errstr;
		
		# entryのリビルド
	    $mt->rebuild_entry( Entry => $entry )
	        or die $mt->errstr;
		
	}
	
	$data = "IPを禁止リストに追加し、".@comments."件のコメントを削除しました。<hr>";
	my $href = &make_href("comment", $rowid, 0, $eid, 0);
	$data .= "$nostr[0]<a href=\'$href\'$akstr[0]>コメント一覧へ戻る</a>";
	&htmlout;
	
	# indexのリビルド
	$mt->rebuild_indexes( Blog => $blog )
		or die $mt->errstr;
}

########################################
# Sub Email_comments - コメントのメール通知制御
########################################
sub email_comments {
	
	if ($email_new_comments){
		$blog->email_new_comments(0);
	}else{
		$blog->email_new_comments(1);
	}
	
	$blog->save
		or die $blog->errstr;
	
	if ($email_new_comments){
		$data = "コメントのメール通知を停止しました。<hr>";
	}else{
		$data = "コメントのメール通知を再開しました。<hr>";
	}
	
	my $href = &make_href("", 0, $page, 0, 0);
	$data .= "$nostr[0]<a href=\"$href\"$akstr[0]>一覧へ戻る</a>";
	&htmlout;

}

########################################
# Sub Confirm - 各種確認
########################################
sub confirm {
	
	my $rowid = $no;
	
	# コメントIDは$pageで受け渡し
	if ($mode eq "confirm_comment_del"){
		
		require MT::Comment;
		my $comment = MT::Comment->load($page);	# コメント番号は$pageで渡す
		if (!$comment) {
			$data = "confirm_comment_del::Comment ID '".$page."' は不正です。";
			&errorout;
			exit;      # exitする
		}
		$data .="本当に以下のコメントを削除してよろしいですか？<br>";
		
		my $href = &make_href("comment", $rowid, $page , $eid, 0);
		$data .= "<a href='$href'>[キャンセルする]</a><br>";
		$href = &make_href("comment_del", $rowid, $page, $eid, 0);
		$data .="<a href='$href'>[削除する]</a><hr>";
		
		$data .= "Author:".&conv_euc_z2h($comment->author)."<br>";
		$data .= "Text:".&conv_euc_z2h($comment->text)."<br>";
		
	}
	elsif ($mode eq "confirm_entry_del"){

		require MT::Entry;
		my $entry = MT::Entry->load($eid);
		if (!$entry) {
			$data = "confirm_entry_del::Entry ID '".$eid."' は不正です。";
			&errorout;
			exit;      # exitする
		}
		
		require MT::Author;
		my $author = MT::Author->load({ id => $entry->author_id });	
		my $author_name = "";
		if ($author) {
			$author_name = &conv_euc_z2h($author->name);
		}
		
		$data .="本当に以下のEntryを削除してよろしいですか？<br>";
		
		my $href = &make_href("individual", $rowid, 0 , $eid, 0);
		$data .= "<a href='$href'>[キャンセルする]</a><br>";
		$href = &make_href("entry_del", $rowid, 0, $eid, 0);
		$data .="<a href='$href'>[削除する]</a><hr>";
		
		if ($author_name){
			$data .= "Author:".$author_name."<br>";
		}
		$data .= "Text:".&conv_euc_z2h($entry->text)."<br>";
		
	}
	elsif ($mode eq "confirm_trackback_del"){
		
		require MT::TBPing;
		my $tbping = MT::TBPing->load($page);	# トラックバック番号は$pageで渡す
		if (!$tbping) {
			$data = "confirm_trackback_del::MTPing ID '".$page."' は不正です。";
			&errorout;
			exit;      # exitする
		}
		
		$data .="本当に以下のTBを削除してよろしいですか？<br>";
		my $href = &make_href("trackback", $rowid, $page , $eid, 0);
		$data .= "<a href='$href'>[キャンセルする]</a><br>";
		$href = &make_href("trackback_del", $rowid, $page, $eid, 0);
		$data .="<a href='$href'>[削除する]</a><hr>";
		
		$data .= "BlogName:".&conv_euc_z2h($tbping->blog_name)."<br>";
		$data .= "Title:".&conv_euc_z2h($tbping->title)."<br>";
		$data .= "Excerpt:".&conv_euc_z2h($tbping->excerpt)."<br>";
		
	}
	elsif ($mode eq "confirm_trackback_ipban"){
		
		require MT::TBPing;
		my $tbping = MT::TBPing->load($page);	# トラックバック番号は$pageで渡す
		if (!$tbping) {
			$data = "confirm_trackback_ipban::MTPing ID '".$page."' は不正です。";
			&errorout;
			exit;      # exitする
		}
		
		$data .="本当にこのIPアドレス(".$tbping->ip.")からの書き込みを禁止＆全削除してよろしいですか？<br>";
		my $href = &make_href("trackback", $rowid, $page , $eid, 0);
		$data .= "<a href='$href'>[キャンセルする]</a><br>";
		$href = &make_href("trackback_ipban", $rowid, $page, $eid, 0);
		$data .="<a href='$href'>[禁止＆全削除する]</a><br>※件数が多い場合はリビルドに時間がかかりタイムアウトすることがありますが、処理は正常に行われます。<hr>";
		$data .="\<対象ﾄﾗｯｸﾊﾞｯｸ一覧\><br>";
		
		####################
		# そのIPから送信されたトラックバックを全て探す
		my @tbpings = MT::TBPing->load(
				{ blog_id => $cfg{Blog_ID}, ip => $tbping->ip});	
		for my $tbping (@tbpings) {
			$data .= &conv_euc_z2h($tbping->blog_name)." -> ";
			$data .= &conv_euc_z2h($tbping->title)."(";
			$data .= &conv_euc_z2h($tbping->created_on).")<br>";
		}
	}
	elsif ($mode eq "confirm_comment_ipban"){
		
		require MT::Comment;
		my $comment = MT::Comment->load($page);	# コメント番号は$pageで渡す
		if (!$comment) {
			$data = "confirm_comment_ipban::Comment ID '".$page."' は不正です。";
			&errorout;
			exit;      # exitする
		}
		
		$data .="本当にこのIPｱﾄﾞﾚｽ(".$comment->ip.")からの書き込みを禁止＆全削除してよろしいですか？<br>";
		my $href = &make_href("comment", $rowid, $page , $eid, 0);
		$data .= "<a href='$href'>[ｷｬﾝｾﾙする]</a><br>";
		$href = &make_href("comment_ipban", $rowid, $page, $eid, 0);
		$data .="<a href='$href'>[禁止＆全削除する]</a><br>※件数が多い場合はﾘﾋﾞﾙﾄﾞに時間がかかりﾀｲﾑｱｳﾄすることがありますが、処理は正常に行われます。<hr>";
		$data .="\<対象ｺﾒﾝﾄ一覧\><br>";
		
		####################
		# そのIPから送信されたコメントを全て探す
		my @comments = MT::Comment->load(
				{ blog_id => $cfg{Blog_ID}, ip => $comment->ip});
		
		for my $comment (@comments) {
			
			require MT::Entry;
			my $entry = MT::Entry->load($comment->entry_id);
			if (!$entry) {
				$data = "confirm_comment_ipban::Entry ID '".$comment->entry_id."' は不正です。";
				&errorout;
				exit;      # exitする
			}
			
			my $comment_author = &conv_euc_z2h($comment->author);
			if ($cfg{AdmNM} eq $comment_author){
				$data .= '<font color="red">'.$comment_author.'</font>'." -> ".&conv_euc_z2h($entry->title);
			}else{
				$data .= $comment_author." -> ".&conv_euc_z2h($entry->title);
			}
			$data .= "(".&conv_euc_z2h($comment->created_on).")<br>";
		}
		
	}else{
		$data .="confirm::mode '".$mode."' は不正です。<br>";
	}
	
	&htmlout;
}

########################################
# Sub Admindoor - 管理者用URLを表示
########################################
sub admindoor {
	my $href;
	if ($pw_text eq $cfg{AdminPassword}){
		$data .= '管理者用URLは';
		$href = &make_href("", 0, 0, 0, 0);
		$href .= '&key='.&enc_crypt($cfg{AdminPassword}.$cfg{Blog_ID});
		$data .= "<a href=\"$href\">こちら</a>";
		$data .= 'です。ﾘﾝｸ先をﾌﾞｯｸﾏｰｸした後、速やかに「mt4i Manager」にて"AdminDoor"の値を"no"に変更してください。<br>';
	}else{
		$data .= "ﾊﾟｽﾜｰﾄﾞが違います<hr>";
	}
	$key = "";
	$href = &make_href("", 0, 0, 0, 0);
	$data .= "$nostr[0]<a href='$href'$akstr[0]>一覧へ戻る</a>";
	&htmlout;
}

########################################
# Sub Separate - 単記事・コメント本文の分割
########################################

sub separate {
	my $text = $_[0];
	my $rowid = $_[1];
	
	# 区切り文字列を配列に格納しておく
	my @sprtstrlist = split(",",$cfg{SprtStr});
	
	# 本文のバイト数を求めておく
	my $maxlen = &lenb_euc($text);
	
	# 初回に分割位置を決め、$sprtbyteへ格納
	if (!$sprtbyte) {
		$sprtpage = 1;
		my $i = 0;
		$sprtbyte = "0";
		while ($i < $maxlen - $cfg{SprtLimit}) {
			my $tmpstart = $i;
			my $tmpend;
			
			if ($tmpstart + $cfg{SprtLimit} > $maxlen) {
				$tmpend = $maxlen - $tmpstart;
			} else {
				$tmpend = $cfg{SprtLimit};
			}
			
			# 区切り文字列の検出
			my $sprtstart;
			my $tmptext = &midb_euc($text, $tmpstart, $tmpend);
			foreach my $tmpsprtstr (@sprtstrlist) {
				if ($tmptext =~ /(.*)$tmpsprtstr/s) {
					$tmptext = $1;
					$sprtstart = &lenb_euc($tmptext) + &lenb_euc($tmpsprtstr);
					last;
				}
			}
			if (!$sprtstart) {
				$sprtstart = $maxlen;
			}
			
			$sprtstart = $sprtstart + $tmpstart;
			
			# 分割位置を$sprtbyteに格納
			if ($sprtstart < $maxlen) {
				$sprtbyte .= ",$sprtstart";
			}
			$i = $sprtstart + 1;
		}
	}
	
	# $sprtbyteを読み取る
	my @argsprtbyte = split(/,/, $sprtbyte);
	my $sprtstart = $argsprtbyte[$sprtpage - 1];
	my $sprtend;
	if ($sprtpage - 1 < $#argsprtbyte) {
		$sprtend = $argsprtbyte[$sprtpage] - $sprtstart;
	} else {
		$sprtend = $maxlen - $sprtstart;
	}
	
	####################
	# 本文文字列生成
	
	my $tmptext = "";
	my $href = &make_href($mode, $rowid, 0, $eid, 0);
	
	# ページリンク（上）
	$tmptext .= "&lt; ﾍﾟｰｼﾞ移動:";
	for (my $i = 1; $i <= $#argsprtbyte + 1; $i++)  {
		if ($i == $sprtpage) {
			$tmptext .= " $i";
		} else {
			$tmptext .= " <a href=\"$href&amp;sprtpage=$i&amp;sprtbyte=$sprtbyte\">$i</a>";
		}
	}
	$tmptext .= " &gt;<br>";
	
	# 記事本文
	$tmptext .= &midb_euc($text, $sprtstart, $sprtend);
	
	# ページリンク（下）
	$tmptext .= "<br>&lt; ﾍﾟｰｼﾞ移動:";
	for (my $i = 1; $i <= $#argsprtbyte + 1; $i++)  {
		if ($i == $sprtpage) {
			$tmptext .= " $i";
		} else {
			$tmptext .= " <a href=\"$href&amp;sprtpage=$i&amp;sprtbyte=$sprtbyte\">$i</a>";
		}
	}
	$tmptext .= " &gt;";
	
	return $tmptext;
}

########################################
# Sub Conv_euc_z2h - →EUC-JP／全角→半角変換
########################################

sub conv_euc_z2h {
	my $tmpstr = $_[0];
	# 第一引数をEUC-JPに変換
	if ($conv_in ne "euc") {
		if ($conv_in eq "utf8" && $ecd == 1) {
			$tmpstr = encode("cp932",decode("utf8",$tmpstr));
			$tmpstr = encode("euc-jp",decode("shiftjis",$tmpstr));
		} else {
			&$jcnv(\$tmpstr,'euc', $conv_in);
		}
	}
	
	# 表示文字列の全角文字を半角に変換
	if ($cfg{Z2H} eq "yes") {
		if ($jcd == 0) {
			&jcode::z2h_euc(\$tmpstr);
			&jcode::tr(\$tmpstr, 'Ａ-Ｚａ-ｚ０-９／！？（）＝＆', 'A-Za-z0-9/!?()=&');
		} else {
			$tmpstr = Jcode->new($tmpstr,'euc')->z2h->tr('Ａ-Ｚａ-ｚ０-９／！？（）＝＆', 'A-Za-z0-9/!?()=&');
		}
	}
	return $tmpstr;
}

########################################
# Sub Img_Url_Conv - 画像URLのスラッシュを%2Fに変換
########################################

sub img_url_conv {
	my $tmpstr = $_[0];
	my $str = "";
	
	# ループしながら<img>タグ内URLの置換
	while ($tmpstr =~ /(<img(?:[^"'>]|"[^"]*"|'[^']*')*src=)("[^"]*"|'[^']*')((?:[^"'>]|"[^"]*"|'[^']*')*>)/i) {
		my $front = $` . $1;
		my $url = $2;
		my $end = $3 . $';
		
		# ダブル・シングルクォーテーションを取り除く
		$url =~ s/"//g;
		$url =~ s/'//g;
		
		# "/"→"%2F"
		$url =~ s/\//\%2F/g;
		
		# ダブルクォーテーションを補いつつ結合
		$str .= "$front\"" . $url;
		$tmpstr = "\"$end";
	}
	$str .= $tmpstr;
	return $str;
}

### valium add start
#################################################################
# Sub Get_mt4ilink - MT4iへのリンクを取得
#
# リンク先のHTMLを取得してMT4iで閲覧するのに適したリンク先を
# 取得する。具体的には [rel|rev]="alternate" のlinkタグのうち、
# title="MT4i" あるいは media="handheld" の属性をもつタグで指
# 定されている href を返す。両方あった場合は title="MT4i" の方
# を優先する見つからなければ空文字列を返す。
#
#################################################################
sub get_mt4ilink {
  my $url = $_[0];

  require LWP::Simple;
  # リンク先コンテンツ取得
  my $content = LWP::Simple::get($url);
  if (!$content) {
    # 取得失敗
    return "";
  }

  # ヘッダーの取り出し
  my $pattern = "<[\s\t]*?head[\s\t]*?>(.*?)<[\s\t]*?/[\s\t]*?head[\s\t]*?>";
  my @head = ($content =~ m/$pattern/is);
  if (!$head[0]) {
    return "";
  }

  # linkタグの取り出し
  $pattern = "<[\s\t]*?link[\s\t]*?(.*?)[\s\t/]*?>";
  my @links = ($head[0] =~ m/$pattern/isg);

  my $mt4ilink = ""; # titile="MT4i"
  my $hhlink   = ""; # media="handheld"

  found : foreach my $link ( @links ) {
    my $title = "";
    my $rel = "";
    my $media = "";
    my $href = "";
    if ($link =~ /title[\s\t]*?=[\s\t]*?([^\s\t]*)/i) {
      $title = $1;
      $title =~ s/"//g;
      $title =~ s/'//g;
    }
    if ($link =~ /rel[\s\t]*?=[\s\t]*?([^\s\t]*)/i) {
      $rel = $1;
    } elsif ($link =~ /rev[\s\t]*?=[\s\t]*?([^\s\t]*)/i) {
      $rel = $1;
    }
    if ($rel) {
      $rel =~ s/"//g;
      $rel =~ s/'//g;
    }
    if ($link =~ /media[\s\t]*?=[\s\t]*?([^\s\t]*)/i) {
      $media = $1;
      $media =~ s/"//g;
      $media =~ s/'//g;
    }
    if ($link =~ /href[\s\t]*?=[\s\t]*?([^\s\t]*)/i) {
      $href = $1;
      $href =~ s/"//g;
      $href =~ s/'//g;
    }
    if ((lc $rel) eq 'alternate') {
      if ((lc $title) eq 'mt4i') {
        $mt4ilink = $href;
        last found;
      } elsif ((lc $media) eq 'handheld') {
        if (!$hhlink) {
          $hhlink = $href;
        }
      }
    }
  }

  if ($mt4ilink) {
    return $mt4ilink;
  }
  return $hhlink;
}
### valium add end

########################################
# Sub Chtmltrans - リンクのURLをchtmltrans経由に変換
# 参考：Perlメモ→http://www.din.or.jp/~ohzaki/perl.htm#HTML_Tag
########################################

sub chtmltrans {
	my $tmpstr = $_[0];
	my $ref_rowid = $_[1];
	my $ref_eid = $_[2];
	my $str = "";
	
	# ループしながらURLの置換
	while ($tmpstr =~ /(<a(?:[^"'>]|"[^"]*"|'[^']*')*href=)("[^"]*"|'[^']*')((?:[^"'>]|"[^"]*"|'[^']*')*>)/i) {
		my $front = $` . $1;
		my $url = $2;
		#my $end = $3 . $';
		my $end = $3;
		my $backward = $';
		my $tmpfront = $1;
		my $tmpend = $3;
		### valium add start
		my $lnkstr = "";
		### valium add end

		my $title;
		
		# title属性を取り出す
		if ($tmpfront =~ /title=/i) {
			my $tmpstr = $tmpfront;
			$tmpstr =~ s/.*<a(?:[^"'>]|"[^"]*"|'[^']*')*title=("[^"]*"|'[^']*')(?:[^"'>]|"[^"]*"|'[^']*')*\Z/$1/i;
			# ダブル・シングルクォーテーションを取り除く
			$tmpstr =~ s/"//g;
			$tmpstr =~ s/'//g;
			$title = $tmpstr;
		} elsif ($tmpend =~ /title=/i) {
			my $tmpstr = $tmpend;
			$tmpstr =~ s/\A.*(?:[^"'>]|"[^"]*"|'[^']*')*title=("[^"]*"|'[^']*')(?:[^"'>]|"[^"]*"|'[^']*')*>/$1/i;
			# ダブル・シングルクォーテーションを取り除く
			$tmpstr =~ s/"//g;
			$tmpstr =~ s/'//g;
			$title = $tmpstr;
		}
		
		if ($title !~ /$cfg{ExitChtmlTrans}/) {
			if ($url =~ m/.*http:\/\/www.amazon.co.jp\/exec\/obidos\/ASIN\/.*/g) {
				# Amazon個別商品リンクならi-mode対応へ変換
				$url =~ s/ASIN/dt\/i\/tg\/aa\/xml\/glance\/-/g;
				
				# ダブル・シングルクォーテーションを取り除く
				$url =~ s/"//g;
				$url =~ s/'//g;
			} elsif ($url =~ m/.*http:\/\/www.amazlet.com\/browse\/ASIN\/.*/g) {
				# Amazletへのリンクなら、Amazonのi-mode対応へ変換
				$url =~ s/www.amazlet.com\/browse\/ASIN/www.amazon.co.jp\/exec\/obidos\/dt\/i\/tg\/aa\/xml\/glance\/-/g;
				
				# ダブル・シングルクォーテーションを取り除く
				$url =~ s/"//g;
				$url =~ s/'//g;
			} elsif ($cfg{MyArcURL} && $url =~ m/.*$cfg{MyArcURL}.*/g && $mode eq 'individual' && (lc $cfg{Ainori}) eq 'no') {
				# 自サイト内リンク&あいのりOFFならMT4i経由に変換
				# ただし、遷移がややこしくなって面倒なので1階層のみ
				$url =~ /$cfg{MyArcURL}/;
				my $eid = $1;
				$eid =~ s/^0+//;
				$url = &make_href("individual_lnk", $ref_rowid, 0, $eid, $ref_eid);
				
				# ダブル・シングルクォーテーションを取り除く
				$url =~ s/"//g;
				$url =~ s/'//g;
			} else {
				### valium add start
				my $mt4ilink = "";
				if ((lc $cfg{Ainori}) eq 'yes') {
					# リンク先を取得
					$mt4ilink = &get_mt4ilink($url);
				}
				if ($mt4ilink) {
					$url = $mt4ilink;
					$lnkstr = $mt4ilinkstr;
				} else {
				### valium add end
					# ダブル・シングルクォーテーションを取り除く
					$url =~ s/"//g;
					$url =~ s/'//g;
					
					# "/"→"@2F"、"?"→"@3F"、"+"→"@2B"
					$url =~ s/\//\@2F/g;
					$url =~ s/\?/\@3F/g;
					$url =~ s/\+/\@2B/g;
					
					# URLを生成
					my $chtmltransurl;
					$chtmltransurl .= 'http://wmlproxy.google.com/chtmltrans/h=ja/u=';
					$url = $chtmltransurl . $url . "/c=0";
				### valium add start
				}
				### valium add end
			}
		} else {
			# ダブル・シングルクォーテーションを取り除く
			$url =~ s/"//g;
			$url =~ s/'//g;
			# 携帯対応マーク
			$lnkstr = $ExitChtmlTransStr;
		}
		# ダブルクォーテーションを補いつつ結合
		### valium modify start
		$str .= "$front\"" . $url;
		### valium modify end
		$tmpstr = "\"$end" . $lnkstr . $backward;
		
	}
	$str .= $tmpstr;

	# title、target属性の削除（バイト数の無駄）
	$str =~ s/ target=["'][^"']*["']//ig;
	$str =~ s/ title=["'][^"']*["']//ig;
	
	return $str;
}
	
########################################
# Sub Lenb_EUC - 半角カナ、3バイト含むEUC文字列用length
# 第一引数：バイト数を数える文字列
# \x8E[\xA1-\xDF] = EUC半角カナ正規表現
# \x8F[\xA1-\xFE][\xA1-\xFE] = EUC3バイト文字正規表現
# 参考：Perlメモ→http://www.din.or.jp/~ohzaki/perl.htm
########################################

sub lenb_euc {
	my $llen;
	$llen = length($_[0]);										# 普通にlength
	$llen -= $_[0]=~s/(\x8E[\xA1-\xDF])/$1/g;					# 半角カナ数をマイナス
	$llen -= ($_[0]=~s/(\x8F[\xA1-\xFE][\xA1-\xFE])/$1/g)*2;	# 3バイト文字数*2をマイナス
	$llen;
}

########################################
# Sub Midb_EUC - 半角カナ、3バイト含むEUC文字列用substr
# 第一引数：切り出し元の文字列
# 第二引数：切り出し開始位置（0〜）
# 第三引数：切り出すバイト数
# \x8E[\xA1-\xDF] = EUC半角カナ正規表現
# \x8F[\xA1-\xFE][\xA1-\xFE] = EUC3バイト文字正規表現
# 参考：Perlメモ→http://www.din.or.jp/~ohzaki/perl.htm
########################################

sub midb_euc {
	my $llen1;
	my $llen2;
	my $lstr;
	my $lstart;
	
	# 先ず正しい開始位置を求めないと
	if ($_[1] == 0) {
		$lstart = 0;
	} else {
		$llen1 = $_[1];
		$lstr = substr($_[0], 0, $llen1);
		$llen2 = lenb_euc($lstr);
		my $llen3 = $llen1;
		while ($_[1] > $llen2) {
			$llen3 = $llen1;
			$llen3 += $lstr=~s/(\x8E[\xA1-\xDF])/$1/g;					# 半角カナ数をプラス
			$llen3 += ($lstr=~s/(\x8F[\xA1-\xFE][\xA1-\xFE])/$1/g)*2;	# 3バイト文字数*2をプラス
			$lstr = substr($_[0], 0, $llen3);
			$llen2 = lenb_euc($lstr);
		}
		$llen1 = $llen3;
		
		# 切り出した文字列の最後が半角カナをぶった切ってないか判定
		if (substr($_[0], 0 + $llen1 - 1, 2)=~s/(\x8E[\xA1-\xDF])/$1/g) {
			# ぶった切ってたらもう1バイト先を開始位置にする
			$llen1++;
		}
		$lstart = $llen1;
	}
	
	# 文字列の切り出し
	$llen1 = $_[2];
	$lstr = substr($_[0], $lstart, $llen1);
	$llen2 = lenb_euc($lstr);
	my $llen3;
	while ($_[2] > $llen2) {
		$llen3 = $llen1;
		$llen3 += $lstr=~s/(\x8E[\xA1-\xDF])/$1/g;					# 半角カナ数をプラス
		$llen3 += ($lstr=~s/(\x8F[\xA1-\xFE][\xA1-\xFE])/$1/g)*2;	# 3バイト文字数*2をプラス
		$lstr = substr($_[0], $lstart, $llen3);
		$llen2 = lenb_euc($lstr);
	}
	$llen1 = $llen3;
	
	# 切り出した文字列の最後が半角カナをぶった切ってないか判定
	if (substr($_[0], $lstart + $llen1 - 1, 2)=~s/(\x8E[\xA1-\xDF])/$1/g) {
		# ぶった切ってたらもう1バイト先まで切り出し
		$lstr = substr($_[0], $lstart, $llen1 + 1);
	}
	return $lstr;
}

########################################
# Sub Htmlout - HTMLの出力
########################################

sub htmlout {
	# HTMLヘッダ/フッタ定義
	$data = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD Compact HTML 1.0 Draft//EN\"><html><head><meta name=\"CHTML\" HTTP-EQUIV=\"content-type\" CONTENT=\"text/html; charset=Shift_JIS\"><meta http-equiv=\"Pragma\" content=\"no-cache\"><meta http-equiv=\"Cache-Control\" content=\"no-cache\"><meta http-equiv=\"Cache-Control\" content=\"max-age=0\"><title>$blog_name mobile ver.</title></head><body bgcolor=\"$cfg{BgColor}\" text=\"$cfg{TxtColor}\" link=\"$cfg{LnkColor}\" alink=\"$cfg{AlnkColor}\" vlink=\"$cfg{VlnkColor}\">" . $data;
	if (exists $cfg{AdmNM}) {
		$data .= "<p><center>管理人:";
		if (exists $cfg{AdmML}) {
			$cfg{AdmML} =~ s/\@/\&#64;/g;
			$cfg{AdmML} =~ s/\./\&#46;/g;
			$data .= "<a href=\"mailto:$cfg{AdmML}\">$cfg{AdmNM}</a>";
		} else {
			$data .= "$cfg{AdmNM}";
		}
		$data .= "</center></p>";
	}
	$data .= "<p><center>Powered by<br><a href=\"http://www.hazama.nu/pukiwiki/index.php?MT4i\">MT4i v$version</a></center></p></body></html>";
	
	# 表示文字列をShift_JISに変換
	&$jcnv(\$data,'sjis', "euc");
	
	# 表示
	binmode(STDOUT);
	print "Content-type: text/html; charset=Shift_JIS\n";
	print "Content-Length: ",length($data),"\n\n";
	print $data;
}

########################################
# Sub Errorout - エラーの出力
########################################

sub errorout {
	# HTMLヘッダ/フッタ定義
	$data = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD Compact HTML 1.0 Draft//EN\"><html><head><meta name=\"CHTML\" HTTP-EQUIV=\"content-type\" CONTENT=\"text/html; charset=Shift_JIS\"><title>Error</title></head><body>" . $data . "</body></html>";
	
	# 表示文字列をShift_JISに変換
	&$jcnv(\$data,'sjis', "euc");
	
	# 表示
	binmode(STDOUT);
	print "Content-type: text/html; charset=Shift_JIS\n";
	print "Content-Length: ",length($data),"\n\n";
	print $data;
}

##############################################################
# Sub conv_datetime - YYYYMMDDhhmmssを MM/DD hh:mm に変換
##############################################################

sub conv_datetime {
	if ($mode || (!$mode && $cfg{DT} eq "dt")) {
		$_[0] =~ s/\d\d\d\d(\d\d)(\d\d)(\d\d)(\d\d)\d\d/($1\/$2 $3:$4)/;
	} elsif (!$mode && $cfg{DT} eq "d") {
		$_[0] =~ s/\d\d\d\d(\d\d)(\d\d)\d\d\d\d\d\d/($1\/$2)/;
	} else {
		$_[0] = "";
	}
	return $_[0];
}

############################################################
# calc_cashe_size:携帯のキャッシュ(1画面に出力できる最大値)を求める
# 返値 携帯のキャッシュサイズ
# 参考：http://deneb.jp/Perl/mobile/
# Special Thanks：drry
############################################################
sub calc_cache_size {

	my ( $user_agent ) = @_;
	my $cache_size = 5120;
	if ( $user_agent =~ m|DoCoMo.*\W.*c(\d+).*(c\d+)|i ) {
		$cache_size = $1*1024;
	} elsif ( $user_agent =~ m|DoCoMo.*\W.*c(\d+).*(c\d+)?|i ) {
		$cache_size = $1*1024;
	} elsif ( $user_agent =~ m|DoCoMo|i ) {
		$cache_size = 5*1024;
	} elsif ( $user_agent =~ m|J-PHONE/[45]\.\d+| ) {
		$cache_size = 12*1024;
	} elsif ( $user_agent =~ m|J-PHONE| ) {
		$cache_size = 6*1024;
	} elsif ( $user_agent =~ m|KDDI\-| ) {
		$cache_size = 9*1024;
	} elsif ( $user_agent =~ m|UP\.Browser| ) {
		$cache_size = 7.5*1024;
	}
	return $cache_size;
}

########################################
# crypt()による暗号化、照合
# 参考：http://www.rfs.co.jp/sitebuilder/perl/05/01.html#crypt
########################################

# 暗号化したい文字列($val)を受け取り、暗号化した文字列を返す関数
sub enc_crypt {
    my ($val) = @_;

    my( $sec, $min, $hour, $day, $mon, $year, $weekday )
        = localtime( time );
    my( @token ) = ( '0'..'9', 'A'..'Z', 'a'..'z' );
    my $salt = $token[(time | $$) % scalar(@token)];
    $salt .= $token[($sec + $min*60 + $hour*60*60) % scalar(@token)];
    my $passwd2 =  crypt( $val, $salt );

    $passwd2 =~ s/\//\@2F/g;
    $passwd2 =~ s/\$/\@24/g;
    $passwd2 =~ s/\./\@2E/g;

    return $passwd2;
}

# パスワード($passwd1)と暗号化したパスワード($passwd2)を受け取り、
# 一致するかを判定する関数
sub check_crypt{
    my ($passwd1, $passwd2) = @_;

    $passwd2 =~ s/\@2F/\//g;
    $passwd2 =~ s/\@24/\$/g;
    $passwd2 =~ s/\@2E/\./g;
	
    # 暗号のチェック
    if ( crypt($passwd1, $passwd2) eq $passwd2 ) {
        return 1;
    } else {
        return 0;
    }
}

############################################################
# Sub Check_Category - エントリーのカテゴリを調べる
############################################################
sub check_category{
	my ($entry) = @_;
	my $cat_label;
	require MT::Placement;
	my (@places) = MT::Placement->load({ blog_id => $cfg{Blog_ID} , entry_id => $entry->id });
	if (@places) {
		require MT::Category;
		my @categories = MT::Category->load({blog_id => $cfg{Blog_ID}},
											{unique => 1});
		if (@categories) {
			for my $category (@categories) {
				if ($category->id == $places[0]->category_id){
					if ($cfg{CatDescReplace} eq "yes"){
						$cat_label = &conv_euc_z2h($category->description);
					}else{
						$cat_label = &conv_euc_z2h($category->label);
					}
				}
			}
		}
	}
	return $cat_label;
}

########################################
# Sub Conv_Euc2utf8 - EUC-JP→UTF8変換
########################################

sub conv_euc2utf8 {
	my ($str) = @_;
	if ($conv_in ne 'euc') {
		if ($conv_in eq 'utf8' && $ecd == 1) {
			$str = encode("shiftjis",decode("euc-jp",$str));
			$str = encode("utf8",decode("cp932",$str));
		} else {
			&$jcnv(\$str, $conv_in, 'euc');
		}
	}
	return $str;
}
