#!/usr/bin/perl
##################################################
#
# MovableType�� i-mode�Ѵ�������ץ�
# ��MT4i��
my $version = "2.0";
# Copyright (C) ��Ŵ All rights reserved.
# Special Thanks
#           �����ꥦ���˼� & Tonkey
#
# About MT4i
#  ��http://www.hazama.nu/t2o2/mt4i.shtml
# Tonkey�����Tonkey Magic
#  ��http://tonkey.mails.ne.jp/
# �����ꥦ���˼ߤο����¤�Ȥ
#  ��http://valium.oops.jp/
#
# -- �������������� --
# �֤ä��㤱���Ԥ�������Фä���Ρ�ư���Ф�����פ�
# �����ǥ��󥰤��Ƥޤ�����Perl�˴ؤ��Ƥ��ǿ�Ʊ���ʤΤǡ�
# ������������������Ū��̤�Ϥ����Ϥ��ƼϤ���������
# -- �����������ޤ� --
#
##################################################

use strict 'vars';
use strict 'subs';
use CGI;

# �����ɤ߹���
# Config.pl��require�ڤ�¸�߳�ǧ
eval {require 'mt4ilib/Config.pl'; 1} || die &errorout('"./mt4ilib/Config.pl"�����դ���ޤ���');
my %cfg = Config::Read("./mt4icfg.cgi");

### valium add start
# MT4i�б���󥯤�����ɽ������ʸ��(�դ������ʤ����϶�ʸ����ˤ����
my @ainori_str = (
	  "<font color=\"#FFCC33\">&#63862;</font>",	# i-mode ����� EZWeb
	  "\x1B\$Fu\x0F",								# J-SKY
	  "(MT4i)"										# other
);
# �����б���󥯤�����ɽ������ʸ��(�դ������ʤ����϶�ʸ����ˤ����
my @ExitChtmlTrans_Str = (
	  "<font color=\"#FFCC33\">&#63862;</font>",	# i-mode ����� EZWeb
	  "\x1B\$Fu\x0F",								# J-SKY
	  "(�����б�)"									# other
);
### valium add end

unshift @INC, $cfg{MT_DIR} . 'lib';
unshift @INC, $cfg{MT_DIR} . 'extlib';

####################
# Encode.pm��̵ͭĴ��
my $ecd;
eval 'use Encode;';
if($@){
	$ecd = 0;
}else{
	$ecd = 1;
}

