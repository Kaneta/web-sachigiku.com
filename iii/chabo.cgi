#!/usr/bin/perl
# ↑ご利用のプロバイダのPerl(JPerl不可)のあるパスを記述してください

# -------------------------------------------------------
# ---  Hybrid Short Message Board  'ChaBo'  Ver3.20β6---
# --- (c)1999-2000 KemoKemo(http://www.kemokemo.com/) ---
# -------------------------------------------------------


# ---初期設定

# ==================== 管理者が設定する項目です（必須） ====================
$SCRIPT     = 'http://sachigiku.com/iii/chabo.cgi';  # chabo.cgi自身を呼び出すURL
$BOARD_NAME = '噂佐菊都風ひと言掲示板';          # メッセージボード名称(PC用)
$BOARD_NAM2 = '噂佐菊都風ひと言掲示板';         # メッセージボード略称(携帯用 全角８文字以内推奨)

$HOMEPAGE   = 'http://sachigiku.com/';       # ホームページのアドレス
$HOMEPAG2   = 'http://sachigiku.com/iii/';         # ホームページのアドレス(iモード用)
#$HOMEPAG3   = 'http://kemokemo.com/ez/';        # ホームページのアドレス(EZweb用)
#$HOMEPAG4   = 'http://kemokemo.com/j/';         # ホームページのアドレス(J-SkyWeb用)
#$HOMEPAG5   = 'http://kemokemo.com/p/';         # ホームページのアドレス(-H"/PメールDX用)
#$HOMEPAG6   = 'http://kemokemo.com/di/';        # ホームページのアドレス(ドットi用)		(Ver3.20)
# ↑パソコン用/iモード用/EZweb用/-H"用のホームページを作っていない場合は
#   $HOMEPAGE   = '';
#   $HOMEPAG2   = '';
#   $HOMEPAG3   = '';
#   $HOMEPAG4   = '';
#   $HOMEPAG5   = '';
#   $HOMEPAG6   = '';
#   と設定してください。それぞれのリンク表示を省略できます。

$USE_CSS   = 1;                                              # CSS(スタイルシート)利用 (0:使わない 1:使う)	(Ver3.20)
$CSS_URL   = 'http://sachigiku.com/iii/chabo.css';    # CSSファイルのURL					(Ver3.20)


# ======= ChaBo Call 関係の初期設定です（必ず、正しく設定して下さい） ======
$CHABOCALL = 0;                                 # ChaBo Call機能(0:使わない 1:使う)
$SENDMAIL  = '/usr/lib/sendmail';               # サーバ内のsendmailのあるパス
$ML_TO     = '09099999999@docomo.ne.jp';        # ChaBo Call受信メールアドレス
$ML_FROM   = 'server@kemokemo.com';             # サーバからの送信メールアドレス
$CC_QUICK  = 1;                                 # ChaBo Callクイックアクセス(0:使わない 1:使う)


# ===== CGIを置くディレクトリ構成が特殊なサーバの場合は変更が必要です ======
$SCR_DIR  = '.';				# chabo.cgi, jcode.pl, include.txtを置くディレクトリ(基準ディレクトリ)
$DAT_DIR  = './chabo';				# chabo.txt等のデータを置くディレクトリ(パーミッション777)


# =============== カスタマイズする場合は適宜変更して下さい =================
$ACT_LINK  = 1;					# クリッカブルメール機能     (0:使わない 1:使う)
$ACT_URL   = 1;					# 簡易クリッカブルＵＲＬ機能 (0:使わない 1:使う)	(Ver3.20)
$ACT_INITIAL = 1;				# あたまとり機能 (0:使わない 1:使う)	(Ver3.20)
$ACT_WORD = 1;					# キーワード機能 (0:使わない 1:使う)	(Ver3.20)
$KEYWORD = '「あたまとり」';
$CUT_TEL   = 0;					# 電話番号カット機能        （0:使わない 1:使う)	(Ver3.20)
$CUT_URL   = 0;					# URLカット機能              (0:使わない 1:使う)	(Ver3.20)
$MAX_MESS  = 100;				# 保存するメッセージ最大数
$MESS_HOME = 'トップページに戻る';		# ホームページへ戻る旨のリンク表示(PC)
$MESS_HOM2 = '終了';				# ホームページへ戻る旨のリンク(携帯)
						# タイトルバナー表示機能は廃止しました			(Ver3.20)

# ---- CSSを利用した場合は以下の設定は無効です ----
$WALLPAPER = '';				# 壁紙のURL (http://〜) 
$BCOLOR    = '#FFFFFF';				# 背景色
$TCOLOR    = '#000000';				# 文字色
$LCOLOR    = '#0F314E';				# リンクの文字色
$VCOLOR    = '#71BBE5';				# 既に辿ったリンクの文字色
$ACOLOR    = '#B22222';				# クリック中のリンク文字色


# =============== 通常、ここから下は変更する必要はありません ===============
$TIMEZONE    = +9;				# タイムゾーン設定(日本:+9)
$INCF        = $SCR_DIR . '/include.txt';	# 組み込みファイル名
$MESF        = $DAT_DIR . '/chabo.txt';		# データファイル名
$LOCKF       = $DAT_DIR . '/chabo.lock'; 	# ロックファイル名
$WDTIMER     = 10;				# ロック監視タイマ（秒）
$COOKIE_NAME = 'kemokemo00';			# クッキー名
$COOKIE_PATH = '';				# クッキーの有効範囲(/:サーバ全体)
$ML_SUBJ     = 'ChaBo Call';			# ChaBo callメールの題名（半角英数字のみ可）
$ML_TIMER    = 10;				# ChaBo callインターバルタイマ（分）

@buffer = ();					# データバッファ初期化
$mesbuff = '';					# メッセージバッファ初期化
$exthead = '';					# 拡張ヘッダ初期化

# ==========================================================================


# ---漢字コード変換ライブラリを組み込む
	require $SCR_DIR . '/jcode.pl';