####################
# Jcode.pm��̵ͭĴ��
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
# User Agent �ˤ�륭��ꥢȽ��
# ���͡�http://specters.net/cgipon/labo/c_dist.html
my $ua;
my @user_agent = split(/\//,$ENV{'HTTP_USER_AGENT'});
my $png_flag;
if ($user_agent[0] eq 'ASTEL') {
	# �ɥå�i �Ѥν���
	$ua = 'other';
} elsif ($user_agent[0] eq 'UP.Browser') {
	# EZweb ��ü���Ѥν���
	$ua = 'ezweb';
} elsif ($user_agent[0] =~ /^KDDI/) {
	# EZweb WAP2.0 �б�ü���Ѥν���
	$ua = 'ezweb';
} elsif ($user_agent[0] eq 'PDXGW') {
	# H" �Ѥν���
	$ua = 'other';
} elsif ($user_agent[0] eq 'DoCoMo') {
	# i-mode �Ѥν���
	$ua = 'i-mode';
} elsif ($user_agent[0] eq 'J-PHONE') {
	# J-SKY �Ѥν���
	$ua = 'j-sky';
	
	# PNG����ɽ���Ǥ��ʤ�����Ϥ�������ʤΤǻ����˥����å�����
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
	# AirH"PHONE�Ѥν���
	$ua = 'i-mode';
} elsif ($user_agent[0] eq 'L-mode') {
	# L-mode �Ѥν���
	$ua = 'other';
} else {
	# ����ʳ�
	$ua = 'other';
}

####################
# AccessKey��ʸ��������
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
    # i-mode �ڤ� EZweb
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
# �����μ���
my $q = new CGI();

if (!$cfg{Blog_ID}) {
	$cfg{Blog_ID} = $q->param("id");	# blog ID
}
my $mode = $q->param("mode");			# �����⡼��
my $no = $q->param("no");				# ����ȥ꡼NO
my $eid = $q->param("eid");				# ����ȥ꡼ID
my $ref_eid = $q->param("ref_eid");		# �������Υ���ȥ꡼ID
my $page = $q->param("page");			# �ڡ���NO
my $sprtpage = $q->param("sprtpage");	# ʬ��ڡ�����
my $sprtbyte = $q->param("sprtbyte");	# �ڡ���ʬ��byte��
my $img = $q->param("img");				# ������URL
my $cat = $q->param("cat");				# ���ƥ���ID
my $post_from = $q->param("from");		# ��Ƽ�
my $post_mail = $q->param("mail");		# �᡼��
my $post_text = $q->param("text");		# ������

my $pw_text = $q->param("pw_text");		# �Ź沽�ѥ����
my $key = $q->param("key");				# �Ź沽����
my $entry_cat = $q->param("entry_cat");					# ����ȥ꡼�Υ��ƥ��꡼
my $entry_title = $q->param("entry_title");				# ����ȥ꡼�Υ����ȥ�
my $entry_text = $q->param("entry_text");				# ����ȥ꡼������
my $entry_text_more = $q->param("entry_text_more");		# ����ȥ꡼���ɵ�
my $entry_excerpt = $q->param("entry_excerpt");			# ����ȥ꡼�γ���
my $entry_keywords = $q->param("entry_keywords");		# ����ȥ꡼�Υ������
my $post_status = $q->param("post_status");				# ����ȥ꡼�Υ��ơ�����
my $allow_comments = $q->param("allow_comments");		# ����ȥ꡼�Υ����ȵ��ĥ����å�
my $allow_pings = $q->param("allow_pings");				# ����ȥ꡼��ping���ĥ����å�
my $text_format = $q->param("convert_breaks");			# ����ȥ꡼�Υƥ����ȥե����ޥå�
my $entry_created_on = $q->param("entry_created_on");	# ����ȥ꡼�κ�������

# PerlMagick ��̵ͭĴ��
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

my $data;	# ɽ��ʸ�����Ѥ��ѿ����������

#�������ѰŹ沽����������å�
my $admin_mode;
if (($key ne "")&&(&check_crypt($cfg{AdminPassword}.$cfg{Blog_ID},$key))){
	$admin_mode = 'yes';
}else{
	$admin_mode = 'no';
	$key = "";
}

####################
# mt.cfg���ɤ߹���
require MT;
my $mt = MT->new( Config => $cfg{MT_DIR} . 'mt.cfg', Directory => $cfg{MT_DIR} )
	or die MT->errstr;

####################
# blog ID�����ꤵ��Ƥ��ʤ��ä����ϥ��顼
if (!$cfg{Blog_ID}) {
	$data = "Error��������blog ID����ꤷ�Ƥ���������<br>";
	# blog����ɽ��
	$data .= "<br>";
	require MT::Blog;
	my @blogs = MT::Blog->load(undef,
							{unique => 1});

	# ������
	@blogs = sort {$a->id <=> $b->id} @blogs;
	
	$data .= '<table border="1">';
	$data .= '<tr><th style="color:#FF0000;">blog ID</th><th>blog Name</th><th>Description</th></tr>';
	
	# ɽ��
	for my $blog (@blogs) {
		my $blog_id = $blog->id;
		my $blog_name = &conv_euc_z2h($blog->name);
		my $blog_description = &conv_euc_z2h($blog->description);
		$data .= "<tr><th style=\"color:#FF0000;\">$blog_id</th><td><a href=\"./$cfg{MyName}?id=$blog_id\">$blog_name</a></td><td>$blog_description</td></tr>";
	}

	$data .= '</table><br><span style="font-weight:bold;">blog ID �λ�����ˡ��</span><br>��MT4i.cgi ������ˤ� "<span style="font-weight:bold;">$blog_id</span>" �˾嵭 <span style="color:#FF0000;font-weight:bold;">blog ID</span> ����ꤹ�뤫��<br>���⤷���Ͼ嵭 <span style="color:#FF0000;font-weight:bold;">blog Name</span> �ˎ؎ݎ�����Ƥ��� URL �ǎ����������롣';
	
	&errorout;
	exit;      # exit����
}

####################
# PublishCharset�μ���
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
# blog̾�ڤӳ��פμ���
require MT::Blog;
my $blog = MT::Blog->load($cfg{Blog_ID},
					  {unique => 1});

# ������blog ID
if (!$blog) {
	$data = "ID '$cfg{Blog_ID}' ��blog��¸�ߤ��ޤ���";
	&errorout;
	exit;      # exit����
}

# blog̾�����ס������ȴ�Ϣ������ѿ��˳�Ǽ
my $blog_name = &conv_euc_z2h($blog->name);
my $description = &conv_euc_z2h($blog->description);
my $sort_order_comments = $blog->sort_order_comments;
my $email_new_comments = $blog->email_new_comments;
my $email_new_pings = $blog->email_new_pings;
my $convert_paras = $blog->convert_paras;
my $convert_paras_comments = $blog->convert_paras_comments;

####################
# ����$mode��Ƚ��
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


# �������ѥХå��ɥ���ɽ��
if ($cfg{AdminDoor} eq "yes"){
	if ($mode eq 'admindoor')	{ &admindoor }
}

#--- ����������ϴ����⡼�ɤǤ����¹ԤǤ��ʤ� ---

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
# Sub Main - �ȥåץڡ���������
########################################

sub main {
	if(!$mode && !$page) { $page = 0 }
	if ($cfg{AccessKey} eq "yes" && ($ua eq "i-mode" || $ua eq "j-sky" || $ua eq "ezweb")) {
		# �������ä���Υ����������ĥ�����������ͭ���ξ���$cfg{DispNum}��6�ʲ��ˤ���
		if ($cfg{DispNum} > 6) {
			$cfg{DispNum} = 6;
		}
	}
	my $rowid;
	if($page == 0) { $rowid = 0 } else { $rowid = $page * $cfg{DispNum} }
	
	####################
	# �����μ���
	my $ttlcnt = &get_ttlcnt;
	
	####################
	# �����μ���
	my @entries = &get_entries($rowid, $cfg{DispNum});
	
	# ������̤�0��ξ��ϥ�å�����ɽ������STOP
	if (@entries <= 0) {
		$data = "������̤�0��Ǥ���<br>";
		&errorout;
		exit;      # exit����
	}
	
	# �������������$cfg{DispNum}��꾯�ʤ���ǽ��������١�
	my $rowcnt = @entries + 1;
	
	####################
	# ɽ��ʸ��������
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
	
	# �����ԥ⡼��
	if ($admin_mode eq 'yes'){
		$data .= "<h2 align=\"center\"><font color=\"$cfg{TitleColor}\">�����ԥ⡼��</font></h2>";
	}
	
	if ($cfg{Dscrptn} eq "yes" && $page == 0 && $description) {
		my $tmp_data .= "<hr><center>$description</center>";
		#ñ�ʤ���Ԥ�<br>�������ִ�
		#(�֥����֥��������פ˲��Ԥ��������au��ɽ������ʤ��Զ��ؤ��н�)
		$tmp_data=~s/\r\n/<br>/g;
		$tmp_data=~s/\r/<br>/g;
		$tmp_data=~s/\n/<br>/g;
		$data .= $tmp_data;
	}
	$data .= "<hr>";
	
	# ���ƥ��ꥻ�쥯��
	$data .= "<center><form action=\"$cfg{MyName}\">";
	if ($key){
		$data .= "<input type=hidden name=\"key\" value=\"$key\">";
	}
	$data .= "<select name=\"cat\">";
	$data .= "<option value=0>���٤�";

	my @cat_datas = ();
	require MT::Category;
	my @categories = MT::Category->load({blog_id => $cfg{Blog_ID}},
											{unique => 1});
	for my $category (@categories) {
		my $label;
		
		# ���ƥ���̾�����ܸ첽��$MTCategoryDescription��ɽ�����Ƥ������
		# ���ƥ��ꥻ�쥯�������Ƥ��ִ�����
		if ($cfg{CatDescReplace} eq "yes"){
			$label = &conv_euc_z2h($category->description);
		}else{
			$label = &conv_euc_z2h($category->label);
		}
		my $cat_id = $category->id;
		require MT::Entry;
		require MT::Placement;
		# ����ȥ꡼��1�ʾ�Τ�ΤΤ����
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
	$data .= "<input type=submit value=\"����\"></form></center>";
	$data .= "<hr>";
	
	# ������ʸ
	my $i = 0;
	for my $entry (@entries){ # ��̤Υե��å���ɽ��
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
		if ($comment_cnt > 0 && $cfg{CommentColor} ne 'no'){ #�����ȿ���������ղ�
			$data .= "<font color=\"$cfg{CommentColor}\">[$comment_cnt]</font>";
		}
		if ($ping_cnt > 0 && $cfg{TbColor} ne 'no'){ #�ȥ�å��Хå�����������ղ�
			$data .= "<font color=\"$cfg{TbColor}\">[$ping_cnt]</font>";
		}
		$data .= "<br>";
	}
	
	# �ǽ��ڡ����λ���
	if ($ttlcnt >= $cfg{DispNum}) {
		my $lastpage = int($ttlcnt / $cfg{DispNum});	# int()�Ǿ������ʲ����ڤ�Τ�
		my $amari = $ttlcnt % $cfg{DispNum};			# ;��λ���
		if ($amari > 0) { $lastpage++ }				# ���ޤ꤬���ä���+1
		my $ttl = $lastpage;						# ���Υڡ�����ɽ���Ѥ��ͼ���
		$lastpage--;								# �Ǥ�ڡ�����0����ϤޤäƤ�Τ�-1�ʤʤ󤫴�ȴ����
		
		# �ڡ�����ɽ��
		my $here = $page + 1;
		$data .= "<center>$here/$ttl</center><hr>";
	
		# �����ѥڡ������׻�
		my $nextpage = $page + 1;
		my $prevpage = $page - 1;
		
		# ���������ǽ�
		if ($rowid < $ttlcnt) {
			my $href = &make_href("", 0, $nextpage, 0, 0);
			if ($page == $lastpage - 1 && $amari > 0) {
				$data .= "$nostr[9]<a href=\"$href\"$akstr[9]>����$amari�� &gt;</a><br>";
			} else {
				$data .= "$nostr[9]<a href=\"$href\"$akstr[9]>����$cfg{DispNum}�� &gt;</a><br>";
			}
		}
		$rowid = $rowid - $rowcnt;
		if ($rowid > 0) {
			my $href = &make_href("", 0, $prevpage, 0, 0);
			$data .= "$nostr[7]<a href=\"$href\"$akstr[7]>&lt; ����$cfg{DispNum}��</a><br>";
		}
		if ($page > 1) {
			my $href = &make_href("", 0, 0, 0, 0);
			$data .= "$nostr[0]<a href=\"$href\"$akstr[0]>&lt;&lt; �ǽ��$cfg{DispNum}��</a><br>";
		}
		
		# �ֺǸ�ץ�󥯤�ɽ��Ƚ��
		if ($page < $lastpage - 1) {
			my $href = &make_href("", 0, $lastpage, 0, 0);
			if ($amari > 0) {
				$data .= "$nostr[8]<a href=\"$href\"$akstr[8]>�Ǹ��$amari�� &gt;&gt;</a><br>";
			} else {
				$data .= "$nostr[8]<a href=\"$href\"$akstr[8]>�Ǹ��$cfg{DispNum}�� &gt;&gt;</a><br>";
			}
		}
	} else {
		$data .= "<center>1/1</center>";
	}

	# �Ƕ�Υ����Ȱ����ؤΥ��
	if ($page == 0) {
		require MT::Comment;
		my $blog_comment_cnt = MT::Comment->count({ blog_id => $cfg{Blog_ID} });
		if ($blog_comment_cnt) {
			my $href = &make_href("recentcomment", 0, 0, 0, 0);
			$data .= "<hr><a href=\"$href\">�Ƕ�Ύ��Ҏݎ�$cfg{RecentComment}��</a>";
		}
	}
	
	# ��������URL�ؤΥ�󥯤�ɽ������
	if ($cfg{AdminDoor} eq "yes"){
		$data .= "<hr>";
		my $href = &make_href("admindoor", 0, 0, 0);
		$data .= "<form method=\"post\" action=\"$href\">";
		$data .= "��������URL�����<br>";
		$data .= "\AdminPassword����";
		$data .= "<br><input type=\"text\" name=\"pw_text\" istyle=3><br>";
		$data .= "<input type=\"hidden\" name=\"id\" value=\"$cfg{Blog_ID}\">";
		$data .= "<input type=\"hidden\" name=\"mode\" value=\"admindoor\">";
		$data .= "<input type=\"submit\" value=\"����\">";
		if ($key){
			$data .= "<input type=hidden name=\"key\" value=\"$key\">";
		}
		$data .= "</form>";
		
		if ($admin_mode eq "yes"){
			$data .= '<font color="red">���ʤ��ϴ�������URL������ѤߤǤ�������URL��̎ގ����ώ��������塢®�䤫�ˡ�MT4i Manager�פˤ�"AdminDoor"���ͤ�"no"���ѹ����Ƥ���������</font><br>';
		}
		if ($cfg{AdminPassword} eq "password"){
			$data .= '<font color="red">"AdminPassword"���Îގ̎��َ���"password"�����ѹ�����Ƥ��ޤ��󡣤��Τޤޤ���¾�ͤ˴�����URL���¬������ǽ�������˹⤯�ʤ�ޤ���®�䤫���ѹ����Ƥ���������</font><br>';
		}
	}
	
	#�������ѥ�˥塼
	if ($admin_mode eq "yes"){
		$data .= "<hr>";
		my $href = &make_href("entryform", 0, 0, 0, 0);
		$data .= "<a href='$href'>[��]Entry�ο�������</a><br>";
		
		my $href = &make_href("email_comments", 0, 0, 0, 0);
		if ($email_new_comments){
			$data .= "<a href='$href'>[��]���ҎݎĤΎҎ������Τ���ߤ���</a><br>";
		}else{
			$data .= "<a href='$href'>[��]���ҎݎĤΎҎ������Τ�Ƴ�����</a><br>";
		}
		$data .= "<hr>";
	}
	
	&htmlout;
}

########################################
# Sub Individual - ñ�����ڡ���������
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
	# �����μ���
	require MT::Entry;
	my $entry = MT::Entry->load($eid);

	# ������̤�0��ξ��ϥ�å�����ɽ������STOP��ͭ�����ʤ����ɤʡ�
	if (!$entry) {
		$data = "Entry ID '$eid' �������Ǥ���";
		&errorout;
		exit;      # exit����
	}

	# ��̤��ѿ��˳�Ǽ
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
	
	# ��ʸ���ɵ����ĤˤޤȤ��
	if($text_more){
		$text = "<p>$text</p><p>$text_more</p>";
	}
	
	####################
	# ��󥯤�URL��chtmltrans��ͳ���Ѵ�
	$text = &chtmltrans($text, $rowid, $eid);
	
	####################
	# <img>����������URL�Υ���å����%2F���Ѵ�
	$text = &img_url_conv($text);
	
	####################
	# �����ν���������
	
	# a������ޤ᤿���ALT��ɽ���������ؤΥ��
	my $href = &make_href("image", $rowid, 0, $eid, 0);
	$text =~ s/<a[^>]*><img[^>]*src=["']([^"'>]*)["'][^>]*alt=["']([^"'>]*)["'][^>]*><\/a>/&lt;<a href="$href&amp;img=$1">������$2<\/a>&gt;/ig;
	$text =~ s/<a[^>]*><img[^>]*alt=["']([^"'>]*)["'][^>]*src=["']([^"'>]*)["'][^>]*><\/a>/&lt;<a href="$href&amp;img=$2">������$1<\/a>&gt;/ig;
	
	# img�����Τߤν��ALT��ɽ���������ؤΥ��
	$text =~ s/<img[^>]*src=["']([^"'>]*)["'][^>]*alt=["']([^"'>]*)["'][^>]*>/&lt;<a href="$href&amp;img=$1">������$2<\/a>&gt;/ig;
	$text =~ s/<img[^>]*alt=["']([^"'>]*)["'][^>]*src=["']([^"'>]*)["'][^>]*>/&lt;<a href="$href&amp;img=$2">������$1<\/a>&gt;/ig;
	
	# a������ޤ᤿��������ؤΥ��
	$text =~ s/<a[^>]*><img[^>]*src=["']([^"'>]*)["'][^>]*><\/a>/&lt;<a href="$href&amp;img=$1">����<\/a>&gt;/ig;
	
	# img�����Τߤν�������ؤΥ��
	$text =~ s/<img[^>]*src=["']([^"'>]*)["'][^>]*>/&lt;<a href="$href&amp;img=$1">����<\/a>&gt;/ig;
	
	####################
	# �����Ѵ���
	if($convert_breaks eq '__default__' || ($convert_breaks ne '__default__' && $convert_breaks ne '0' && $convert_paras eq '__default__')) {
		# bq�������ο��ѹ�
		if ($cfg{BqColor}) {
			$text=~s/<blockquote>/<blockquote><font color="$cfg{BqColor}">/ig;
			$text=~s/<\/blockquote>/<\/font><\/blockquote>/ig;
		}
		# bq������p�����ؤ��Ѵ�
		if ($cfg{BQ2P} eq "yes") {
			$text=~s/<blockquote>/<p>/ig;
			$text=~s/<\/blockquote>/<\/p>/ig;
		} else {
			# bq���������;�פ�br��������
			$text=~s/<br><br><blockquote>/<blockquote>/ig;
			$text=~s/<br><blockquote>/<blockquote>/ig;
			$text=~s/<\/blockquote><br><br>/<\/blockquote>/ig;
			$text=~s/<p><blockquote>/<blockquote>/ig;
			$text=~s/<\/blockquote><\/p>/<\/blockquote>/ig;
		}
		# p���������;�פ�br��������
		$text=~s/<br \/><br \/><p>/<p>/ig;
		$text=~s/<br \/><p>/<p>/ig;
		$text=~s/<\/p><br \/><br \/>/<\/p>/ig;
		$text=~s/<br \/><\/p>/<\/p>/ig;
		# ul���������;�פ�br��������
		$text=~s/<br \/><br \/><ul>/<ul>/ig;
		$text=~s/<br \/><ul>/<ul>/ig;
		$text=~s/<ul><br \/>/<ul>/ig;
		$text=~s/<\/ul><br \/><br \/>/<\/ul>/ig;
		# ol���������;�פ�br��������
		$text=~s/<br \/><br \/><ol>/<ol>/ig;
		$text=~s/<br \/><ol>/<ol>/ig;
		$text=~s/<ol><br \/>/<ol>/ig;
		$text=~s/<\/ol><br \/><br \/>/<\/ol>/ig;
	}
	
	####################
	# ��ʸʬ�����
	if (&lenb_euc($text) > $cfg{SprtLimit}) {
		$text = &separate($text, $rowid);
	}
	
	####################
	# ɽ��ʸ��������
	$data .= "<h4>";
	
	# ������������α����ʤ鵭���ֹ�򿶤�
	if ($mode eq 'individual') {
		$data .= "$rowid.";
	}
	
	# ���񤭡����������ɤ�����Ĵ�٤�
	my $d_f;
	if ($ent_status == 1) {
		$d_f = '(����)';
	} elsif ($ent_status == 3) {
		$d_f = '(������)';
	}
	
	$data .= "$d_f$title";
	
	# ���ƥ���̾��ɽ��
	if ($cfg{IndividualCatLabelDisp} eq 'yes') {
		my $cat_label = &check_category($entry);
		$data .= "[$cat_label]";
	}
	
	if ($cfg{IndividualAuthorDisp} eq 'yes') {
		# Author��nickname������С������ɽ����̵�����name��ɽ������
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
	# ������������α����ʤ鵭���ֹ�򿶤�
	if ($mode eq 'individual') {
		# ��������
		$ttlcnt = &get_ttlcnt;
		
		# ����ȥ꡼��ɽ��
		$data .= "<center>$rowid/$ttlcnt</center><hr>";
	} else {
		$data .= "<hr>";
	}
	
	#####################
	# None�Ǥ���Ƥ�ɽ����̵����Open�ʤ�ξ��OK��Closed��ɽ���Τ�
	# $comment_cnt���� None=0,Open=1,Closed=2
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
				# �����Τ���ϥ����Ȼ��ȤǤ��ʤ��褦�ˡ�
				# ���Τäƿ������ݤ����餵�á�
				$data .= "$nostr[8]<a href=\"$href\"$akstr[8]>���Ҏݎ�($comment_cnt)</a><hr>";
			}
		} elsif ($ent_allow_comments == 1) {
			if ($mode eq 'individual') {
				$href = &make_href("postform", $rowid, 0, $eid, 0);
				$data .= "$nostr[8]<a href=\"$href\"$akstr[8]>���Ҏݎ����</a><hr>";
			} elsif ($mode eq 'individual_rcm') {
				$href = &make_href("postform_rcm", $rowid, 0, $eid, 0);
				$data .= "$nostr[8]<a href=\"$href\"$akstr[8]>���Ҏݎ����</a><hr>";
			}
				# ���⡼�ɡ�comment_lnk�פλ��ϥ�������ƤǤ��ʤ���
				# ��������Ū�ʤ�����饳���Ƚ񤯤���̵���Ǥ��硢���֤�
		}
	}
	
	# Trackback
	if ($ping_cnt > 0) {
		$href = &make_href("trackback", $rowid, 0, $eid);
		$data .= "$nostr[9]<a href=\"$href\"$akstr[9]>�Ď׎����ʎގ���($ping_cnt)</a><hr>";
	}

	# �����ԤΤߡ�Entry�Խ����õ�פ���ǽ
	if ($admin_mode eq "yes"){
		$href = &make_href("entryform", $rowid, 0,$eid, 0);
		$data .="<a href='$href'>[��]����Entry���Խ�</a><br>";
		$href = &make_href("confirm_entry_del", $rowid, 0,$eid, 0);
		$data .="<a href='$href'>[��]����Entry����</a><hr>";
	}
	
	if ($mode eq 'individual') {
		# ������������α���
		# �����ѥ���ȥ꡼NO����
		my $nextno = $rowid + 1;
		my $prevno = $rowid - 1;
		
		# �����ѥ���ȥ꡼ID���С�prev��next�����÷����֤äƤ���Τ���ա�
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
			$data .= "$nostr[9]<a href=\"$href\"$akstr[9]>���ε����� &gt;</a><br>";
		}
		if($rowid > 1) {
			$href = &make_href("individual", $prevno, 0, $previd, 0);
			$data .= "$nostr[7]<a href=\"$href\"$akstr[7]>&lt; ���ε�����</a><br>";
		}
		# �ڡ���������
		$page = int($no / $cfg{DispNum});	# int()�Ǿ������ʲ����ڤ�Τ�
		
		$href = &make_href("", 0, $page, 0, 0);
		$data .= "$nostr[0]<a href=\"$href\"$akstr[0]>���������</a>";
	} elsif ($mode eq 'individual_rcm') {
		# �Ƕᥳ���Ȱ�������α���
		$href = &make_href("recentcomment", 0, 0, 0, 0);
		$data .= "$nostr[0]<a href=\"$href\"$akstr[0]>�ǶᎺ�Ҏݎİ��������</a>";
	} elsif ($mode eq 'individual_lnk') {
		# �������󥯤���α���
		$href = &make_href("individual", $rowid, 0, $ref_eid, 0);
		$data .= "$nostr[0]<a href=\"$href\"$akstr[0]>�؎ݎ����ε��������</a>";
	} elsif ($mode eq 'ainori') {
		# �����Τ���ϥ�ե�������
		$href = $ENV{'HTTP_REFERER'};
		$data .= "$nostr[0]<a href=\"$href\"$akstr[0]>�؎ݎ��������</a>";
	}
	
	&htmlout;
}

########################################
# Sub Comment - ����������
########################################

sub comment {
	my $rowid = $no;
	
	####################
	# entry id�μ���
	require MT::Entry;
	my $entry = MT::Entry->load($eid);

	# ������̤�0��ξ��ϥ�å�����ɽ������STOP��ͭ�����ʤ����ɤʡ�
	if ($entry <= 0) {
		$data = "Entry ID '$eid' �������Ǥ���";
		&errorout;
		exit;      # exit����
	}

	# ��̤��ѿ��˳�Ǽ
	my $ent_title = &conv_euc_z2h($entry->title);
	my $ent_created_on = &conv_euc_z2h(&conv_datetime($entry->created_on));
	my $ent_id = $entry->id;
	my $ent_allow_comments = $entry->allow_comments;
	
	####################
	# �����Ȥμ���
	my @comments;
	# �����ԥ⡼�ɤǤϥ����Ȥ�ս�ɽ������
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
		
		# �����ԤΤߡ֥����Ⱦõ��������ǽ
		if ($admin_mode eq "yes"){
			my $href = &make_href("confirm_comment_del", $rowid, $comment->id, $eid, 0);
			$text .="<br><_ahref=\'$href\'>[��]���Ύ��ҎݎĤ���</a><br>";
			#$href = &make_href("confirm_comment_ipban", $rowid, $comment->id, $eid, 0);
			#$text .="<_ahref=\'$href\'>[��]����IP����Υ����Ȥ�ػߡ������</a>";
		}
	}

	####################
	# �����Ѵ���
	if($convert_paras_comments eq '__default__'){
		# ���Ԥ�br�����ؤ��Ѵ�
		$text=~s/\r\n/<br>/g;
		$text=~s/\r/<br>/g;
		$text=~s/\n/<br>/g;
	}

	####################
	# ��󥯤�URL��chtmltrans��ͳ���Ѵ�
	$text = &chtmltrans($text, $rowid, $eid);
	
	####################
	# <_ahref>��<a href>���᤹
	$text=~s/_ahref/a href/g;
	
	####################
	# ��ʸʬ�����
	if (&lenb_euc($text) > $cfg{SprtLimit}) {
		$text = &separate($text, $rowid);
	}
	
	####################
	# ɽ��ʸ��������
	$data .= "<h4>";
	if ($rowid) {
		$data .= "$rowid.";
	}
	if ($admin_mode eq "yes"){
		$data .= "$ent_title$ent_created_on�ؤΎ��Ҏݎ�(��������)</h4>";
	}else{
		$data .= "$ent_title$ent_created_on�ؤΎ��Ҏݎ�</h4>";
	}
	$data .= "$text<hr>";
	if ($ent_allow_comments == 1){
		if ($mode eq 'comment') {
			my $href = &make_href("postform", $rowid, 0, $eid, 0);
			$data .= "$nostr[8]<a href=\"$href\"$akstr[8]>���Ҏݎ����</a><hr>";
		} elsif ($mode eq 'comment_rcm') {
			my $href = &make_href("postform_rcm", $rowid, 0, $eid, 0);
			$data .= "$nostr[8]<a href=\"$href\"$akstr[8]>���Ҏݎ����</a><hr>";
		}
			# ���⡼�ɡ�comment_lnk�פλ��ϥ�������ƤǤ��ʤ���
			# ��������Ū�ʤ�����饳���Ƚ񤯤���̵���Ǥ��硢���֤�
	}
	my $href = &make_href("individual", $rowid, 0, $eid, 0);
	if ($mode eq 'comment') {
		$data .= "$nostr[0]<a href=\"$href\"$akstr[0]>���������</a>";
	} else {
		if ($mode eq 'comment_rcm') {
			$href =~ s/individual/individual_rcm/ig;
		} elsif ($mode eq 'comment_lnk') {
			$href = &make_href("individual_lnk", $rowid, 0, $eid, $ref_eid);
		}
		$data .= "$nostr[7]<a href=\"$href\"$akstr[7]>���������ɤ�</a><hr>";
		if ($mode eq 'comment_rcm') {
			my $href = &make_href("recentcomment", 0, 0, 0, 0);
			$data .= "$nostr[0]<a href=\"$href\"$akstr[0]>�ǶᎺ�Ҏݎİ��������</a>";
		} elsif ($mode eq 'comment_lnk') {
			my $href = &make_href("individual", $rowid, 0, $ref_eid, 0);
			$data .= "$nostr[0]<a href=\"$href\"$akstr[0]>�؎ݎ����ε��������</a>";
		}
	}

	&htmlout;
}

########################################
# Sub Recent_Comment - �����ȤޤȤ��ɤ�
########################################

sub recent_comment {
	
	####################
	# �����Ȥμ���
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
	# ɽ��ʸ��������
	$data .= "<h4>�Ƕ�Υ�����$cfg{RecentComment}��</h4>";
	$data .= "$text<hr>";
	
	my $href = &make_href("", 0, 0, 0, 0);
	$data .= "<br>$nostr[0]<a href='$href'$akstr[0]>���������</a>";

	&htmlout;
}

########################################
# Sub Trackback - �ȥ�å��Хå�ɽ��
########################################

sub trackback {
	
	my $rowid = $no;
	
	####################
	# �ȥ�å��Хå��μ���
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
		# �����ԤΤߡ֥ȥ�å��Хå������������ǽ
		if ($admin_mode eq "yes"){
			my $href = &make_href("confirm_trackback_del", $rowid, $ping_id, $eid, 0);
			$text .="<_ahref=\'$href\'>[��]����TB����</a><br>";
			#$href = &make_href("confirm_trackback_ipban", $rowid, $ping_id, $eid, 0);
			#$text .="<_ahref=\'$href\'>[��]����IP�����TB��ػߡ������</a>";
		}
	}
	
	####################
	# ��󥯤�URL��chtmltrans��ͳ���Ѵ�
	$text = &chtmltrans($text);
	
	####################
	# <_ahref>��<a href>���᤹
	$text=~s/_ahref/a href/g;
	
	####################
	# ɽ��ʸ��������
	if (@tbpings < $cfg{RecentTB}){
		$cfg{RecentTB} = @tbpings;
	}
	
	$data .= "<h4>����Entry�ؤκǶ�ΎĎ׎����ʎގ���$cfg{RecentTB}��(��������)</h4>";
	$data .= "$text<hr>";
	
	my $href = &make_href("individual", $rowid, 0, $eid);
	$data .= "$nostr[0]<a href=\"$href\"$akstr[0]>���������</a>";
	
	&htmlout;
}