# ---ブラウザ種別をチェック
	$doti = 0;						# (Ver3.20)
	$user_agent = $ENV{'HTTP_USER_AGENT'};

	if   ($user_agent =~ /DoCoMo\//)      { $mode =  1; }	# iモード
	elsif($user_agent =~ /UP\.Browser\//) { $mode = -1; }	# EZweb
	elsif($user_agent =~ /PDXGW\/\d\.\d/) { $mode = -2; }	# PメールDX
	elsif($user_agent =~ /J-PHONE\//)     { $mode =  2; }	# J-SkyWeb	(Ver3.20変更)
	elsif($user_agent =~ /ASTEL\//)       {			# ドットi	(Ver3.20)
		$mode =  1; $HOMEPAG2 = $HOMEPAG6;
	}
								# PDAモード（ザウルス・コミパル・Dialo）
	elsif($user_agent =~ /sharp pda browser/ || $user_agent =~ /Dialo/) { $pda = 1; }
								# エクシーレ	(Ver3.20)
	elsif($user_agent eq 'Mozilla/3.0N AVE-Front/2.0 (Screen=320x240x4; Product=NEC/MW-E; )') {
		$mode = 1; $pda = 1;
	}
	else{ $mode = 0; }					# その他


#---フォームデコード
	&decode_form;
	$page     = $cgi_name{'p'};				# ページ(0:一覧 1〜:番号 -1:書き込み)
	$view     = $cgi_name{'v'};				# 表示件数(1/5)
	$name     = $cgi_name{'n'};				# 名前
	$message  = $cgi_name{'m'};				# メッセージ
	$undo = ($cgi_name{'u'} eq 'ok') ? 1 : 0;		# Undoフラグ
								# x:SUBMITダミー(J-PHONE用)
	# PDX用処理
	if($mode == -2) {
		&jcode'h2z_sjis(*BOARD_NAM2);			# 題名の半角カナ→全角変換

		$pdx_url = $SCRIPT;				# URL短縮「http://」→「//」
		$pdx_url =~ s/^http://;

		$view = 5;					# PDXは５件固定

		$pdxsubj = $cgi_name{'pdxsubj'};		# 題名
		$pdxdata = $cgi_name{'pdxdata'};		# 受信データ
		$pdxturn = $cgi_name{'pdxturn'};		# アクセス回数(Ver3.10)

		$pdxsubj =~ s/[\t\r\n]//g;			# タブ・改行除去
		$pdxdata =~ s/[\t\r\n]//g;
		$pdxsubj =~ s/(　| )+$//g;			# 文末の空白除去 (Ver3.20β5再修正)
		$pdxdata =~ s/(　| )+$//g;

		if   (($pdxdata eq '1' || $pdxdata eq '１')&& $page >=0) { $page = 1; }			# 読む(最新)
		elsif(($pdxdata eq '7' || $pdxdata eq '７')&& $page > 0) { $page = 999; }		# 読む(最初)

		elsif(($pdxdata eq '2' || $pdxdata eq '２')&& $page > 0) {				# ↑
			$page = ($page-$view < 1) ? 1 : $page-$view;
		}
		elsif(($pdxdata eq '8' || $pdxdata eq '８')&& $page > 0) { $page += $view; }		# ↓

		elsif(($pdxdata eq '3' || $pdxdata eq '３')&& $page >=0) { $page = -1; }		# 書く
		elsif(($pdxdata eq '9' || $pdxdata eq '９')&&($page>0 || $page<=-3)) { $page = 0; }	# メニュー
		elsif(($pdxdata eq '9' || $pdxdata eq '９')&& $page ==0) { $page = -9; }		# 終了

													# 名前スキップ
		elsif(($pdxdata eq '1' || $pdxdata eq '１')&& $page == -1 && $name ne '') { $page = -2; }

		elsif($pdxdata ne '' && $page == -1) { $page = -2; $name    = $pdxdata; }		# 名前→メッセージ
		elsif($pdxdata ne '' && $page == -2) { $page =  1; $message = $pdxdata; }		# メッセージ→投稿

		elsif(($pdxdata eq '19' || $pdxdata eq '１９')&& $page >=0) { $page = -19; }		# 回線切断
		elsif(($pdxdata eq '99' || $pdxdata eq '９９')&& $page ==0) { $page = -99; }		# サポート用

		elsif(($pdxdata ne '' && $pdxsubj ne '')&& $pdxturn == 1) {				# オフ書き
			$page = 1; $name = $pdxsubj; $message = $pdxdata;
		}

		else { $page = 0; }	# それ以外ならメニュー
	}

	if($page eq '')  { $page = 0; }
	if($view ne '5') { $view = 1; }


# ---セキュリティチェック／GETメソッドでの書き込みは無効
	if($ENV{'REQUEST_METHOD'} eq 'GET' && $message ne '') {
		if($mode != -2 && $mode != 2) {				# -H"/PDX/J-Skyは見逃してあげる
			$err .= 'エラー：GETメソッドでの書き込みは無効です。<BR>';
			$message = '';
		}
	}


# ---タブ・改行・文末の空白除去
	$name    =~ s/[\t\r\n]//g;
	$message =~ s/[\t\r\n]//g;
	$name    =~ s/(　| )+$//g;		# (Ver3.20β6)
	$message =~ s/(　| )+$//g;		# (Ver3.20β6)


# ---iモード/J-SKy端末の場合、絵文字除去
	if($mode == 1) {
		$name    = &cut_isymbol($name);
		$message = &cut_isymbol($message);
	}
	elsif($mode == 2) {
		$name    = &cut_jsymbol($name);
		$message = &cut_jsymbol($message);
	}

# -------------------------- 簡易フィルタ機能 (Ver3.20) --------------------------
#  (ひねって投稿されると検出できないので、その節は随時手作業で削除してください^^;)

# ---電話番号排除
	if($CUT_TEL) {
		if($name =~ /0[79]0/ ||
		   $name =~ /０７０/ ||
		   $name =~ /０９０/ ) { $name = ''; }

		if($message =~ /0[79]0/ ||
		   $message =~ /０９０/ ||
		   $message =~ /０９０/ ||
		   $message =~ /%d%d%d%d%d%d%d%d/ ||
		   $message =~ /〇九〇/ ||
		   $message =~ /０九０/ ||
		   $message =~ /零九零/ ||
		   $message =~ /ｾﾞﾛ(.*)ｷｭｳ(.*)ｾﾞﾛ/ )	{ $message = '【電話番号は記入できません】'; }
	}


# --- URL排除
	if($CUT_URL) {
		if($message =~ /http:/ ) { $message = '【ホームページアドレスは記入できません】'; }
	}


# --------------------------------------------------------------------------------


# ---漢字コード変換 (Ver2.10bからスルー)
#	&jcode'convert(*name, 'sjis');
#	&jcode'convert(*message, 'sjis');


# ---文字数チェック
	if(length($name)    > 32)  {
		$err .= 'エラー：お名前が長すぎます。全角16文字までです。<BR>';
		$name = '';
	}
	if(length($message) > 200) {
		$err .= 'エラー：メッセージが長すぎます。全角100文字までです。<BR>';
		$message = '';
	}


# ---名前のURLエンコード
	$u_name = &url_enc($name);


# ---クッキーからユーザ情報展開（フォーム優先）
	if($mode == 0 || $mode == -1) {
		&decode_cookie($COOKIE_NAME);
		$name = ($name eq '') ? $COOKIE{'Name'} : $name;
		$COOKIE{'Name'} = $name;
	}

	$userid = $COOKIE{'UserID'};
	if($userid eq '') {					# User IDがなければ発行
		$userid = time . $ENV{'REMOTE_ADDR'};
		$userid =~ s/\.//g;
	}
	$COOKIE{'UserID'} = $userid;

	$setcook="UserID\:$COOKIE{'UserID'},Name\:$COOKIE{'Name'},Email\:$COOKIE{'Email'},Url\:$COOKIE{'Url'}";


# ---クッキー賞味期限生成
	($secg,$ming,$hourg,$mdayg,$mong,$yearg,$wdayg) = gmtime(time+60*86400);		# 60日間有効
	$youbi = ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday') [$wdayg];
	$month = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec') [$mong];
	$yearg += ($yearg > 70) ? 1900 : 2000;			# クッキー2000年対策
	$date_gmt = sprintf("%s, %02d\-%s\-%04d %02d:%02d:%02d GMT",$youbi,$mdayg,$month,$yearg,$hourg,$ming,$secg);


	#（PC/EZ端末で、かつフォームデータが揃っていればクッキーを喰わせる） (Ver3.20でEZ追加)
	if(($mode == 0 || $mode == -1) && $name ne '' && $message ne '') {
		$exthead .= "Set-Cookie: $COOKIE_NAME=$setcook; expires=$date_gmt; path=$COOKIE_PATH\n";
	}

# ==================== ガイダンスとフォームを出力 ====================

# ---通常端末
	if( !$mode ) {
		$mesbuff .= "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0 Transitional//EN\">\n";		# (Ver3.20)
		$mesbuff .= "<HTML>\n<HEAD>\n";
		$mesbuff .= "<TITLE>$BOARD_NAME</TITLE>\n";
		$mesbuff .= "<META HTTP-EQUIV=\"Content-Type\" CONTENT=\"text/html; charset=Shift_JIS\">\n";

		if( $USE_CSS ) {			# スタイルシートを使用する場合	(Ver3.20)
			$mesbuff .= "<LINK REL=\"stylesheet\" TYPE=\"text/css\" HREF=\"$CSS_URL\">\n";
			$mesbuff .= "</HEAD>\n";
			$mesbuff .= "<BODY>\n";
		} else {				# スタイルシートを使用しない場合
			$WALLPAPER = ($WALLPAPER ne '') ? "BACKGROUND=\"$WALLPAPER\"" : '';
			$mesbuff .= "</HEAD>\n";
			$mesbuff .= "<BODY $WALLPAPER BGCOLOR=\"$BCOLOR\" TEXT=\"$TCOLOR\" LINK=\"$LCOLOR\" VLINK=\"$VCOLOR\" ALINK=\"$ACOLOR\">\n";
		}

	# ---組み込みファイルがあれば、表示
		if( open(INC,"<$INCF") ) {
			while(<INC>) { $mesbuff .= $_; }
			close(INC);
		} else {
							# タイトルバナー表示廃止 (Ver3.20)
			$mesbuff .= "<H1>$BOARD_NAME</H1>\n";

			$mesbuff .= "<P CLASS=\"note\">";
			$mesbuff .= '情報提供・挨拶・つぶやきなどお気軽に。芝居の実況もいいですね。<BR>';
			$mesbuff .= '個別の記事に関する内容は「コメント」へお願いします。<BR>';
			$mesbuff .= 'URLは自動で[URL]に変換されます。HTMLタグは使えません。</P>'."\n";
		}

	# ---書き込みフォームを表示
		$mesbuff .= "<DIV ALIGN=\"center\">\n";
		$mesbuff .= "<FORM METHOD=\"POST\" ACTION=\"$SCRIPT\">\n<TABLE>";
		$mesbuff .= '<TR><TD>お名前</TD>';
		if( $pda ) { $mesbuff .= '</TR><TR>'; }
		$mesbuff .= "<TD><INPUT TYPE=\"TEXT\" SIZE=\"16\" MAXLENGTH=\"16\" NAME=\"n\" VALUE=\"$name\"></TD></TR>\n";
		$mesbuff .= '<TR><TD>メッセージ</TD>';
		if( $pda ) { $mesbuff .= '</TR><TR>'; }
		$mesbuff .= "<TD><INPUT TYPE=\"TEXT\" SIZE=\"60\" MAXLENGTH=\"200\" NAME=\"m\" VALUE=\"\">";
		$mesbuff .= "<INPUT TYPE=\"SUBMIT\" VALUE=\"書き込む\"></TD></TR></TABLE>\n</FORM>\n";

		if($HOMEPAGE ne '') {
			$mesbuff .= "<A HREF=\"$HOMEPAGE\">$MESS_HOME</A>\n";
		}

		$mesbuff .= "</DIV><HR><P CLASS=\"mess\">\n";
	}

# ---ｉモード/J-SkyWeb端末
	elsif($mode > 0) {
		$mesbuff .= "<HTML><HEAD>";
		$mesbuff .= "<TITLE>$BOARD_NAM2</TITLE>";
		$mesbuff .= "</HEAD>\n<BODY>";

	# ---メニューページ出力
		if($page == 0) {

			$lastup= &lastup($MESF);
			if($lastup ne '') { $lastup .= '更新'; }

			if($mode == 2) { $mesbuff .= "$BOARD_NAM2<BR>$lastup"; }			# (Ver3.20β5)
			else { $mesbuff .= "<DIV ALIGN=\"center\">$BOARD_NAM2<BR>$lastup</DIV>"; }	# (Ver3.20β5)

			$mesbuff .= "<HR><DIV ALIGN=\"center\">◆MENU◆</DIV>";

			if($mode == 2) {	# J-Sky
				$mesbuff .= "<A HREF=\"$SCRIPT?p=1&v=1&n=$u_name\" DIRECTKEY=\"1\">1件ずつ読む</A><BR>";
				$mesbuff .= "<A HREF=\"$SCRIPT?p=1&v=5&n=$u_name\" DIRECTKEY=\"5\">5件ずつ読む</A><BR>";
				$mesbuff .= "<A HREF=\"$SCRIPT?p=-1&v=$view&n=$u_name\" DIRECTKEY=\"3\">ﾒｯｾｰｼﾞを書く</A><BR>";
			} else {		# iMODE
				$mesbuff .= "[1]<A HREF=\"$SCRIPT?p=1&v=1&n=$u_name\" ACCESSKEY=\"1\">1件ずつ読む</A><BR>";
				$mesbuff .= "[5]<A HREF=\"$SCRIPT?p=1&v=5&n=$u_name\" ACCESSKEY=\"5\">5件ずつ読む</A><BR>";
				$mesbuff .= "[3]<A HREF=\"$SCRIPT?p=-1&v=$view&n=$u_name\" ACCESSKEY=\"3\">ﾒｯｾｰｼﾞを書く</A><BR>";
			}

			if($HOMEPAG2 ne '' && $mode == 2) {		# J-Sky
				$mesbuff .= "<A HREF=\"$HOMEPAG4\" DIRECTKEY=\"9\">$MESS_HOM2</A><BR>";
			}
			if($HOMEPAG4 ne '' && $mode == 1) {		# iMODE/dot-i
				$mesbuff .= "[9]<A HREF=\"$HOMEPAG2\" ACCESSKEY=\"9\">$MESS_HOM2</A><BR>";
			}

			# ===↓Copyrightは改変禁止(Do Not Correct.)
			if($mode == 2) {	# J-Sky (Ver3.20)
				$mesbuff .= "<HR><DIV ALIGN=\"right\">by <A HREF=\"http://www.kemokemo.com/j/\">ChaBo</A></DIV>";
			} else {		# iMODE/dot-i
				$mesbuff .= "<HR><DIV ALIGN=\"right\">by <A HREF=\"http://www.kemokemo.com/i/\">ChaBo</A></DIV>";
			}
			# ===↑ここまで
		}

	# ---投稿フォーム出力
		if($page < 0) {
			$mesbuff .= 'ﾒｯｾｰｼﾞをどうぞ<BR>(最大'.$MAX_MESS.'件保存)<HR>';

			if($mode == 2) { $mesbuff .= "<FORM METHOD=\"GET\" ACTION=\"$SCRIPT\">"; }	# J-Sky
			else { $mesbuff .= "<FORM METHOD=\"POST\" ACTION=\"$SCRIPT\">"; }		# iMODE

			$mesbuff .= "<INPUT TYPE=\"HIDDEN\" NAME=\"p\" VALUE=\"1\">";
			$mesbuff .= "<INPUT TYPE=\"HIDDEN\" NAME=\"v\" VALUE=\"$view\">";
			$mesbuff .= "お名前<BR><INPUT TYPE=\"TEXT\" SIZE=\"12\" MAXLENGTH=\"16\" NAME=\"n\" VALUE=\"$name\"><BR>";

			# ---J-SkyはTEXTフォームから36〜64バイトまでしか入力できないのでTEXTAREAにする (Ver3.20)
			if($mode == 2) {	# J-Sky
				$mesbuff .= "ﾒｯｾｰｼﾞ<BR>(全角100字まで)<BR><TEXTAREA COLS=\"16\" ROWS=\"1\" NAME=\"m\"></TEXTAREA><BR>";
			} else {		# iMODE
				$mesbuff .= "ﾒｯｾｰｼﾞ<BR><INPUT TYPE=\"TEXT\" SIZE=\"16\" MAXLENGTH=\"200\" NAME=\"m\" VALUE=\"\"><BR>";
			}

			# NAMEをつけてないSUBMITのVALUEまでGETで送ってしまう、J-SH02の仕様対策
			if($mode == 2) { $mesbuff .= "<INPUT TYPE=\"SUBMIT\" NAME=\"x\" VALUE=\"書き込む\"></FORM>"; }
			else { $mesbuff .= "<INPUT TYPE=\"SUBMIT\" VALUE=\"書き込む\"></FORM>"; }

			$mesbuff .= '絵文字は使わないで下さい｡ 改行は無視します<BR>';
			if($mode == 2) {  $mesbuff .= "<HR><A HREF=\"$SCRIPT?p=0&n=$u_name\" DIRECTKEY=\"9\">ﾒﾆｭｰに戻る</A><BR>"; }
			else { $mesbuff .= "<HR><A HREF=\"$SCRIPT?p=0&n=$u_name\" DIRECTKEY=\"9\">ﾒﾆｭｰに戻る</A><BR>"; }
		}
	}


# ---EZweb端末
	elsif($mode == -1) {
		$mesbuff .= "<HDML VERSION=\"3.0\" MARKABLE=\"TRUE\" PUBLIC=\"TRUE\" TTL=\"0\">\n";

	# ---メニューデッキ出力
		if($page == 0) {
			$mesbuff .= "<DISPLAY NAME=\"MENU\" TITLE=\"$BOARD_NAM2\">\n";
			$mesbuff .= "<ACTION TYPE=\"ACCEPT\" LABEL=\"読む\" TASK=\"GO\" DEST=\"?p=1&v=$view\">\n";
			$mesbuff .= "<ACTION TYPE=\"SOFT1\" LABEL=\"戻る\" TASK=\"PREV\">\n";
			$mesbuff .= "<CENTER>$BOARD_NAM2<BR>\n";

			$lastup = &lastup($MESF);
			if($lastup ne '') { $mesbuff .= "<CENTER>$lastup" . '更新<BR>'; }

			$mesbuff .= "<CENTER>◆MENU◆<BR>\n";

			$mesbuff .= "<A ACCESSKEY=\"1\" LABEL=\"読む\" TASK=\"GO\" DEST=\"?p=1&v=1\">1件ずつ読む</A><BR>\n";
			$mesbuff .= "<A ACCESSKEY=\"5\" LABEL=\"読む\" TASK=\"GO\" DEST=\"?p=1&v=5\">5件ずつ読む</A><BR>\n";
			$mesbuff .= "<A ACCESSKEY=\"3\" LABEL=\"書く\" TASK=\"GO\" DEST=\"?p=-1&v=$view\">ﾒｯｾｰｼﾞを書く</A><BR>\n";

			if($HOMEPAG3 ne '') {
				$mesbuff .= "<A ACCESSKEY=\"9\" LABEL=\"終了\" TASK=\"GO\" DEST=\"$HOMEPAG3\">$MESS_HOM2</A><BR>\n";
			}

			$mesbuff .= "<CENTER>----------------<BR>\n";

			# ===↓Copyrightは改変禁止(Do Not Correct.)
			$mesbuff .= "<RIGHT><A LABEL=\"情報\" TASK=\"GO\" DEST=\"http://www.kemokemo.com/ez/\" SENDREFERER=\"TRUE\">by ChaBo</A><BR>\n";
			# ===↑ここまで

			$mesbuff .= "</DISPLAY>\n";
		}

	# ---投稿デッキ出力
		if($page < 0) {
			$mesbuff .= "<NODISPLAY NAME=\"INIT\">\n";
			$mesbuff .= "<ACTION TYPE=\"ACCEPT\" TASK=\"GO\" DEST=\"#NAMIN\" REL=\"NEXT\" VARS=\"mess=\">\n";
			$mesbuff .= "</NODISPLAY>\n";

			$mesbuff .= "<ENTRY NAME=\"NAMIN\" KEY=\"name\" EMPTYOK=\"TRUE\">\n";
			$mesbuff .= "<ACTION TYPE=\"ACCEPT\" LABEL=\"次へ\" TASK=\"GO\" DEST=\"#MESIN\">\n";
			$mesbuff .= "お名前：<BR>(全角16字まで)\n</ENTRY>\n";

			$mesbuff .= "<ENTRY NAME=\"MESIN\" KEY=\"mess\" EMPTYOK=\"FALSE\">\n";
			$mesbuff .= "<ACTION TYPE=\"ACCEPT\" LABEL=\"次へ\" TASK=\"GO\" DEST=\"#CONF\">\n";
			$mesbuff .= "メッセージ：<BR>(全角100字まで)\n</ENTRY>\n";

			$mesbuff .= "<DISPLAY NAME=\"CONF\">\n";
			$mesbuff .= "<ACTION TYPE=\"ACCEPT\" LABEL=\"書く\" TASK=\"GO\" DEST=\"?\" POSTMETHOD=\"POST\" POSTDATA=\"p=1\&v=$view\&n=\$name\&m=\$mess\">\n";
			$mesbuff .= "<ACTION TYPE=\"SOFT1\" LABEL=\"修正\" TASK=\"GO\" DEST=\"#NAMIN\">\n";
			$mesbuff .= "書込みOK?<BR>\n<CENTER>----------------<BR>\n";
			$mesbuff .= "[\$name]<BR>\$mess<BR>\n";

			$mesbuff .= "<CENTER>----------------<BR>\n";
			$mesbuff .= "<A LABEL=\"書く\" TASK=\"GO\" DEST=\"?\" POSTMETHOD=\"POST\" POSTDATA=\"p=1\&v=$view\&n=\$name\&m=\$mess\">書き込む</A><BR>\n";
			$mesbuff .= "<A LABEL=\"修正\" TASK=\"GO\" DEST=\"#NAMIN\">修正する</A><BR>\n";
			$mesbuff .= "<A LABEL=\"ﾒﾆｭｰ\" TASK=\"GO\" DEST=\"?p=0&v=$view\">ﾒﾆｭｰに戻る</A><BR>\n";
			$mesbuff .= "</DISPLAY>\n";
		}
	}


# ---H"/PDX端末
	elsif($mode == -2) {
		$mesbuff .= "Content-Type: text/plain\n";	# Pメールヘッダの一部
		$mesbuff .= "Subject: $BOARD_NAM2\n";

	# ---メニューページ出力
		if($page == 0) {
			$mesbuff .= "From: $pdx_url?p=0&n=$u_name\n\n";

			$lastup= &lastup($MESF);
			if($lastup ne '') { $mesbuff .= $lastup . ' 更新' . "\n"; }

			$mesbuff .= "−−−−−−\n";
			$mesbuff .= "◆ＭＥＮＵ◆\n";
			$mesbuff .= "�@伝言を読む\n";
			$mesbuff .= "�B伝言を書く\n";

			if($HOMEPAG5 ne '') { $mesbuff .= "�H$MESS_HOM2\n"; }

			$mesbuff .= "�R回線切断\n";

			# ===↓Copyrightは改変禁止(Do Not Correct.)
			$mesbuff .= "−−−−−−\nChaBo\n";
			# ===↑ここまで
		}

	# ---投稿ページ出力
		if($page == -1) {						# 名前
			$mesbuff .= "From: $pdx_url?p=-1&n=$u_name\n\n";
			$mesbuff .= "お名前を１６字以内で入力して下さい：\n";

			if($name ne '') {					# 名前スキップ
				$mesbuff .= "�@→「$name」\n";
			}
			$mesbuff .= "−−−−−−\n";
		}

		if($page == -2) {						# メッセージ
			$mesbuff .= "From: $pdx_url?p=-2&n=$u_name\n\n";
			$mesbuff .= "メッセージを１００字以内で入力して下さい：\n";
			$mesbuff .= "−−−−−−\n";
		}

	# ---終了ページ出力
	#  （機能水準の低いPDX端末に対応するため、ワンクッションおきます）
		if($page == -9) {
			$mesbuff .= "From: $HOMEPAG5\n\n";			# ホームページへ
			$mesbuff .= "◇終了◇\n";
			$mesbuff .= "ご利用ありがとうございました。\n";
			$mesbuff .= "�@進む\n";
			$mesbuff .= "−−−−−−\n";
		}

	# ---切断ページ出力
		if($page == -19) {
			$mesbuff .= "X-PmailDX-CTRL: LineDisconnect\n";		# 切断指令
			$mesbuff .= "From: $pdx_url?p=-9&n=$u_name\n\n";
			$mesbuff .= "◇回線切断◇\n";
			$mesbuff .= "ご利用ありがとうございました。\n";
			$mesbuff .= "−−−−−−\n";
			$mesbuff .= "★Ｔｉｐｓ★\n";
			$mesbuff .= "接続前に\n";
			$mesbuff .= "「題名」←お名前\n";
			$mesbuff .= "「本文」←メッセージ\n";
			$mesbuff .= "をあらかじめ書いてから接続すると伝言板に直接書き込みできます\n";
			$mesbuff .= "−−−−−−\n";
		}

	# ---サポート用
		if($page == -99) {
			$mesbuff .= "From: //kemokemo.com/p/\n\n";
			$mesbuff .= "サポートサイトに進みます。\n";
			$mesbuff .= "�@進む\n";
			$mesbuff .= "−−−−−−\n";
		}
	}


# ====================================================================

# ---データ読込み
	&file_iowait;						# ロック解除まで待機 (Ver3.12)

	if(open (MESF,"<$MESF")) {				# オープン
		$count = 0;
		while(<MESF>) {  				# データ読込み
			push(@buffer,$_);
			if(++$count >= $MAX_MESS) { last; }	# 最大メッセージ数まで読み込む
		}
		close(MESF);
	}
	else {							# 読み込めなければファイルを作る
		$err .= 'データファイル '.$MESF.' が読込めません。<BR>';
		if(open (MESF,">$MESF")) {
			close(MESF);
			$err .= 'データファイルを新規作成しました。<BR>';
		}
		else { $err .= 'エラー：データファイルの新規作成に失敗しました。<BR>'; }
	}


# ---フォームからのデータ有り？
	if(($name ne '' && $message ne '') || $undo) {

	# ---データ格納
		&file_iowait;					# ロック解除まで待機
		&file_lock;					# ファイルロック

		if(-f $MESF) {
			@fileinfo = stat($MESF);		# データファイル最終更新時刻を保存
			$lastup = $fileinfo[9];
		}

		if(open (MESF,">$MESF")) {

		# ---データ準備
								# アンドゥ
			if( $undo ) {
								# ユーザIDが一致、かつ６時間以内ならばデータバッファから削除
				($gtime, $uid, $host, $timestamp, $name, $message) = split(/,/,@buffer[0],6);
				if(crypt($userid,'KK') eq $uid && time-$gtime < 21600) { shift(@buffer); }
			}
			else {
				$name =~ s/,/，/g;		# 名前の特殊文字は全角変換
				$name =~ s/&/＆/g;
				$name =~ s/%/％/g;
				$name =~ s/</＜/g;
				$name =~ s/>/＞/g;
				$name =~ s/"/”/g;

				$message =~ s/&/&amp;/g;	# メッセージの特殊文字はHTMLエンコード
				$message =~ s/</&lt;/g;
				$message =~ s/>/&gt;/g;
				$message =~ s/"/&quot;/g;

				$gtime = time;			# 時刻
				$uid  = crypt($userid,'KK');	# ユーザIDを暗号化

								# リモートホスト名か、IPアドレス
				$host = $ENV{'REMOTE_HOST'};
				if($host eq '') { $host = $ENV{'REMOTE_ADDR'}; }

								# タイムスタンプ生成
				($sec,$min,$hour,$mday,$mon) = gmtime($gtime+$TIMEZONE*3600);
				$timestamp = sprintf("%02d/%02d %02d:%02d",++$mon,$mday,$hour,$min);

								# データフィールド組み立て
				$data = "$gtime,$uid,$host,$timestamp,$name,$message\n";

								# 直前のメッセージ内容を所得
				($d_gtime, $d_uid, $d_host, $d_timestamp, $d_name, $d_message) = split(/,/,@buffer[0],6);
				$d_message =~ s/[\r\n]+$//;

								# 多重書きこみチェック
				if(($name ne $d_name) || ($message ne $d_message)) {

								# 多重でなければデータバッファに追加
					unshift(@buffer,$data);

								# メッセージ最大保存件数を超えたら消去
					$count = @buffer;
					if($count > $MAX_MESS) { pop(@buffer); }
				}
			}
								# データバッファ書き戻し
			foreach(@buffer) { print MESF $_; }
			close(MESF);


		# ---更新通知メール送信
			if($CHABOCALL && -f $MESF) {
				@fileinfo = stat($MESF);
				$lastup2 = $fileinfo[9];
								# インターバル時間を過ぎていれば、更新メール送信
				if($lastup2-$lastup > $ML_TIMER*60) { $err .= &call_mail; }
			}

		# ---リロード準備 (-H"/PDXはスルー)
			if($mode != -2) { $exthead .= "Location: $SCRIPT?p=1&v=$view&n=$u_name\n"; }

		}
		else { $err .= 'エラー：データファイルの更新ができません。<BR>'; }

		&file_unlock;					# ファイルロック解除
	}


# ============================== データ表示 ==============================

	$kosuu = @buffer;					# 発言数

	if($err eq '') {

	# ---通常端末
		if(!$mode) {
			foreach(@buffer) {
				($gtime, $uid, $host, $timestamp, $name, $message) = split(/,/,$_,6);
				$name    =~ s/ /&nbsp;/g;
				$message =~ s/ /&nbsp;/g;

				if($ACT_LINK) { $message = &active_link($message); }
				if($ACT_URL ) { $message = &active_url($message);  }
				if($ACT_WORD ) { $message = &active_word($message); }
				if($ACT_INITIAL ) { $message = &active_initial($message); }
									# 時刻を表示
				if (time - $gtime < 86400) { $mesbuff .= "<SMALL CLASS=\"new\">"; }
				 else { $mesbuff .= "<SMALL CLASS=\"std\">"; }
				$mesbuff .= "$timestamp</SMALL> ";

				$mesbuff .= "<B CLASS=\"name\">$name</B> : ";		# 名前を表示

				if( $pda ) { $mesbuff .= '<BR>'; }	# PDAの場合は改行
				$mesbuff .= "$message<BR>\n";
			}
		}

	# ---iモード端末
		elsif($mode > 0)  {
			if($page > 0) {
	
				if($page > $kosuu) {		# 最初の番号決定
					$page = $kosuu - $view + 1;
					$page = ($page < 1) ? 1 : $page;
				}

				$loop = $page;			# アーティクル表示
				while($loop < $page+$view) {
					if($loop <= $kosuu) {
						($gtime, $uid, $host, $timestamp, $a_name, $message) = split(/,/,@buffer[$loop-1],6);

						$a_name  =~ s/ /&nbsp;/g;
						$message =~ s/ /&nbsp;/g;

						if($ACT_LINK) { $message = &active_link($message); }
						if($ACT_URL)  { $message = &active_url($message);  }
						if($ACT_WORD)  { $message = &active_word($message);  }
						if($ACT_INITIAL ) { $message = &active_initial($message); }

						$mesbuff .= "▼$loop/$kosuu";
						if($loop == 1) { $mesbuff .= "(最新)"; }
						if($pda == 1) {						# エクシーレ (Ver3.20)
							$mesbuff .= " $timestamp 【$a_name】<BR>$message<HR>";
						}
						else {							# iモード/J-Sky
							$mesbuff .= "<BR>$timestamp<BR>$a_name<HR WIDTH=\"90%\">$message<HR>";
						}
					}
					++$loop;
				}

				$f_page = $page - $view;	# 次のページ
				$b_page = $page + $view;	# 前のページ

				if($page == 1) {
					if($mode == 2) { $mesbuff .= "<A HREF=\"$SCRIPT?p=1&v=$view&n=$u_name\" DIRECTKEY=\"1\">更新</A>"; }		# (Ver3.10)
					else { $mesbuff .= "[1]<A HREF=\"$SCRIPT?p=1&v=$view&n=$u_name\" ACCESSKEY=\"1\">更新</A>"; }
				}
				if($page > 1) {
					if($mode == 2) { $mesbuff .= "<A HREF=\"$SCRIPT?p=1&v=$view&n=$u_name\" DIRECTKEY=\"1\">最新</A>"; }		# (Ver3.10)
					else { $mesbuff .= "[1]<A HREF=\"$SCRIPT?p=1&v=$view&n=$u_name\" ACCESSKEY=\"1\">最新</A>"; }
				}
				if($page-$view > 1) {
					if($mode == 2) { $mesbuff .= "<A HREF=\"$SCRIPT?p=$f_page&v=$view&n=$u_name\" DIRECTKEY=\"2\">次↑</A>"; }	# (Ver3.10)
					else { $mesbuff .= "[2]<A HREF=\"$SCRIPT?p=$f_page&v=$view&n=$u_name\" ACCESSKEY=\"2\">次↑</A>"; }
				}
				$mesbuff .= '<BR>';
	
				if($page < $kosuu) {
					if($mode == 2) { $mesbuff .= "<A HREF=\"$SCRIPT?p=999&v=$view&n=$u_name\" DIRECTKEY=\"7\">最初</A>"; }		# (Ver3.10)
					else { $mesbuff .= "[7]<A HREF=\"$SCRIPT?p=999&v=$view&n=$u_name\" ACCESSKEY=\"7\">最初</A>"; }
				}
				if($page+$view < $kosuu) {
					if($mode == 2) { $mesbuff .= "<A HREF=\"$SCRIPT?p=$b_page&v=$view&n=$u_name\" DIRECTKEY=\"8\">前↓</A>"; }	# (Ver3.10)
					else { $mesbuff .= "[8]<A HREF=\"$SCRIPT?p=$b_page&v=$view&n=$u_name\" ACCESSKEY=\"8\">前↓</A>"; }
				}
				$mesbuff .= '<BR>';
	
				if($page != 0) {
					if($view != 5) {
						if($mode == 2) { $mesbuff .= "<A HREF=\"$SCRIPT?p=$page&v=5&n=$u_name\" DIRECTKEY=\"5\">5件ずつ読む</A><BR>"; }	# (Ver3.10)
						else { $mesbuff .= "[5]<A HREF=\"$SCRIPT?p=$page&v=5&n=$u_name\" ACCESSKEY=\"5\">5件ずつ読む</A><BR>"; }
					} else {
						if($mode == 2) { $mesbuff .= "<A HREF=\"$SCRIPT?p=$page&v=1&n=$u_name\" DIRECTKEY=\"5\">1件ずつ読む</A><BR>"; } # (Ver3.10)
						else { $mesbuff .= "[5]<A HREF=\"$SCRIPT?p=$page&v=1&n=$u_name\" ACCESSKEY=\"5\">1件ずつ読む</A><BR>"; }
					}
	
					if($mode == 2) {										# (Ver3.10)
						$mesbuff .= "<A HREF=\"$SCRIPT?p=-1&v=$view&n=$u_name\" DIRECTKEY=\"3\">書く</A>";
						$mesbuff .= "<A HREF=\"$SCRIPT?p=0&v=$view&n=$u_name\" DIRECTKEY=\"9\">ﾒﾆｭｰ</A>";
					} else {
						$mesbuff .= "[3]<A HREF=\"$SCRIPT?p=-1&v=$view&n=$u_name\" ACCESSKEY=\"3\">書く</A>";
						$mesbuff .= "[9]<A HREF=\"$SCRIPT?p=0&v=$view&n=$u_name\" ACCESSKEY=\"9\">ﾒﾆｭｰ</A>";
					}
				}

				$mesbuff .= "<BR>\n";
			}
		}

	#--- EZweb端末
		elsif($mode == -1) {
			if($page > 0) {

				$mesbuff .= "<DISPLAY NAME=\"VIEW\">\n";
				$mesbuff .= "<ACTION TYPE=\"ACCEPT\" TASK=\"GO\" LABEL=\"書く\" DEST=\"?p=-1&v=$view\">\n";
				$mesbuff .= "<ACTION TYPE=\"SOFT1\" TASK=\"GO\" LABEL=\"ﾒﾆｭｰ\" DEST=\"?p=0&v=$view\">\n";

				if($page > $kosuu) {		# 最初の番号決定
					$page = $kosuu - $view + 1;
					$page = ($page < 1) ? 1 : $page;
				}

				$loop = $page;			# アーティクル表示
				while($loop < $page+$view) {
					if($loop <= $kosuu) {
						($gtime, $uid, $host, $timestamp, $a_name, $message) = split(/,/,@buffer[$loop-1],6);
						$a_name  =~ s/ /&nbsp;/g;	# (Ver3.10)
						$message =~ s/ /&nbsp;/g;
						$a_name  =~ s/\$/&dol;/g;	# (Ver3.10)
						$message =~ s/\$/&dol;/g;	# (Ver3.10)

						if($ACT_LINK) { $message = &active_link_ez($message); }
						if($ACT_URL)  { $message = &active_url_ez($message);  }
						if($ACT_WORD)  { $message = &active_word_ez($message);  }
						if($ACT_INITIAL ) { $message = &active_initial_ez($message); }

						$mesbuff .= "▼$loop/$kosuu";
						if($loop == 1) { $mesbuff .= "(最新)"; }
						$mesbuff .= "<BR>$timestamp<BR>[$a_name]<BR>$message<BR>\n";
						$mesbuff .= "<CENTER>------------<BR>\n";
					}
					++$loop;
				}

				$f_page = $page - $view;	# 次のページ
				$b_page = $page + $view;	# 前のページ

				if($page == 1) {							# (Ver3.20β5)
						$rnd = sprintf("%04d" , int( rand(10000) ));
						$mesbuff .= "<A LABEL=\"選択\" TASK=\"GO\" DEST=\"?p=1&v=$view&x=$rnd\" ACCESSKEY=\"1\">更新</A><BR>\n";
				}
				if($page > 1) {
						$mesbuff .= "<A LABEL=\"選択\" TASK=\"GO\" DEST=\"?p=1&v=$view\" ACCESSKEY=\"1\">最新</A><BR>\n";
				}
				if($page-$view > 1) {
					$mesbuff .= "<A LABEL=\"選択\" TASK=\"GO\" DEST=\"?p=$f_page&v=$view\" ACCESSKEY=\"2\">次↑</A><BR>\n";
				}

				if($page != 0) {
					if($view != 5) {
						$mesbuff .= "<A LABEL=\"選択\" TASK=\"GO\" DEST=\"?p=$page&v=5\" ACCESSKEY=\"5\">5件ずつ読む</A><BR>\n";
					} else {
						$mesbuff .= "<A LABEL=\"選択\" TASK=\"GO\" DEST=\"?p=$page&v=1\" ACCESSKEY=\"5\">1件ずつ読む</A><BR>\n";
					}
				}

				if($page < $kosuu) {
					$mesbuff .= "<A LABEL=\"選択\" TASK=\"GO\" DEST=\"?p=999&v=$view\" ACCESSKEY=\"7\">最初</A><BR>\n";
				}
				if($page+$view < $kosuu) {
					$mesbuff .= "<A LABEL=\"選択\" TASK=\"GO\" DEST=\"?p=$b_page&v=$view\" ACCESSKEY=\"8\">前↓</A><BR>\n";

				}

				if($page != 0) {
					$mesbuff .= "<A LABEL=\"選択\" TASK=\"GO\" DEST=\"?p=-1&v=$view\" ACCESSKEY=\"3\">書く</A><BR>\n";
					$mesbuff .= "<A LABEL=\"選択\" TASK=\"GO\" DEST=\"?p=0&v=$view\" ACCESSKEY=\"9\">ﾒﾆｭｰ</A><BR>\n";
				}

				$mesbuff .= "</DISPLAY>\n";
			}
		}

	#--- -H"/PDX端末
		elsif($mode == -2) {
			if($page > 0) {

				if($page > $kosuu) {		# 最初の番号決定
					$page = $kosuu - $view + 1;
					$page = ($page < 1) ? 1 : $page;
				}

				$mesbuff .= "Content-Type: text/plain\n";	# Pメールヘッダ表示
				$mesbuff .= "From: $pdx_url?p=$page&n=$u_name\n";
				$mesbuff .= "Subject: $BOARD_NAM2\n";
				$mesbuff .= "\n";

				$loop = $page;			# アーティクル表示
				while($loop < $page+$view) {
					if($loop <= $kosuu) {
						($gtime, $uid, $host, $timestamp, $a_name, $message) = split(/,/,@buffer[$loop-1],6);

						$message =~ s/&amp;/&/g;	# HTML→テキストデコード
						$message =~ s/&lt;/</g;
						$message =~ s/&gt;/>/g;
						$message =~ s/&quot;/"/g;
										# &nbsp;のデコードは不要

						&jcode'h2z_sjis(*a_name);	# 半角カナ→全角変換(-H"/PDXは半角カナ禁止)
						&jcode'h2z_sjis(*message);

						$mesbuff .= "▼$loop";
#						$mesbuff .= "/$kosuu";
						if($loop == 1) { $mesbuff .= "(最新)"; }
						$mesbuff .= "\n$timestamp\n[$a_name]\n$message";
						$mesbuff .= "−−−−−−\n";
					}
					++$loop;
				}

				$f_page = $page - $view;	# 次のページ
				$b_page = $page + $view;	# 前のページ

				if($page > 1)       { $mesbuff .= "�@最新\n"; }
				if($page-$view > 1) { $mesbuff .= "�A次↑\n"; }

				if($page < $kosuu)       { $mesbuff .= "�F最初\n"; }
				if($page+$view < $kosuu) { $mesbuff .= "�G前↓\n"; }

				if($page != 0) {
					$mesbuff .= "�B書く\n";
					$mesbuff .= "�Hメニュー\n";
					$mesbuff .= "�R回線切断\n";
				}
			}
		}
	}


# ---エラーメッセージ表示
	else {
		if($mode == -1) {				# EZweb
			$mesbuff .= "<DISPLAY NAME=\"ERR\">\n";
			$mesbuff .= "<ACTION TYPE=\"ACCEPT\" TASK=\"GO\" LABEL=\"ﾒﾆｭｰ\" DEST=\"?p=0&v=$view\">\n";
			$mesbuff .= $err;
			$mesbuff .= "</DISPLAY>\n";
		}
		elsif($mode == -2) {				# -H"/PDX
			$err =~ s/<BR>/\n/g;			# タグ潰し
			$mesbuff .= "From: $pdx_url?p=0\n\n";
			$mesbuff .= "$err（発信→メニューへ戻る）\n";
		}
		else {						# その他
			$mesbuff .= $err;
		}
	}


# ---Undoボタン表示（通常端末）
	if(!$mode) {
		$mesbuff .= "</P><HR><DIV ALIGN=\"center\">";
		$mesbuff .= '※「元に戻す」ボタンが表示されていれば、直前に自分が書き込んだメッセージを消すことができます。<BR>';

		($gtime, $uid, $host, $timestamp, $name, $message) = split(/,/,@buffer[0],6);

								# Undoは他人が書き込むか、6時間有効
		if(crypt($userid,'KK') eq $uid && time-$gtime < 21600) {
			$mesbuff .= "<FORM METHOD=\"POST\" ACTION=\"$SCRIPT\">";
			$mesbuff .= "<INPUT TYPE=\"HIDDEN\" NAME=\"u\" VALUE=\"ok\">";
			$mesbuff .= "<INPUT TYPE=\"SUBMIT\" VALUE=\"元に戻す\"></FORM>";
		} else {
			$mesbuff .= '<BR>';
		}

		# ---ホームページへ戻るリンク表示
		if($HOMEPAGE ne '') {
			$mesbuff .= "<A HREF=\"$HOMEPAGE\">$MESS_HOME</A></DIV>";
		}

		# ===↓Copyrightは改変禁止(Do Not Correct.)
		$mesbuff .= "<DIV ALIGN=\"right\"><FONT SIZE=\"2\">powerd by <A HREF=\"http://www.kemokemo.com/\">ChaBo</A>.</FONT></DIV>\n";
		$mesbuff .= "<!-- ChaBo Ver3.20β6(c)1999-2000 KemoKemo(Yoichi Sato) -->\n";
		# ===↑ここまで
	}


# ---ページを閉じる
	if($mode == -1) { $mesbuff .= "</HDML>"; }		# EZweb
	elsif($mode >= 0 ) { $mesbuff .= "</BODY></HTML>"; }	# その他(-H"/PDX以外)


# ---メッセージバッファを掃き出す
	&buf_flash($mode, $exthead, $mesbuff);
	exit;


# ============================== end of main ==============================


# ---フォームデコードサブルーチン
sub decode_form {
	local($_,@_);

	if ($ENV{'REQUEST_METHOD'} eq "GET") {

	# ---「&」を生で送って来るJ-Sky端末対策
		if($ENV{'HTTP_X_JPHONE_MSNAME'} ne '') {
			$_ = $ENV{'QUERY_STRING'};
			s/&([mnpvux]=)/%amp$1/g;
			s/&/%26/g;
			s/%amp/&/g;
		} else { $_ = $ENV{'QUERY_STRING'}; }		# その他の素直な端末
	}
	elsif ($ENV{'REQUEST_METHOD'} eq "POST") { read(STDIN,$_,$ENV{'CONTENT_LENGTH'}); }
	split(/&/);

	foreach(@_) {
		if (index($_,"=") == $[ - 1) { push(name,'',$_); }
		else { push(name, split(/=/,$_, 2)); }
	}

	foreach(@name) {
		s/\+/ /g;
		s/%(..)/pack("c",hex($1))/ge;
	}

	%cgi_name = @name;
}


# ---Cookieのデコード
sub decode_cookie {
	local($cookie) = @_;
	local($name,$value,$cookies);

	foreach (split(/\;/,$ENV{'HTTP_COOKIE'})) {
		($name, $value) = split(/=/);
		$name =~ s/ //g;
		$COOKIES{$name} = $value;
	}

	foreach (split(/\,/,$COOKIES{$cookie})) {
		($name, $value) = split(/:/);
		$COOKIE{$name} = $value;
	}

	return;
}


# ---ファイルロック
sub file_lock {
	open(LOCKFILE,">$LOCKF");
	close(LOCKFILE);
	return 0;
}


# ---ファイルロック解除されるまで待機
sub file_iowait {
	local($count) = 0;
	while(-e $LOCKF && ++$count < $WDTIMER) { sleep(1); }
	if($count >= $WDTIMER) { &file_unlock; }		# タイムオーバーしたら強制解除
	return 0;
}


# ---ファイルロック解除
sub file_unlock {
	unlink($LOCKF);
	return 0;
}


# ---最終更新日付を調べる（引数：ファイル名）
sub lastup {
	local($filename) = @_[0];
	local(@fileinfo,$sec,$min,$hour,$mday,$mon,$retv);

	if(-f $filename) {
		@fileinfo = stat($filename);			# ファイル情報所得
		($sec,$min,$hour,$mday,$mon) = gmtime($fileinfo[9] + $TIMEZONE*3600);
		$retv = sprintf("%02d/%02d %02d:%02d",++$mon,$mday,$hour,$min);
	}
	else { $retv = ''; }

	return $retv;
}


# ---ChaBo call用サブルーチン
sub call_mail {

	local($buffer)  = '伝言板が更新されました by ChaBo';	# メールの本文
	local($headder) = '';					# メールのヘッダ
	local($mail)    = '';					# メール全体
	local($err)     = '';					# 戻りコード

	# ---ヘッダを作る
	$headder .= "To: $ML_TO\n";
	$headder .= "From: $ML_FROM\n";
	$headder .= "Subject: $ML_SUBJ\n";
	$headder .= "Content-Type: text/plain\; charset=iso-2022-jp\n";
	$headder .= "\n";

	# ---メール組み立て
	$mail = $headder.$buffer."\n";
								# クイックアクセス
	if($CC_QUICK) { $mail .= "\n".$SCRIPT.'?p=1&v=1'."\n"; }

	&jcode'sjis2jis(*mail);

	# ---メール送信
	$SENDMAIL .= " -t";

	if(open(MAIL, "| $SENDMAIL")) {
#	if(open(MAIL, ">./chabo/chabomail.txt")) {		# テスト用
		print MAIL $mail;
		close(MAIL);
	}
	else { $err = 'sendmailが使用できません。<BR>'; }

	return $err;
}


# ---クリッカブルメール
sub active_link {
	local($toencode) = @_[0];

	# SJIS 漢字1バイト目は [\x80-\x9f\xe0-\xfc]と仮定
	$toencode =~ s/[\x80-\x9f\xe0-\xfc]./$&\e/g;
	$toencode =~ s/[0-9A-Za-z]+[\-\.\w]*\@([0-9A-Za-z]+[\-\w]*\.){1,4}[0-9A-Za-z]+/<A HREF="mailto:$&">[Mail]<\/A>/g;
	$toencode =~ s/\e//g;
	return $toencode;
}


# ---クリッカブルメール(EZweb) (Ver3.20)
sub active_link_ez {
	local($toencode) = @_[0];
	$toencode =~ s/[\x80-\x9f\xe0-\xfc]./$&\e/g;

	if($ENV{'HTTP_X_UP_SUBNO'} =~ /[a-z][a-z]\.ezweb/ ) {		# @mail対応端末 (Ver3.20β4)
		$toencode =~ s/[0-9A-Za-z]+[\-\.\w]*\@([0-9A-Za-z]+[\-\w]*\.){1,4}[0-9A-Za-z]+/<A TASK="GOSUB" DEST="mailto:$&" LABEL="ﾒｰﾙ">[Mail]<\/A>/g;
	} else {						# その他のEZweb端末
		$toencode =~ s/[0-9A-Za-z]+[\-\.\w]*\@([0-9A-Za-z]+[\-\w]*\.){1,4}[0-9A-Za-z]+/<A TASK="GOSUB" DEST="device:home\/goto?svc=Email&SUB=sendMsg" VARS="TO=$&" LABEL="ﾒｰﾙ">[Mail]<\/A>/g;
	}

	$toencode =~ s/\e//g;
	return $toencode;
}


# ---簡易クリッカブルＵＲＬ (Ver3.20)
# (セキュリティ対策として、引数付きURLの引数部分(?より先)は無視する仕様にしています)
sub active_url {
	local($toencode) = @_[0];
	$toencode =~ s/(s?https?:\/\/[-_.!~*'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)/<A HREF="$1">[URL]<\/A>/g;
	return $toencode;
}


# ---簡易クリッカブルＵＲＬ(EZweb) (Ver3.20)
sub active_url_ez {
	local($toencode) = @_[0];
	$toencode =~ s/(s?https?:\/\/[-_.!~*'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)/<A TASK="GO" DEST="$1" LABEL="移動"> [URL$2]<\/A>/g;
	return $toencode;
}

# ---あたまとり機能 (Ver3.20)
# (セキュリティ対策として、引数付きURLの引数部分(?より先)は無視する仕様にしています)
sub active_initial {
	local($toencode) = @_[0];	
	$toencode =~ s/(?<=^「)(..)/<font color="#b22222">$1<\/font>/g;
	return $toencode;
}


# ---あたまとり機能(EZweb) (Ver3.20)
sub active_initial_ez {
	local($toencode) = @_[0];
	$toencode =~ s/(?<=^「)(..)/<font color="#b22222">$1<\/font>/g;
	return $toencode;
}

# ---キーワード機能 (Ver3.20)
# (セキュリティ対策として、引数付きURLの引数部分(?より先)は無視する仕様にしています)
sub active_word {
	local($toencode) = @_[0];	
	$toencode =~ s/($KEYWORD)/$1<font color="#b22222">【←大当たり！】<\/font>/g;
	return $toencode;
}


# ---キーワード機能(EZweb) (Ver3.20)
sub active_word_ez {
	local($toencode) = @_[0];
	$toencode =~ s/($KEYWORD)/$1<font color="#b22222">【←大当たり！】<\/font>/g;
	return $toencode;
}


# ---URLのエンコード
sub url_enc {
	local($toencode) = @_[0];

		# Hi-HOでは下の２行を削除してスルーにすると文字化けしない？
	$toencode =~ s/([^a-zA-Z0-9_.-])/uc sprintf("%%%02x",ord($1))/eg;
	$toencode =~ s/%20/+/g;
	return $toencode;
}


# ---iモード専用絵文字を除去
sub cut_isymbol {
	local($enc1) = @_[0];
	local($enc2) = '';
	local($str)  = '';
	local($ptr)  = 0;

	for($ptr=0; $ptr<length($enc1); $ptr++) {
		$str = substr($enc1, $ptr, 2);

								# 絵文字なら、スキップ
		if( $str =~ /^[\xf8\xf9].?/ ) { $ptr++; }
								# 絵文字以外の漢字なら、2バイトコピー
		elsif($str =~ /^[\x80-\x9f\xe0-\xf7\xf9-\xfc]./ ) {
			$enc2 .= $str;
			$ptr++;
		}
								# 漢字以外のコードなら、1バイトコピー
		else { $enc2 .= substr($enc1, $ptr, 1); }
	}
	return $enc2;
}


# ---J-SkyWeb用絵文字を除去
sub cut_jsymbol {
	local($_) = @_[0];

	s/\x1b\$G.+\x0f//g;
	return $_;
}


# ---メッセージバッファを掃き出す（引数:表示モード, 拡張ヘッダ, バッファ内容）
sub buf_flash {
	local($bf_mode, $bf_head, $bf_buff) = @_;
	local($bf_len);

	if($bf_mode == -1) {					# EZweb
		print "Content-Type: text/x-hdml; charset=Shift_jis\n";
	} elsif($bf_mode == -2) {				# -H"/PDX
		print "Content-Type: text/plain\n";
	} else {						# その他
		print "Content-Type: text/html\n";
	}

	if($bf_mode != -2) {
		$bf_buff =~ s/[\r\n]//g;			# Windows対策
		$bf_len = length($bf_buff);
		print "Content-Length: $bf_len\n";		# データ長送出
	}

	print $bf_head;						# 拡張ヘッダ送出
	print "\n";
	print $bf_buff;						# バッファ送出

	return;
}

# ---end of chabo.cgi