#############################################
# Sub Get_Entries - ����ȥ�μ���
# ������ : ���ե��å�
# ������� : �����Ŀ�
# �����Ԥξ��ˤϡ�status�θ�����
#############################################
sub get_entries {
	my @ent;
	require MT::Entry;
	
	if ($admin_mode eq "yes"){
		if ($cat == 0) {
			# ���ƥ������ʤ�
			@ent = MT::Entry->load(
				 { blog_id => $cfg{Blog_ID} },
				 { limit => $_[1],
				   offset => $_[0],
				   sort => 'created_on',
				   direction => 'descend' });
		} else {
			# ���ƥ�����ꤢ��
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
			# ���ƥ������ʤ�
			@ent = MT::Entry->load(
				 { blog_id => $cfg{Blog_ID},
				   status => 2 },
				 { limit => $_[1],
				   offset => $_[0],
				   sort => 'created_on',
				   direction => 'descend' });
		} else {
			# ���ƥ�����ꤢ��
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
# Sub Get_Comments - �����Ȥμ���
# ������ : ����ȥ꡼ID
# ������� : �����Ŀ�
# �軰���� : �����ȹ߽硿����
# ��Ͱ��� : visible�ͥ����å���̵ͭ 1:ͭ 0:̵
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
# Sub Get_Ttlcnt - ��������μ���
##############################################
sub get_ttlcnt {
	require MT::Entry;
	require MT::Placement;
	if ($cat == 0) {
		#���ƥ���ʤ�
		return MT::Entry->count({blog_id => $cfg{Blog_ID}, status => 2},
				{sort => 'created_on',
				 direction => 'descend',
				 unique => 1});
	} else {
		#���ƥ��ꤢ��
		return MT::Entry->count({blog_id => $cfg{Blog_ID}, status => 2}, {
				join => [ 'MT::Placement', 'entry_id', { blog_id => $cfg{Blog_ID},
														   category_id => $cat } ],
				sort => 'created_on',
				direction => 'descend',
				unique => 1});
	}
}

##############################################
# Sub Make_Href - HREFʸ����κ���
# ������ : mode
# ������� : no
# �軰���� : page
# ��Ͱ��� : eid
# ��ް��� : ref_eid
#
# �㳰�Ȥ��ơ�$mode��"post"�ξ��ˤ�
# id����Ϥ��ޤ���
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
# Sub Image - ����ɽ��
########################################

sub image {
	# PerlMagick ��̵����в����̾�ɽ�������Ϥ��ʤ�
	if ($imk == 0){
		$img =~ s/\%2F/\//ig;
		$data .="<p><img src=\"$img\"></p>";
	}else{
        # /��%2F�˺ƥ��󥳡���
		$img =~ s/\//\%2F/ig;
		$data .="<p><img src=\"./$cfg{MyName}?mode=img_cut&amp;id=$cfg{Blog_ID}&amp;img=$img\"></p>";
	}
	my $href = &make_href("individual", $no, 0, $eid, 0);
	$data .="$nostr[0]<a href=\"$href\"$akstr[0]>���</a>";
	
	&htmlout;
}

########################################
# Sub Image_Cut - �����̾�ɽ��
########################################

sub image_cut {
	$img =~ s/\%2F/\//ig;
	my $url = $img;
	$url =~ s/http:\/\///;
	my $host = substr($url, 0, index($url, "/"));
	my $path = substr($url, index($url, "/"));
	$data = "";

	####################
	# �ۥ���̾�ִ�
	if ($host eq $cfg{Photo_Host_Original}){
		$host = $cfg{Photo_Host_Replace};
	}
	
	####################
	# �����ɤ߹��ߤ�LWP�⥸�塼����Ѥ��ѹ�
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
	# vodafone�����굡��˸¤�png������ʳ���jpg���Ѵ�
	# �������˴ؤ�餺��png�⤷����jpg���Ѵ�����褦���ѹ�
	my $image = Image::Magick->new;
	$image->BlobToImage(@blob);
	
	# �ǥ�����ʤɤΥ��ץꥱ����������κ��
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
	
	# ���͡�http://deneb.jp/Perl/mobile/
	my $start_pos = 0;
	my $user_agent = $ENV{'HTTP_USER_AGENT'};
	my $cache_limit = -1024 + &calc_cache_size( $user_agent );
	# ���������˥���å�������ϰ���ʤ�̾��������ʤ�
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
# Sub Postform - ��������ƥե�����
########################################

sub postform {
	my $rowid = $no;
	
	# Entry����
	require MT::Entry;
	my $entry = MT::Entry->load($eid);

	# ������̤�0��ξ��ϥ�å�����ɽ������STOP��ͭ�����ʤ����ɤʡ�
	if ($entry <= 0) {
		$data = "Entry ID '$eid' �������Ǥ���";
		&errorout;
		exit;      # exit����
	}

	# ��̤��ѿ��˳�Ǽ
	my $ent_title = &conv_euc_z2h($entry->title);
	my $ent_created_on = &conv_euc_z2h(&conv_datetime($entry->created_on));

	####################
	# ɽ��ʸ��������
	$data = "<h4>";
	if ($rowid) {
		$data .= "$rowid.";
	}
	$data .= "$ent_title$ent_created_on�ؤΎ��Ҏݎ����</h4><hr>";
	if ($mt->version_number() >= 3.0 && $cfg{ApproveComment} eq 'no') {
		$data .= "���ҎݎĤ���Ƹ塢�Ǻܤ���α����ޤ���<br>�����ͤˤ�뾵���塢�Ǻܤ���ޤ���<br>";
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
	$data .= "̾��";
	if ($cfg{PostFromEssential} ne "yes"){
		$data .= "(��ά��)";
	}
	$data .= "<br><input type=text name=from><br>";
	$data .= "�Ҏ��َ��Ďގڎ�";
	if ($cfg{PostMailEssential} ne "yes"){
		$data .= "(��ά��)";
	}
	$data .= "<br><input type=text name=mail><br>";
	$data .= "���Ҏݎ�";
	if ($cfg{PostTextEssential} ne "yes"){
		$data .= "(��ά��)";
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
	$data .= "�������פ򲡤��Ƥ���񤭹��ߴ�λ�ޤ�¿�����֤�������ޤ���<br>�Ķ��ˤ�äƤώ����ю����Ĥ��Ф뤳�Ȥ�����ޤ������񤭹��ߤϴ�λ���Ƥ��ޤ���<br>�������פ����ٲ��������Фˤ��ʤ��ǲ�������<br>";
	$data .= "<input type=hidden name=no value=$rowid>";
	$data .= "<input type=hidden name=eid value=$eid>";
	if ($key){
		$data .= "<input type=hidden name=\"key\" value=\"$key\">";
	}
	$data .= "<input type=submit value='����'>";
	$data .= "</form>";
	$data .= "<hr>";
	if ($mode eq 'postform') {
		$href = &make_href("individual", $rowid, 0, $eid, 0);
	} elsif ($mode eq 'postform_rcm') {
		$href = &make_href("individual_rcm", $rowid, 0, $eid, 0);
	} elsif ($mode eq 'postform_lnk') {
		$href = &make_href("individual_lnk", $rowid, 0, $eid, 0);
	}
	$data .="$nostr[0]<a href='$href'$akstr[0]>���</a>";
	&htmlout;
}

########################################
# Sub Post - ���������->ɽ������
########################################
sub post {
	require MT::Comment;
	require MT::App;
	

	my $rowid = $no;
	$no--;
	
	# ������Ƥ��öEUC-JP���Ѵ�
	&$jcnv(\$post_from, 'euc', 'sjis');
	&$jcnv(\$post_mail, 'euc', 'sjis');
	&$jcnv(\$post_text, 'euc', 'sjis');
	
	####################
	# admin_helper������å�(�����ԥ⡼�ɻ��Τ�)
	my $post_from_org = $post_from;
	if (($cfg{AdminHelper} eq 'yes') && ($admin_mode eq 'yes')){
		if ($post_from_org eq $cfg{AdminHelperID}){
			$post_from = $cfg{AdminHelperNM};
			$post_mail = $cfg{AdminHelperML};
		}
	}
	
	####################
	# ɬ�����Ϲ��ܤ�����å�
	# ̾��,mail,text�Τɤ�����Ϥ�̵����Х��顼
	if(((!$post_from)&&(!$post_text)&&(!$post_mail))||
       ((!$post_from)&&($cfg{PostFromEssential} eq "yes"))||
       ((!$post_mail)&&($cfg{PostMailEssential} eq "yes"))||
       ((!$post_text)&&($cfg{PostTextEssential} eq "yes")))
	{
		$data .="Error!<br>̤���Ϲ��ܤ�����ޤ�.<br>";
		my $href = &make_href("postform", $rowid, 0, $eid, 0);
		$data .="$nostr[0]<a href='$href'$akstr[0]>���</a>";
		&errorout;
		return;
	}
	
	####################
	# �᡼�륢�ɥ쥹�����å�
	if ($post_mail){
		unless($post_mail=~/^[\w\-+\.]+\@[\w\-+\.]+$/i){
			$data .="Error!<br>�Ҏ��َ��Ďގڎ��������Ǥ�.<br>";
			my $href = &make_href("postform", $rowid, 0, $eid, 0);
			$data .="$nostr[0]<a href='$href'$akstr[0]>���</a>";
			&errorout;
			return;
		}
	}

	# ��Ƥ��줿ʸ�����Ⱦ��ʸ�������Ѥ��Ѵ�
	if ($jcd == 0) {
		&jcode::h2z_euc($post_from);
		&jcode::h2z_euc($post_mail);
		&jcode::h2z_euc($post_text);
	} else {
		Jcode->new(\$post_from,'euc')->h2z;
		Jcode->new(\$post_mail,'euc')->h2z;
		Jcode->new(\$post_text,'euc')->h2z;
	}

	# PublishCharset���Ѵ�
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
	
	# Ϣ³����ɻ�
	# ��ľ���Υ����Ȥ���Ӥ���Ʊ���ƤǤ����
	# ��Ϣ³��ƤȤߤʤ����顼�Ȥ��롣
	# �����դ���Ϣ³����ɻߤȤ������ϡ�
	# �������ॢ���ȸ�ʤɤ��Ժ�٤βἺ�ɻߡ���
	my @comments = get_comments($eid, 1, 'descend', 0);
	
	for my $tmp (@comments) {
		if ($post_from eq $tmp->author &&
			$post_mail eq $tmp->email &&
			$post_text eq $tmp->text) {
			$data .="Error!<br>Ʊ���ƤΎ��ҎݎĤ�������Ƥ���Ƥ��ޤ�<hr>";
			my $href = &make_href("comment", $rowid, 0, $eid, 0);
			$data .="$nostr[0]<a href='$href'$akstr[0]>��Ƥ��줿���ҎݎĤ��ǧ����</a>";
			&errorout;
			return;
		}
	}
	
	# Entry ID��Entry Title�μ���
	require MT::Entry;
	my $entry = MT::Entry->load($eid);

	# ������̤�0��ξ��ϥ�å�����ɽ������STOP��ͭ�����ʤ����ɤʡ�
	if ($entry <= 0) {
		$data = "Entry ID '$eid' �������Ǥ���";
		&errorout;
		exit;      # exit����
	}

	# DB����
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
	
	# MT3.0�ʾ�ʤ�visible������
	if ($mt->version_number() >= 3.0) {
		# $cfg{ApproveComment}='yes'�ξ��ˤϡ��񤭹��ߤ�Ʊ���˷Ǻܤ�������
		if ($cfg{ApproveComment} eq 'yes') {
			$comment->visible(1);
		} else {
			$comment->visible(0);
		}
	}
	
    $comment->save
        or die $comment->errstr;

	# �᡼������
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
								$entry->title . &conv_euc2utf8(' �ؤο����������� from MT4i')
                       );
            my $charset = $mt->{cfg}->PublishCharset || 'iso-8859-1';
            $head{'Content-Type'} = qq(text/plain; charset="$charset");
            my $body = &conv_euc2utf8('�����������Ȥ������֥� ') .
						$blog->name  . ' ' .
						&conv_euc2utf8('�Υ���ȥ꡼ #') . $entry->id . " (" .
						$entry->title . &conv_euc2utf8(') �ˤ���ޤ���');
			
			# �������ؤΥ�󥯺���
			my $link_url = $entry->permalink;
			
            use Text::Wrap;
            $Text::Wrap::cols = 72;
            $body = Text::Wrap::wrap('', '', $body) . "\n$link_url\n\n" .
            $body = $body . "\n$link_url\n\n" .
              &conv_euc2utf8('IP���ɥ쥹:') . ' ' . $comment->ip . "\n" .
              &conv_euc2utf8('̾��:') . ' ' . $comment->author . "\n" .
              &conv_euc2utf8('�᡼�륢�ɥ쥹:') . ' ' . $comment->email . "\n" .
              &conv_euc2utf8('URL:') . ' ' . $comment->url . "\n\n" .
              &conv_euc2utf8('������:') . "\n\n" . $comment->text . "\n\n" .
              &conv_euc2utf8("-- \nfrom MT4i v$version\n");
            MT::Mail->send(\%head, $body);
        }
    }

	####################
	# ��ӥ��
	
	# Index�ƥ�ץ졼��
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
	
	# Archive�ƥ�ץ졼��
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

	# ����ɽ��
	if ($mt->version_number() >= 3.0 && $cfg{ApproveComment} eq 'no') {
		$data = "���ҎݎĤ���Ƥ���ޤ��������Ǻܤ���α����Ƥ��ޤ���<br>�����ͤˤ�뾵���塢�Ǻܤ���ޤ���<hr>";
	} else {
		$data = "���ҎݎĤ���Ƥ���ޤ���<hr>";
	}
	my $href;
	if ($mode eq 'post') {
		$href = &make_href("comment", $rowid, 0, $eid, 0);
	} elsif ($mode eq 'post_rcm') {
		$href = &make_href("comment_rcm", $rowid, 0, $eid, 0);
	} elsif ($mode eq 'post_lnk') {
		$href = &make_href("comment_lnk", $rowid, 0, $eid, 0);
	}
	$data .="$nostr[0]<a href='$href'$akstr[0]>���</a>";
	&htmlout;
}

########################################
# Sub entryform - ����Entry/Entry�Խ� �ե�����
########################################
sub entryform {
	
	my ($org_title,$org_text,$org_text_more,$org_excerpt,$org_keywords,$org_convert_breaks,$org_created_on,$org_comment_cnt,$org_ent_status,$org_ent_allow_comments,$org_ent_allow_pings);
	my $rowid = $no;
	
	if ($eid == 0){
		$data = "<h4>����Entry�κ���</h4><hr>";
		
		# ���������μ���
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
		#$wday = sprintf("%s", ("��", "��", "��", "��", "��", "��", "��")[$wday]);
		$org_created_on = "$year-$mon-$mday $hour:$min:$sec";
	}else{
		
		$data = "<h4>Entry���Խ�</h4><hr>";
		
		# Entry����
		require MT::Entry;
		my $entry = MT::Entry->load($eid);
		
		# ������̤�0��ξ��ϥ�å�����ɽ������STOP��ͭ�����ʤ����ɤʡ�
		if (!$entry) {
			$data = "Entry ID '".$eid."' �������Ǥ���";
			&errorout;
			exit;      # exit����
		}
		
		# �Խ��ʤΤǡ����Υǡ���������
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
		
		# �����ȥ�򥨥󥳡���
		$org_title =~ s/&/&amp;/g;
		$org_title =~ s/ /&nbsp;/g;
		$org_title =~ s/\</&lt;/g;
		$org_title =~ s/\>/&gt;/g;
		# ��ʸ�򥨥󥳡���
		$org_text =~ s/&/&amp;/g;
		$org_text =~ s/ /&nbsp;/g;
		$org_text =~ s/\</&lt;/g;
		$org_text =~ s/\>/&gt;/g;
		# �ɵ��򥨥󥳡���
		$org_text_more =~ s/&/&amp;/g;
		$org_text_more =~ s/ /&nbsp;/g;
		$org_text_more =~ s/\</&lt;/g;
		$org_text_more =~ s/\>/&gt;/g;
		# ���פ򥨥󥳡���
		$org_excerpt =~ s/&/&amp;/g;
		$org_excerpt =~ s/ /&nbsp;/g;
		$org_excerpt =~ s/\</&lt;/g;
		$org_excerpt =~ s/\>/&gt;/g;
		# ������ɤ򥨥󥳡���
		$org_keywords =~ s/&/&amp;/g;
		$org_keywords =~ s/ /&nbsp;/g;
		$org_keywords =~ s/\</&lt;/g;
		$org_keywords =~ s/\>/&gt;/g;
	}
	
	####################
	# ɽ��ʸ��������
	my $href = &make_href("post", 0, 0, $eid, 0);
	$data .= "<form method=\"post\" action=\"$href\">";
	
	# ���ƥ��ꥻ�쥯��
	my $cat_label;
	if ($eid){
		$cat_label = &check_category(MT::Entry->load($eid));
	}
	$data .= "���Î��ގ�<br>";
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
	
	$data .= "�����Ď�";
	$data .= "<br><input type=\"text\" name=\"entry_title\" value=\"$org_title\"><br>";
	$data .= "Entry������";
	$data .= "<br><textarea rows=\"4\" name=\"entry_text\">$org_text</textarea><br>";
	$data .= "Extended(�ɵ�)";
	$data .= "<br><textarea rows=\"4\" name=\"entry_text_more\">$org_text_more</textarea><br>";
	$data .= "Excerpt(����)";
	$data .= "<br><textarea rows=\"4\" name=\"entry_excerpt\">$org_excerpt</textarea><br>";
	$data .= "�����܎��Ď�";
	$data .= "<br><textarea rows=\"4\" name=\"entry_keywords\">$org_keywords</textarea><br>";
	$data .= "��Ƥξ���<br>";
	$data .= "<select name=\"post_status\">";
	if (($eid && $org_ent_status == 1) || (!$eid && $blog->status_default == 1)) {
		$data .= "<option value=1 selected>����<br>";
		$data .= "<option value=2>����<br>";
		if ($mt->version_number() >= 3.1) {
			$data .= "<option value=3>������<br>";
		}
	} elsif (($eid && $org_ent_status == 2) || (!$eid && $blog->status_default == 2)) {
		$data .= "<option value=1>����<br>";
		$data .= "<option value=2 selected>����<br>";
		if ($mt->version_number() >= 3.1) {
			$data .= "<option value=3>������<br>";
		}
	} elsif (($eid && $org_ent_status == 3)) {
		$data .= "<option value=1>����<br>";
		$data .= "<option value=2>����<br>";
		if ($mt->version_number() >= 3.1) {
			$data .= "<option value=3 selected>������<br>";
		}
	} else {
		$data .= "<option value=1>����<br>";
		$data .= "<option value=2 selected>����<br>";
		if ($mt->version_number() >= 3.1) {
			$data .= "<option value=3>������<br>";
		}
	}
	$data .= "</select><br>";	
	
	$data .= "���Ҏݎ�<br>";
	$data .= "<select name=\"allow_comments\">";
	
	if (($eid && $org_ent_allow_comments == 0) || (!$eid && $blog->allow_comments_default == 0)) {
			$data .= "<option value=0 selected>�ʤ�<br>";
			$data .= "<option value=1>�����̎ߎ�<br>";
			$data .= "<option value=2>���ێ�����<br>";
	} elsif (($eid && $org_ent_allow_comments == 1) || (!$eid && $blog->allow_comments_default == 1)) {
			$data .= "<option value=0>�ʤ�<br>";
			$data .= "<option value=1 selected>�����̎ߎ�<br>";
			$data .= "<option value=2>���ێ�����<br>";
	} else {
			$data .= "<option value=0>�ʤ�<br>";
			$data .= "<option value=1>�����̎ߎ�<br>";
			$data .= "<option value=2 selected>���ێ�����<br>";
	}
	$data .= "</select><br>";
	
	$data .= "�Ď׎����ʎގ���������Ĥ���<br>";
	if (($eid && $org_ent_allow_pings) || (!$eid && $blog->allow_pings_default == 1)) {
		$data .= "<INPUT TYPE=checkbox name=\"allow_pings\" value=\"1\" CHECKED><br>";
	}else{
		$data .= "<INPUT TYPE=checkbox name=\"allow_pings\" value=\"1\"><br>";
	}
	
	## �ƥ����ȥե����ޥåȤΥ���
	my $filters = $mt->all_text_filters;
	my $text_filters = [];
	for my $filter (keys %$filters) {
		push @{ $text_filters }, {
			filter_key => $filter,
			filter_label => $filters->{$filter}{label},
		};
	}
	# ������
	$text_filters = [ sort { $a->{filter_key} cmp $b->{filter_key} } @{ $text_filters } ];
	# �֤ʤ��פ��ɲ�
	unshift @{ $text_filters }, {
		filter_key => '0',
		filter_label => '�ʤ�',
	};
	# ����
	$data .= "�Î����Ď̎����ώ���<br>";
	$data .= '<select name="convert_breaks">';
	foreach my $filter ( @{ $text_filters } ) {
		my $selected;
		if (($org_convert_breaks eq $filter->{filter_key}) || (!$org_convert_breaks && $convert_paras eq $filter->{filter_key})) {
			$selected = ' selected';
		}
		$data .= "<option value=\"$filter->{filter_key}\"$selected>$filter->{filter_label}</option>";
	}
	$data .= '</select><br>';
	
	$data .= "��������<br>";
	$data .= "<input type=\"text\" name=\"entry_created_on\" value=\"$org_created_on\"><br>";
	
	$data .= "<input type=\"hidden\" name=\"id\" value=\"$cfg{Blog_ID}\">";
	$data .= "<input type=\"hidden\" name=\"mode\" value=\"entry\">";
	$data .= "<input type=\"hidden\" name=\"no\" value=\"$rowid\">";
	$data .= "<input type=\"hidden\" name=\"eid\" value=\"$eid\">";
	if ($key){
		$data .= "<input type=\"hidden\" name=\"key\" value=\"$key\">";
	}
	$data .= "<input type=\"submit\" value=\"����\">";
	$data .= "</form>";
	$data .= "<hr>";
	$href = &make_href("", 0, 0, 0, 0);
	$data .= "$nostr[0]<a href='$href'$akstr[0]>���������</a>";
	&htmlout;
}

########################################
# Sub Entry - ����Entry���->ɽ������
########################################
sub entry {
	
	my $rowid = $no;
	$no--;
	
	# ������Ƥ��öEUC-JP���Ѵ�
	&$jcnv(\$entry_title, 'euc', 'sjis');
	&$jcnv(\$entry_text, 'euc', 'sjis');
	&$jcnv(\$entry_text_more, 'euc', 'sjis');
	&$jcnv(\$entry_excerpt, 'euc', 'sjis');
	&$jcnv(\$entry_keywords, 'euc', 'sjis');
	
	# Ⱦ�ѥ��ڡ���'&nbsp;'��ǥ�����
	$entry_title =~ s/&nbsp;/ /g;
	$entry_text =~ s/&nbsp;/ /g;
	$entry_text_more =~ s/&nbsp;/ /g;
	$entry_excerpt =~ s/&nbsp;/ /g;
	$entry_keywords =~ s/&nbsp;/ /g;

	####################
	# ɬ�����Ϲ��ܤ�����å�
	# �����ȥ롢�ƥ����ȤΤɤ��餫�����Ϥ�̵����Х��顼
	if((!$entry_title)||(!$entry_text))
	{
		$data .="Error!<br>̤���Ϲ��ܤ�����ޤ����֥����ȥ�פȡ�Entry�����ơפ�ɬ�ܤǤ���<br>";
		my $href = &make_href("entryform", 0, 0, $eid, 0);
		$data .="$nostr[0]<a href=\"$href\"$akstr[0]>���</a>";
		&errorout;
		return;
	}
	# �������������Ϥ�̵����Х��顼
	if (!$entry_created_on) {
		$data .="Error!<br>̤���Ϲ��ܤ�����ޤ����ֺ��������פ�ɬ�ܤǤ���<br>";
		my $href = &make_href("entryform", 0, 0, $eid, 0);
		$data .="$nostr[0]<a href=\"$href\"$akstr[0]>���</a>";
		&errorout;
		return;
	}
	require MT::Author;
	my $author = MT::Author->load({ name => $cfg{AuthorName} });	
	if (!$author) {
		$data = "\"$cfg{AuthorName}\"��Author�Ȥ�����Ͽ����Ƥ��ޤ���<br>";
		&errorout;
		exit;      # exit����
	}
	
	# ��Ƥ��줿ʸ�����Ⱦ�ѥ��ʤ����Ѥ��Ѵ�
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
	# PublishCharset���Ѵ�
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
		$data = "Entry�Ͻ�������ޤ���<hr>";
	}else{
		$data = "����Entry����������ޤ���<hr>";
	}
	
	# ��ӥ��
    $mt->rebuild_indexes( Blog => $blog )
        or die $mt->errstr;
    $mt->rebuild_entry( Entry => $entry )
        or die $mt->errstr;
	
	####################
	# ����ping����
	# status��publish�ξ��Τ�ping����
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
	$data .= "$nostr[0]<a href=\"$href\"$akstr[0]>���������</a>";
	&htmlout;
}

########################################
# Sub Entry_del - Entry���
########################################
sub entry_del {
	
	my $rowid = $no;
	$no--;
	
	require MT::Entry;
	my $entry = MT::Entry->load($eid);
	if (!$entry) {
		$data = "entry_del::Entry ID '".$eid."' �������Ǥ���";
		&errorout;
		exit;      # exit����
	}
	
	$entry->remove;
	
	# ��ӥ��
    $mt->rebuild_indexes( Blog => $blog )
        or die $mt->errstr;
    $mt->rebuild_entry( Entry => $entry )
        or die $mt->errstr;
	
	$data = "Entry���������ޤ���<hr>";
	my $href = &make_href("", 0, 0, 0, 0);
	$data .= "$nostr[0]<a href='$href'$akstr[0]>���������</a>";
	&htmlout;
}

########################################
# Sub Comment_del - �����Ⱥ��
########################################
sub comment_del {
	
	my $rowid = $no;
	$no--;
	
	####################
	# comment��õ��
	require MT::Comment;
	my $comment = MT::Comment->load($page);	# �������ֹ��$page���Ϥ�
	if (!$comment) {
		$data = "comment_del::Comment ID '".$page."' �������Ǥ���";
		&errorout;
		exit;      # exit����
	}
	$comment->remove()
		or die $comment->errstr;
	
	#����comment��°����Entry��õ��
	require MT::Entry;
	my $entry = MT::Entry->load($comment->entry_id);
	if (!$entry) {
		$data = "comment_del::Entry ID '".$comment->entry_id."' �������Ǥ���";
		&errorout;
		exit;      # exit����
	}
	
	# ��ӥ��
    $mt->rebuild_indexes( Blog => $blog )
        or die $mt->errstr;
    $mt->rebuild_entry( Entry => $entry )
        or die $mt->errstr;
	
	$data = "�����Ȥ��������ޤ���<hr>";
	my $href = &make_href("comment", $rowid, 0, $eid, 0);
	$data .= "$nostr[0]<a href=\'$href\'$akstr[0]>�����Ȱ��������</a>";
	&htmlout;
}

########################################
# Sub Trackback_del - �ȥ�å��Хå����
########################################
sub trackback_del {
	
	my $rowid = $no;
	$no--;
	
	####################
	# ping��õ��
	require MT::TBPing;
	my $tbping = MT::TBPing->load($page);	# �ȥ�å��Хå��ֹ��$page���Ϥ�
	if (!$tbping) {
		$data = "trackback_del::MTPing ID '".$page."' �������Ǥ���";
		&errorout;
		exit;      # exit����
	}
	$tbping->remove()
		or die $tbping->errstr;
	
	#����tbping��°����Trackback��õ��
	require MT::Trackback;
	my $trackback = MT::Trackback->load($tbping->tb_id);
	if (!$trackback) {
		$data = "trackback_del::Trackback ID '".$tbping->tb_id."' �������Ǥ���";
		&errorout;
		exit;      # exit����
	}
	
	#����Trackback��°����Entry��õ��
	require MT::Entry;
	my $entry = MT::Entry->load($trackback->entry_id);
	if (!$entry) {
		$data = "trackback_del::Entry ID '".$trackback->entry_id."' �������Ǥ���";
		&errorout;
		exit;      # exit����
	}
	
	# ��ӥ��
    $mt->rebuild_indexes( Blog => $blog )
        or die $mt->errstr;
    $mt->rebuild_entry( Entry => $entry )
        or die $mt->errstr;
	
	$data = "�Ď׎����ʎގ������������ޤ���<hr>";
	my $href = &make_href("trackback", $rowid, 0, $eid, 0);
	$data .= "$nostr[0]<a href=\'$href\'$akstr[0]>�Ď׎����ʎގ������������</a>";
	&htmlout;
}

########################################
# Sub Trackback_ipban - ����IP����Υȥ�å��Хå���ػߡ������
########################################
sub trackback_ipban {
	
	my $rowid = $no;
	$no--;
	
	####################
	# ping��õ��
	require MT::TBPing;
	my $tbping = MT::TBPing->load($page);	# �ȥ�å��Хå��ֹ��$page���Ϥ�
	if (!$tbping) {
		$data = "trackback_ipban::MTPing ID '".$page."' �������Ǥ���";
		&errorout;
		exit;      # exit����
	}
	
	require MT::IPBanList;
	my $ban = MT::IPBanList->new;
	$ban->blog_id($blog->id);
	$ban->ip($tbping->ip);
	$ban->save
		or die $ban->errstr;
	
	####################
	# ����IP�����������줿�ȥ�å��Хå�������õ��
	my @tbpings = MT::TBPing->load(
			{ blog_id => $cfg{Blog_ID}, ip => $tbping->ip});	
	
	for my $tbping (@tbpings) {
		
		#����tbping��°����Trackback��õ��
		require MT::Trackback;
		my $trackback = MT::Trackback->load($tbping->tb_id);
		if (!$trackback) {
			$data = "trackback_ipban::Trackback ID '".$tbping->tb_id."' �������Ǥ���";
			&errorout;
			exit;      # exit����
		}
		
		#����Trackback��°����Entry��õ��
		require MT::Entry;
		my $entry = MT::Entry->load($trackback->entry_id);
		if (!$entry) {
			$data = "trackback_ipban::Entry ID '".$trackback->entry_id."' �������Ǥ���";
			&errorout;
			exit;      # exit����
		}
		
		$data .= &conv_euc_z2h($tbping->excerpt)."<hr>";
		
		# �ȥ�å��Хå�ping���
		$tbping->remove()
			or die $tbping->errstr;

		# entry�Υ�ӥ��
		$mt->rebuild_entry( Entry => $entry )
			or die $mt->errstr;
	}
	
	$data = "IP��ػߥꥹ�Ȥ��ɲä���".@tbpings."��ΎĎ׎����ʎގ����������ޤ�����<hr>";
	my $href = &make_href("trackback", $rowid, 0, $eid ,0);
	$data .= "$nostr[0]<a href=\'$href\'$akstr[0]>�Ď׎����ʎގ������������</a>";
	&htmlout;
	
	# index�Υ�ӥ��
	$mt->rebuild_indexes( Blog => $blog )
		or die $mt->errstr;
}

########################################
# Sub Comment_ipban - ����IP����Υ����Ȥ�ػߡ������
########################################
sub comment_ipban {
	
	my $rowid = $no;
	$no--;
	
	####################
	# comment��õ��
	require MT::Comment;
	my $comment = MT::Comment->load($page);	# �������ֹ��$page���Ϥ�
	if (!$comment) {
		$data = "comment_ipban::Comment ID '".$page."' �������Ǥ���";
		&errorout;
		exit;      # exit����
	}
	
	require MT::IPBanList;
	my $ban = MT::IPBanList->new;
	$ban->blog_id($blog->id);
	$ban->ip($comment->ip);
	$ban->save
		or die $ban->errstr;
	
	####################
	# ����IP�����������줿�����Ȥ�����õ��
	my @comments = MT::Comment->load(
			{ blog_id => $cfg{Blog_ID}, ip => $comment->ip});
	
	for my $comment (@comments) {
		
		require MT::Entry;
		my $entry = MT::Entry->load($comment->entry_id);
		if (!$entry) {
			$data = "comment_ipban::Entry ID '".$comment->entry_id."' �������Ǥ���";
			&errorout;
			exit;      # exit����
		}
		
		# �����Ⱥ��
		$comment->remove()
			or die $comment->errstr;
		
		# entry�Υ�ӥ��
	    $mt->rebuild_entry( Entry => $entry )
	        or die $mt->errstr;
		
	}
	
	$data = "IP��ػߥꥹ�Ȥ��ɲä���".@comments."��Υ����Ȥ������ޤ�����<hr>";
	my $href = &make_href("comment", $rowid, 0, $eid, 0);
	$data .= "$nostr[0]<a href=\'$href\'$akstr[0]>�����Ȱ��������</a>";
	&htmlout;
	
	# index�Υ�ӥ��
	$mt->rebuild_indexes( Blog => $blog )
		or die $mt->errstr;
}

########################################
# Sub Email_comments - �����ȤΥ᡼����������
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
		$data = "�����ȤΥ᡼�����Τ���ߤ��ޤ�����<hr>";
	}else{
		$data = "�����ȤΥ᡼�����Τ�Ƴ����ޤ�����<hr>";
	}
	
	my $href = &make_href("", 0, $page, 0, 0);
	$data .= "$nostr[0]<a href=\"$href\"$akstr[0]>���������</a>";
	&htmlout;

}

########################################
# Sub Confirm - �Ƽ��ǧ
########################################
sub confirm {
	
	my $rowid = $no;
	
	# ������ID��$page�Ǽ����Ϥ�
	if ($mode eq "confirm_comment_del"){
		
		require MT::Comment;
		my $comment = MT::Comment->load($page);	# �������ֹ��$page���Ϥ�
		if (!$comment) {
			$data = "confirm_comment_del::Comment ID '".$page."' �������Ǥ���";
			&errorout;
			exit;      # exit����
		}
		$data .="�����˰ʲ��Υ����Ȥ������Ƥ�����Ǥ�����<br>";
		
		my $href = &make_href("comment", $rowid, $page , $eid, 0);
		$data .= "<a href='$href'>[����󥻥뤹��]</a><br>";
		$href = &make_href("comment_del", $rowid, $page, $eid, 0);
		$data .="<a href='$href'>[�������]</a><hr>";
		
		$data .= "Author:".&conv_euc_z2h($comment->author)."<br>";
		$data .= "Text:".&conv_euc_z2h($comment->text)."<br>";
		
	}
	elsif ($mode eq "confirm_entry_del"){

		require MT::Entry;
		my $entry = MT::Entry->load($eid);
		if (!$entry) {
			$data = "confirm_entry_del::Entry ID '".$eid."' �������Ǥ���";
			&errorout;
			exit;      # exit����
		}
		
		require MT::Author;
		my $author = MT::Author->load({ id => $entry->author_id });	
		my $author_name = "";
		if ($author) {
			$author_name = &conv_euc_z2h($author->name);
		}
		
		$data .="�����˰ʲ���Entry�������Ƥ�����Ǥ�����<br>";
		
		my $href = &make_href("individual", $rowid, 0 , $eid, 0);
		$data .= "<a href='$href'>[����󥻥뤹��]</a><br>";
		$href = &make_href("entry_del", $rowid, 0, $eid, 0);
		$data .="<a href='$href'>[�������]</a><hr>";
		
		if ($author_name){
			$data .= "Author:".$author_name."<br>";
		}
		$data .= "Text:".&conv_euc_z2h($entry->text)."<br>";
		
	}
	elsif ($mode eq "confirm_trackback_del"){
		
		require MT::TBPing;
		my $tbping = MT::TBPing->load($page);	# �ȥ�å��Хå��ֹ��$page���Ϥ�
		if (!$tbping) {
			$data = "confirm_trackback_del::MTPing ID '".$page."' �������Ǥ���";
			&errorout;
			exit;      # exit����
		}
		
		$data .="�����˰ʲ���TB�������Ƥ�����Ǥ�����<br>";
		my $href = &make_href("trackback", $rowid, $page , $eid, 0);
		$data .= "<a href='$href'>[����󥻥뤹��]</a><br>";
		$href = &make_href("trackback_del", $rowid, $page, $eid, 0);
		$data .="<a href='$href'>[�������]</a><hr>";
		
		$data .= "BlogName:".&conv_euc_z2h($tbping->blog_name)."<br>";
		$data .= "Title:".&conv_euc_z2h($tbping->title)."<br>";
		$data .= "Excerpt:".&conv_euc_z2h($tbping->excerpt)."<br>";
		
	}
	elsif ($mode eq "confirm_trackback_ipban"){
		
		require MT::TBPing;
		my $tbping = MT::TBPing->load($page);	# �ȥ�å��Хå��ֹ��$page���Ϥ�
		if (!$tbping) {
			$data = "confirm_trackback_ipban::MTPing ID '".$page."' �������Ǥ���";
			&errorout;
			exit;      # exit����
		}
		
		$data .="�����ˤ���IP���ɥ쥹(".$tbping->ip.")����ν񤭹��ߤ�ػߡ���������Ƥ�����Ǥ�����<br>";
		my $href = &make_href("trackback", $rowid, $page , $eid, 0);
		$data .= "<a href='$href'>[����󥻥뤹��]</a><br>";
		$href = &make_href("trackback_ipban", $rowid, $page, $eid, 0);
		$data .="<a href='$href'>[�ػߡ����������]</a><br>�������¿�����ϥ�ӥ�ɤ˻��֤������꥿���ॢ���Ȥ��뤳�Ȥ�����ޤ���������������˹Ԥ��ޤ���<hr>";
		$data .="\<�оݎĎ׎����ʎގ�������\><br>";
		
		####################
		# ����IP�����������줿�ȥ�å��Хå�������õ��
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
		my $comment = MT::Comment->load($page);	# �������ֹ��$page���Ϥ�
		if (!$comment) {
			$data = "confirm_comment_ipban::Comment ID '".$page."' �������Ǥ���";
			&errorout;
			exit;      # exit����
		}
		
		$data .="�����ˤ���IP���Ďގڎ�(".$comment->ip.")����ν񤭹��ߤ�ػߡ���������Ƥ�����Ǥ�����<br>";
		my $href = &make_href("comment", $rowid, $page , $eid, 0);
		$data .= "<a href='$href'>[�����ݎ��٤���]</a><br>";
		$href = &make_href("comment_ipban", $rowid, $page, $eid, 0);
		$data .="<a href='$href'>[�ػߡ����������]</a><br>�������¿�����ώ؎ˎގَĎޤ˻��֤�����������ю����Ĥ��뤳�Ȥ�����ޤ���������������˹Ԥ��ޤ���<hr>";
		$data .="\<�оݎ��Ҏݎİ���\><br>";
		
		####################
		# ����IP�����������줿�����Ȥ�����õ��
		my @comments = MT::Comment->load(
				{ blog_id => $cfg{Blog_ID}, ip => $comment->ip});
		
		for my $comment (@comments) {
			
			require MT::Entry;
			my $entry = MT::Entry->load($comment->entry_id);
			if (!$entry) {
				$data = "confirm_comment_ipban::Entry ID '".$comment->entry_id."' �������Ǥ���";
				&errorout;
				exit;      # exit����
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
		$data .="confirm::mode '".$mode."' �������Ǥ���<br>";
	}
	
	&htmlout;
}

########################################
# Sub Admindoor - ��������URL��ɽ��
########################################
sub admindoor {
	my $href;
	if ($pw_text eq $cfg{AdminPassword}){
		$data .= '��������URL��';
		$href = &make_href("", 0, 0, 0, 0);
		$href .= '&key='.&enc_crypt($cfg{AdminPassword}.$cfg{Blog_ID});
		$data .= "<a href=\"$href\">������</a>";
		$data .= '�Ǥ����؎ݎ����̎ގ����ώ��������塢®�䤫�ˡ�mt4i Manager�פˤ�"AdminDoor"���ͤ�"no"���ѹ����Ƥ���������<br>';
	}else{
		$data .= "�ʎߎ��܎��Ďޤ��㤤�ޤ�<hr>";
	}
	$key = "";
	$href = &make_href("", 0, 0, 0, 0);
	$data .= "$nostr[0]<a href='$href'$akstr[0]>���������</a>";
	&htmlout;
}

########################################
# Sub Separate - ñ��������������ʸ��ʬ��
########################################

sub separate {
	my $text = $_[0];
	my $rowid = $_[1];
	
	# ���ڤ�ʸ���������˳�Ǽ���Ƥ���
	my @sprtstrlist = split(",",$cfg{SprtStr});
	
	# ��ʸ�ΥХ��ȿ�����Ƥ���
	my $maxlen = &lenb_euc($text);
	
	# ����ʬ����֤��ᡢ$sprtbyte�س�Ǽ
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
			
			# ���ڤ�ʸ����θ���
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
			
			# ʬ����֤�$sprtbyte�˳�Ǽ
			if ($sprtstart < $maxlen) {
				$sprtbyte .= ",$sprtstart";
			}
			$i = $sprtstart + 1;
		}
	}
	
	# $sprtbyte���ɤ߼��
	my @argsprtbyte = split(/,/, $sprtbyte);
	my $sprtstart = $argsprtbyte[$sprtpage - 1];
	my $sprtend;
	if ($sprtpage - 1 < $#argsprtbyte) {
		$sprtend = $argsprtbyte[$sprtpage] - $sprtstart;
	} else {
		$sprtend = $maxlen - $sprtstart;
	}
	
	####################
	# ��ʸʸ��������
	
	my $tmptext = "";
	my $href = &make_href($mode, $rowid, 0, $eid, 0);
	
	# �ڡ�����󥯡ʾ��
	$tmptext .= "&lt; �͎ߎ����ް�ư:";
	for (my $i = 1; $i <= $#argsprtbyte + 1; $i++)  {
		if ($i == $sprtpage) {
			$tmptext .= " $i";
		} else {
			$tmptext .= " <a href=\"$href&amp;sprtpage=$i&amp;sprtbyte=$sprtbyte\">$i</a>";
		}
	}
	$tmptext .= " &gt;<br>";
	
	# ������ʸ
	$tmptext .= &midb_euc($text, $sprtstart, $sprtend);
	
	# �ڡ�����󥯡ʲ���
	$tmptext .= "<br>&lt; �͎ߎ����ް�ư:";
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
# Sub Conv_euc_z2h - ��EUC-JP�����Ѣ�Ⱦ���Ѵ�
########################################

sub conv_euc_z2h {
	my $tmpstr = $_[0];
	# ��������EUC-JP���Ѵ�
	if ($conv_in ne "euc") {
		if ($conv_in eq "utf8" && $ecd == 1) {
			$tmpstr = encode("cp932",decode("utf8",$tmpstr));
			$tmpstr = encode("euc-jp",decode("shiftjis",$tmpstr));
		} else {
			&$jcnv(\$tmpstr,'euc', $conv_in);
		}
	}
	
	# ɽ��ʸ���������ʸ����Ⱦ�Ѥ��Ѵ�
	if ($cfg{Z2H} eq "yes") {
		if ($jcd == 0) {
			&jcode::z2h_euc(\$tmpstr);
			&jcode::tr(\$tmpstr, '��-�ڣ�-����-���������ʡˡ��', 'A-Za-z0-9/!?()=&');
		} else {
			$tmpstr = Jcode->new($tmpstr,'euc')->z2h->tr('��-�ڣ�-����-���������ʡˡ��', 'A-Za-z0-9/!?()=&');
		}
	}
	return $tmpstr;
}

########################################
# Sub Img_Url_Conv - ����URL�Υ���å����%2F���Ѵ�
########################################

sub img_url_conv {
	my $tmpstr = $_[0];
	my $str = "";
	
	# �롼�פ��ʤ���<img>������URL���ִ�
	while ($tmpstr =~ /(<img(?:[^"'>]|"[^"]*"|'[^']*')*src=)("[^"]*"|'[^']*')((?:[^"'>]|"[^"]*"|'[^']*')*>)/i) {
		my $front = $` . $1;
		my $url = $2;
		my $end = $3 . $';
		
		# ���֥롦���󥰥륯�����ơ������������
		$url =~ s/"//g;
		$url =~ s/'//g;
		
		# "/"��"%2F"
		$url =~ s/\//\%2F/g;
		
		# ���֥륯�����ơ��������䤤�Ĥķ��
		$str .= "$front\"" . $url;
		$tmpstr = "\"$end";
	}
	$str .= $tmpstr;
	return $str;
}

### valium add start
#################################################################
# Sub Get_mt4ilink - MT4i�ؤΥ�󥯤����
#
# ������HTML���������MT4i�Ǳ�������Τ�Ŭ����������
# �������롣����Ū�ˤ� [rel|rev]="alternate" ��link�����Τ�����
# title="MT4i" ���뤤�� media="handheld" ��°�����ĥ����ǻ�
# �ꤵ��Ƥ��� href ���֤���ξ�����ä����� title="MT4i" ����
# ��ͥ�褹�븫�Ĥ���ʤ���ж�ʸ������֤���
#
#################################################################
sub get_mt4ilink {
  my $url = $_[0];

  require LWP::Simple;
  # ����襳��ƥ�ļ���
  my $content = LWP::Simple::get($url);
  if (!$content) {
    # ��������
    return "";
  }

  # �إå����μ��Ф�
  my $pattern = "<[\s\t]*?head[\s\t]*?>(.*?)<[\s\t]*?/[\s\t]*?head[\s\t]*?>";
  my @head = ($content =~ m/$pattern/is);
  if (!$head[0]) {
    return "";
  }

  # link�����μ��Ф�
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
# Sub Chtmltrans - ��󥯤�URL��chtmltrans��ͳ���Ѵ�
# ���͡�Perl��⢪http://www.din.or.jp/~ohzaki/perl.htm#HTML_Tag
########################################

sub chtmltrans {
	my $tmpstr = $_[0];
	my $ref_rowid = $_[1];
	my $ref_eid = $_[2];
	my $str = "";
	
	# �롼�פ��ʤ���URL���ִ�
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
		
		# title°������Ф�
		if ($tmpfront =~ /title=/i) {
			my $tmpstr = $tmpfront;
			$tmpstr =~ s/.*<a(?:[^"'>]|"[^"]*"|'[^']*')*title=("[^"]*"|'[^']*')(?:[^"'>]|"[^"]*"|'[^']*')*\Z/$1/i;
			# ���֥롦���󥰥륯�����ơ������������
			$tmpstr =~ s/"//g;
			$tmpstr =~ s/'//g;
			$title = $tmpstr;
		} elsif ($tmpend =~ /title=/i) {
			my $tmpstr = $tmpend;
			$tmpstr =~ s/\A.*(?:[^"'>]|"[^"]*"|'[^']*')*title=("[^"]*"|'[^']*')(?:[^"'>]|"[^"]*"|'[^']*')*>/$1/i;
			# ���֥롦���󥰥륯�����ơ������������
			$tmpstr =~ s/"//g;
			$tmpstr =~ s/'//g;
			$title = $tmpstr;
		}
		
		if ($title !~ /$cfg{ExitChtmlTrans}/) {
			if ($url =~ m/.*http:\/\/www.amazon.co.jp\/exec\/obidos\/ASIN\/.*/g) {
				# Amazon���̾��ʥ�󥯤ʤ�i-mode�б����Ѵ�
				$url =~ s/ASIN/dt\/i\/tg\/aa\/xml\/glance\/-/g;
				
				# ���֥롦���󥰥륯�����ơ������������
				$url =~ s/"//g;
				$url =~ s/'//g;
			} elsif ($url =~ m/.*http:\/\/www.amazlet.com\/browse\/ASIN\/.*/g) {
				# Amazlet�ؤΥ�󥯤ʤ顢Amazon��i-mode�б����Ѵ�
				$url =~ s/www.amazlet.com\/browse\/ASIN/www.amazon.co.jp\/exec\/obidos\/dt\/i\/tg\/aa\/xml\/glance\/-/g;
				
				# ���֥롦���󥰥륯�����ơ������������
				$url =~ s/"//g;
				$url =~ s/'//g;
			} elsif ($cfg{MyArcURL} && $url =~ m/.*$cfg{MyArcURL}.*/g && $mode eq 'individual' && (lc $cfg{Ainori}) eq 'no') {
				# ������������&�����Τ�OFF�ʤ�MT4i��ͳ���Ѵ�
				# �����������ܤ���䤳�����ʤä����ݤʤΤ�1���ؤΤ�
				$url =~ /$cfg{MyArcURL}/;
				my $eid = $1;
				$eid =~ s/^0+//;
				$url = &make_href("individual_lnk", $ref_rowid, 0, $eid, $ref_eid);
				
				# ���֥롦���󥰥륯�����ơ������������
				$url =~ s/"//g;
				$url =~ s/'//g;
			} else {
				### valium add start
				my $mt4ilink = "";
				if ((lc $cfg{Ainori}) eq 'yes') {
					# ���������
					$mt4ilink = &get_mt4ilink($url);
				}
				if ($mt4ilink) {
					$url = $mt4ilink;
					$lnkstr = $mt4ilinkstr;
				} else {
				### valium add end
					# ���֥롦���󥰥륯�����ơ������������
					$url =~ s/"//g;
					$url =~ s/'//g;
					
					# "/"��"@2F"��"?"��"@3F"��"+"��"@2B"
					$url =~ s/\//\@2F/g;
					$url =~ s/\?/\@3F/g;
					$url =~ s/\+/\@2B/g;
					
					# URL������
					my $chtmltransurl;
					$chtmltransurl .= 'http://wmlproxy.google.com/chtmltrans/h=ja/u=';
					$url = $chtmltransurl . $url . "/c=0";
				### valium add start
				}
				### valium add end
			}
		} else {
			# ���֥롦���󥰥륯�����ơ������������
			$url =~ s/"//g;
			$url =~ s/'//g;
			# �����б��ޡ���
			$lnkstr = $ExitChtmlTransStr;
		}
		# ���֥륯�����ơ��������䤤�Ĥķ��
		### valium modify start
		$str .= "$front\"" . $url;
		### valium modify end
		$tmpstr = "\"$end" . $lnkstr . $backward;
		
	}
	$str .= $tmpstr;

	# title��target°���κ���ʥХ��ȿ���̵�̡�
	$str =~ s/ target=["'][^"']*["']//ig;
	$str =~ s/ title=["'][^"']*["']//ig;
	
	return $str;
}
	
########################################
# Sub Lenb_EUC - Ⱦ�ѥ��ʡ�3�Х��ȴޤ�EUCʸ������length
# ���������Х��ȿ��������ʸ����
# \x8E[\xA1-\xDF] = EUCȾ�ѥ�������ɽ��
# \x8F[\xA1-\xFE][\xA1-\xFE] = EUC3�Х���ʸ������ɽ��
# ���͡�Perl��⢪http://www.din.or.jp/~ohzaki/perl.htm
########################################

sub lenb_euc {
	my $llen;
	$llen = length($_[0]);										# ���̤�length
	$llen -= $_[0]=~s/(\x8E[\xA1-\xDF])/$1/g;					# Ⱦ�ѥ��ʿ���ޥ��ʥ�
	$llen -= ($_[0]=~s/(\x8F[\xA1-\xFE][\xA1-\xFE])/$1/g)*2;	# 3�Х���ʸ����*2��ޥ��ʥ�
	$llen;
}

########################################
# Sub Midb_EUC - Ⱦ�ѥ��ʡ�3�Х��ȴޤ�EUCʸ������substr
# ���������ڤ�Ф�����ʸ����
# ����������ڤ�Ф����ϰ��֡�0����
# �軰�������ڤ�Ф��Х��ȿ�
# \x8E[\xA1-\xDF] = EUCȾ�ѥ�������ɽ��
# \x8F[\xA1-\xFE][\xA1-\xFE] = EUC3�Х���ʸ������ɽ��
# ���͡�Perl��⢪http://www.din.or.jp/~ohzaki/perl.htm
########################################

sub midb_euc {
	my $llen1;
	my $llen2;
	my $lstr;
	my $lstart;
	
	# �褺���������ϰ��֤���ʤ���
	if ($_[1] == 0) {
		$lstart = 0;
	} else {
		$llen1 = $_[1];
		$lstr = substr($_[0], 0, $llen1);
		$llen2 = lenb_euc($lstr);
		my $llen3 = $llen1;
		while ($_[1] > $llen2) {
			$llen3 = $llen1;
			$llen3 += $lstr=~s/(\x8E[\xA1-\xDF])/$1/g;					# Ⱦ�ѥ��ʿ���ץ饹
			$llen3 += ($lstr=~s/(\x8F[\xA1-\xFE][\xA1-\xFE])/$1/g)*2;	# 3�Х���ʸ����*2��ץ饹
			$lstr = substr($_[0], 0, $llen3);
			$llen2 = lenb_euc($lstr);
		}
		$llen1 = $llen3;
		
		# �ڤ�Ф���ʸ����κǸ夬Ⱦ�ѥ��ʤ�֤ä��ڤäƤʤ���Ƚ��
		if (substr($_[0], 0 + $llen1 - 1, 2)=~s/(\x8E[\xA1-\xDF])/$1/g) {
			# �֤ä��ڤäƤ���⤦1�Х�����򳫻ϰ��֤ˤ���
			$llen1++;
		}
		$lstart = $llen1;
	}
	
	# ʸ������ڤ�Ф�
	$llen1 = $_[2];
	$lstr = substr($_[0], $lstart, $llen1);
	$llen2 = lenb_euc($lstr);
	my $llen3;
	while ($_[2] > $llen2) {
		$llen3 = $llen1;
		$llen3 += $lstr=~s/(\x8E[\xA1-\xDF])/$1/g;					# Ⱦ�ѥ��ʿ���ץ饹
		$llen3 += ($lstr=~s/(\x8F[\xA1-\xFE][\xA1-\xFE])/$1/g)*2;	# 3�Х���ʸ����*2��ץ饹
		$lstr = substr($_[0], $lstart, $llen3);
		$llen2 = lenb_euc($lstr);
	}
	$llen1 = $llen3;
	
	# �ڤ�Ф���ʸ����κǸ夬Ⱦ�ѥ��ʤ�֤ä��ڤäƤʤ���Ƚ��
	if (substr($_[0], $lstart + $llen1 - 1, 2)=~s/(\x8E[\xA1-\xDF])/$1/g) {
		# �֤ä��ڤäƤ���⤦1�Х�����ޤ��ڤ�Ф�
		$lstr = substr($_[0], $lstart, $llen1 + 1);
	}
	return $lstr;
}

########################################
# Sub Htmlout - HTML�ν���
########################################

sub htmlout {
	# HTML�إå�/�եå����
	$data = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD Compact HTML 1.0 Draft//EN\"><html><head><meta name=\"CHTML\" HTTP-EQUIV=\"content-type\" CONTENT=\"text/html; charset=Shift_JIS\"><meta http-equiv=\"Pragma\" content=\"no-cache\"><meta http-equiv=\"Cache-Control\" content=\"no-cache\"><meta http-equiv=\"Cache-Control\" content=\"max-age=0\"><title>$blog_name mobile ver.</title></head><body bgcolor=\"$cfg{BgColor}\" text=\"$cfg{TxtColor}\" link=\"$cfg{LnkColor}\" alink=\"$cfg{AlnkColor}\" vlink=\"$cfg{VlnkColor}\">" . $data;
	if (exists $cfg{AdmNM}) {
		$data .= "<p><center>������:";
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
	
	# ɽ��ʸ�����Shift_JIS���Ѵ�
	&$jcnv(\$data,'sjis', "euc");
	
	# ɽ��
	binmode(STDOUT);
	print "Content-type: text/html; charset=Shift_JIS\n";
	print "Content-Length: ",length($data),"\n\n";
	print $data;
}

########################################
# Sub Errorout - ���顼�ν���
########################################

sub errorout {
	# HTML�إå�/�եå����
	$data = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD Compact HTML 1.0 Draft//EN\"><html><head><meta name=\"CHTML\" HTTP-EQUIV=\"content-type\" CONTENT=\"text/html; charset=Shift_JIS\"><title>Error</title></head><body>" . $data . "</body></html>";
	
	# ɽ��ʸ�����Shift_JIS���Ѵ�
	&$jcnv(\$data,'sjis', "euc");
	
	# ɽ��
	binmode(STDOUT);
	print "Content-type: text/html; charset=Shift_JIS\n";
	print "Content-Length: ",length($data),"\n\n";
	print $data;
}

##############################################################
# Sub conv_datetime - YYYYMMDDhhmmss�� MM/DD hh:mm ���Ѵ�
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
# calc_cashe_size:���ӤΥ���å���(1���̤˽��ϤǤ��������)�����
# ���� ���ӤΥ���å��奵����
# ���͡�http://deneb.jp/Perl/mobile/
# Special Thanks��drry
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
# crypt()�ˤ��Ź沽���ȹ�
# ���͡�http://www.rfs.co.jp/sitebuilder/perl/05/01.html#crypt
########################################

# �Ź沽������ʸ����($val)�������ꡢ�Ź沽����ʸ������֤��ؿ�
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

# �ѥ����($passwd1)�ȰŹ沽�����ѥ����($passwd2)�������ꡢ
# ���פ��뤫��Ƚ�ꤹ��ؿ�
sub check_crypt{
    my ($passwd1, $passwd2) = @_;

    $passwd2 =~ s/\@2F/\//g;
    $passwd2 =~ s/\@24/\$/g;
    $passwd2 =~ s/\@2E/\./g;
	
    # �Ź�Υ����å�
    if ( crypt($passwd1, $passwd2) eq $passwd2 ) {
        return 1;
    } else {
        return 0;
    }
}

############################################################
# Sub Check_Category - ����ȥ꡼�Υ��ƥ����Ĵ�٤�
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
# Sub Conv_Euc2utf8 - EUC-JP��UTF8�Ѵ�
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
