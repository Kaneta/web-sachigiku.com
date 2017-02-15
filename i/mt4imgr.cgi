#!/usr/bin/perl
##################################################
# 
# MT4i Manager - MT4i����ץ����
my $version = "2.0";
# 
##################################################

#---------- ���곫�� ----------
my $password = '1341i';
#---------- ���꽪λ ----------

use strict;
use CGI;

# Config.pl��require�ڤ�¸�߳�ǧ
eval {require 'mt4ilib/Config.pl'; 1} || die &errorout('"./mt4ilib/Config.pl"�����դ���ޤ���');

# �ѿ����
my %cfg;
my $mt4inm = 'mt4i.cgi';

####################
# �����μ���
my $q = new CGI();
my $mode = $q->param("mode");			# �����⡼��

####################
# ����$mode��Ƚ��
if (!$mode)				{ &login }
if ($mode eq 'edit')	{ &edit }
if ($mode eq 'vup')		{ &edit }
if ($mode eq 'save')	{ &save }

sub login {
	print "Content-type: text/html; charset=EUC-JP\n\n";
	print '<?xml version="1.0" encoding="EUC-JP"?>';
	print '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">';
	print '<html xmlns="http://www.w3.org/1999/xhtml" lang="ja" xml:lang="ja">';
	print '<head>';
	print '<meta http-equiv="Content-Type" content="text/html; charset=EUC-JP" />';
	print '<title>MT4i Manager</title>';
	print '<style type="text/css">';
	print 'body { background-color:#ffffcc; }';
	print 'h2 { background-color:#ccffcc;border:solid 2px;text-align:center; }';
	print 'div.input { margin-left:20px;margin-right:20px;margin-bottom:20px; }';
	print 'input { height:22px;margin-bottom:10px; }';
	print '</style>';
	print '</head>';
	print '<body>';
	print '<h2>MT4i Manager '.$version.'</h2>';
	print "<form action=\"./mt4imgr.cgi\" method=\"post\">";
	print '<div class="description">';
	print '�ѥ����';
	print '</div>';
	print '<div class="input">';
	print '<input type="password" name="password" />';
	print '<input type="submit" name="submit" value="������" />';
	print '</div>';
	print '<input type="hidden" name="mode" value="edit" />';
	print '</form>';
	print '</body>';
	print '</html>';
}

sub edit {
	print "Content-type: text/html; charset=EUC-JP\n\n";

	print '<?xml version="1.0" encoding="EUC-JP"?>';
	print '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">';
	print '<html xmlns="http://www.w3.org/1999/xhtml" lang="ja" xml:lang="ja">';
	print '<head>';
	print '<meta http-equiv="Content-Type" content="text/html; charset=EUC-JP" />';
	print '<title>MT4i Manager</title>';

	# �ѥ����ǧ��
	my $sendpass = $q->param("password");
	if ($sendpass ne $password) {
		print '</head>';
		print '<body>';
		print '�ѥ���ɤ��㤤�ޤ���<br />';
		print "<a href\"http://$ENV{'HTTP_HOST'}$ENV{\'SCRIPT_NAME'}\">���</a>";
		print "</body>";
		print "</html>";
		exit;
	}
	
	print '<style type="text/css">';
	print 'body { background-color:#ffffcc; }';
	print 'h2 { background-color:#ccffcc;border:solid 2px;text-align:center; }';
	print 'h3 { background-color:#ccffcc; }';
	print 'h4 { text-decoration:underline; }';
	print 'div.description { margin-left:10px;margin-right:10px;margin-bottom:10px; }';
	print 'div.input { margin-left:20px;margin-right:20px;margin-bottom:10px; }';
	print 'div.backlink { margin-left:30px;margin-right:10px;margin-bottom:20px; }';
	print 'input { height:22px;margin-bottom:10px; }';
	print 'select { height:22px;margin-bottom:10px; }';
	print '</style>';
	print '</head>';
	print '<body>';
	print '<h2 id="top">MT4i Manager '.$version.'</h2>';

	if ($mode eq "vup") {
		if ($q->param("mt4inm")) {
			$mt4inm = $q->param("mt4inm");
		}
		if (!-e $mt4inm) {
			print "\"$mt4inm\"�����դ���ޤ���<br>";
			print "MT4i���ΤΥե�����̾�����Ϥ��Ƥ���������<br>";
			print "<form action=\"./mt4imgr.cgi\" method=\"post\">";
			print "<input type=\"text\" name=\"mt4inm\" style=\"width:200px\"><br />";
			print "<input type=\"submit\" name=\"submit\" value=\"����\">";
			print "<input type=\"hidden\" name=\"mode\" value=\"vup\">";
			print "<input type=\"hidden\" name=\"password\" value=\"$password\">";
			print "</form>";
			print "</body>";
			print "</html>";
			exit;
		}
		# mt4i.cgi�����ץ�
		open(IN,"< $mt4inm") or die print "\"$mt4inm\"�����դ���ޤ���";
		
		my $rit_id_fl = 0;
		my $rat_id_fl = 0;
		while (<IN>){
			my $tmp = $_;
			chomp($tmp);
			
			if ($tmp =~ /^my/) {
				if ($tmp =~ /\(\$MT_DIR\)[^"']*["']([^"']*)["']/) {
					$cfg{'MT_DIR'} = enc_tag($1);
				} elsif ($tmp =~ /\$blog_id[^"']*["']([^"']*)["']/) {
					$cfg{'Blog_ID'} = enc_tag($1);
				} elsif ($tmp =~ /\$adm_nm[^"']*["']([^"']*)["']/) {
					$cfg{'AdmNM'} = enc_tag($1);
				} elsif ($tmp =~ /\$adm_ml[^"']*["']([^"']*)["']/) {
					$cfg{'AdmML'} = enc_tag($1);
				} elsif ($tmp =~ /\$logo_i[^"']*["']([^"']*)["']/) {
					$cfg{'Logo_i'} = enc_tag($1);
				} elsif ($tmp =~ /\$logo_o[^"']*["']([^"']*)["']/) {
					$cfg{'Logo_o'} = enc_tag($1);
				} elsif ($tmp =~ /\$dscrptn[^"']*["']([^"']*)["']/) {
					$cfg{'Dscrptn'} = enc_tag($1);
				} elsif ($tmp =~ /\$disp_num[^"']*["']([^"']*)["']/) {
					$cfg{'DispNum'} = enc_tag($1);
				} elsif ($tmp =~ /\$dt[^"']*["']([^"']*)["']/) {
					$cfg{'DT'} = enc_tag($1);
				} elsif ($tmp =~ /\$title_color[^"']*["']([^"']*)["']/) {
					$cfg{'TitleColor'} = enc_tag($1);
				} elsif ($tmp =~ /\$bg_color[^"']*["']([^"']*)["']/) {
					$cfg{'BgColor'} = enc_tag($1);
				} elsif ($tmp =~ /\$txt_color[^"']*["']([^"']*)["']/) {
					$cfg{'TxtColor'} = enc_tag($1);
				} elsif ($tmp =~ /\$lnk_color[^"']*["']([^"']*)["']/) {
					$cfg{'LnkColor'} = enc_tag($1);
				} elsif ($tmp =~ /\$alnk_color[^"']*["']([^"']*)["']/) {
					$cfg{'AlnkColor'} = enc_tag($1);
				} elsif ($tmp =~ /\$vlnk_color[^"']*["']([^"']*)["']/) {
					$cfg{'VlnkColor'} = enc_tag($1);
				} elsif ($tmp =~ /\$comment_color[^"']*["']([^"']*)["']/) {
					$cfg{'CommentColor'} = enc_tag($1);
				} elsif ($tmp =~ /\$trackback_color[^"']*["']([^"']*)["']/) {
					$cfg{'TbColor'} = enc_tag($1);
				} elsif ($tmp =~ /\$z2h[^"']*["']([^"']*)["']/) {
					$cfg{'Z2H'} = enc_tag($1);
				} elsif ($tmp =~ /\$bq2p[^"']*["']([^"']*)["']/) {
					$cfg{'BQ2P'} = enc_tag($1);
				} elsif ($tmp =~ /\$bqcolor[^"']*["']([^"']*)["']/) {
					$cfg{'BqColor'} = enc_tag($1);
				} elsif ($tmp =~ /\$sprtstr[^"']*["']([^"']*)["']/) {
					$cfg{'SprtStr'} = enc_tag($1);
					#$cfg{'SprtStr'} =~ s/&nbsp;/ /g;
				} elsif ($tmp =~ /\$sprtlimit[^"']*["']([^"']*)["']/) {
					$cfg{'SprtLimit'} = enc_tag($1);
				} elsif ($tmp =~ /\$myname[^"']*["']([^"']*)["']/) {
					$cfg{'MyName'} = enc_tag($1);
				} elsif ($tmp =~ /\$accesskey[^"']*["']([^"']*)["']/) {
					$cfg{'AccessKey'} = enc_tag($1);
				} elsif ($tmp =~ /\$image_autoreduce[^"']*["']([^"']*)["']/) {
					$cfg{'ImageAutoReduce'} = enc_tag($1);
				} elsif ($tmp =~ /\$photo_width[^"']*["']([^"']*)["']/) {
					$cfg{'PhotoWidth'} = enc_tag($1);
				} elsif ($tmp =~ /\$png_width[^"']*["']([^"']*)["']/) {
					$cfg{'PngWidth'} = enc_tag($1);
				} elsif ($tmp =~ /\$cat_desc_replace[^"']*["']([^"']*)["']/) {
					$cfg{'CatDescReplace'} = enc_tag($1);
				} elsif ($tmp =~ /\$cat_desc_sort[^"']*["']([^"']*)["']/) {
					$cfg{'CatDescSort'} = enc_tag($1);
				} elsif ($tmp =~ /\$post_from_essential[^"']*["']([^"']*)["']/) {
					$cfg{'PostFromEssential'} = enc_tag($1);
				} elsif ($tmp =~ /\$post_mail_essential[^"']*["']([^"']*)["']/) {
					$cfg{'PostMailEssential'} = enc_tag($1);
				} elsif ($tmp =~ /\$post_text_essential[^"']*["']([^"']*)["']/) {
					$cfg{'PostTextEssential'} = enc_tag($1);
				} elsif ($tmp =~ /\$recent_comment[^"']*["']([^"']*)["']/) {
					$cfg{'RecentComment'} = enc_tag($1);
				} elsif ($tmp =~ /\$recent_trackback[^"']*["']([^"']*)["']/) {
					$cfg{'RecentTB'} = enc_tag($1);
				} elsif ($tmp =~ /\$photo_host_original[^"']*["']([^"']*)["']/) {
					$cfg{'Photo_Host_Original'} = enc_tag($1);
				} elsif ($tmp =~ /\$photo_host_replace[^"']*["']([^"']*)["']/) {
					$cfg{'Photo_Host_Replace'} = enc_tag($1);
				} elsif ($tmp =~ /\$my_arc_url[^"']*["']([^"']*)["']/) {
					$cfg{'MyArcURL'} = enc_tag($1);
				} elsif ($tmp =~ /\$comment_notes[^"']*["']([^"']*)["']/) {
					$cfg{'CommentNotes'} = enc_tag($1);
				} elsif ($tmp =~ /\$exitchtmltrans[^"']*["']([^"']*)["']/) {
					$cfg{'ExitChtmlTrans'} = enc_tag($1);
				} elsif ($tmp =~ /\$ainori[^"']*["']([^"']*)["']/) {
					$cfg{'Ainori'} = enc_tag($1);
				} elsif ($tmp =~ /\@rbld_indx_tmpl_id/) {
					$rit_id_fl = 1;
					$cfg{'RIT_ID'} = '';
				} elsif ($tmp =~ /\@rbld_arc_tmpl_id/) {
					$rat_id_fl = 1;
					$cfg{'RAT_ID'} = '';
				} elsif ($tmp =~ /\$approve_comment[^"']*["']([^"']*)["']/) {
					$cfg{'ApproveComment'} = enc_tag($1);
				} elsif ($tmp =~ /\$admin_helper[^"']*["']([^"']*)["']/) {
					my @arg = split(/,/, $1);
					$cfg{'AdminHelper'} = 'yes';
					$cfg{'AdminHelperID'} = $arg[0];
					$cfg{'AdminHelperNM'} = $arg[1];
					$cfg{'AdminHelperML'} = $arg[2];
				} elsif ($tmp =~ /\$author_name[^"']*["']([^"']*)["']/) {
					$cfg{'AuthorName'} = enc_tag($1);
				} elsif ($tmp =~ /\$admin_door[^"']*["']([^"']*)["']/) {
					$cfg{'AdminDoor'} = enc_tag($1);
				} elsif ($tmp =~ /\$admin_password[^"']*["']([^"']*)["']/) {
					$cfg{'AdminPassword'} = enc_tag($1);
				}
			} elsif ($rit_id_fl == 1) {
				if ($tmp !~ /\);/) {
					$tmp =~ s/	//g;
					$tmp =~ s/ //g;
					$tmp =~ s/'//g;
					$cfg{'RIT_ID'} = $cfg{'RIT_ID'} . $tmp;
				} else {
					$rit_id_fl = 0;
					$cfg{'RIT_ID'} =~ s/,$//g;
				}
			} elsif ($rat_id_fl == 1) {
				if ($tmp !~ /\);/) {
					$tmp =~ s/	//g;
					$tmp =~ s/ //g;
					$tmp =~ s/'//g;
					$cfg{'RAT_ID'} = $cfg{'RAT_ID'} . $tmp;
				} else {
					$rat_id_fl = 0;
					$cfg{'RAT_ID'} =~ s/,$//g;
				}
			}
		}
		print '<p>';
		print '������ɤ߹��ߤޤ�����<br />';
		print '</p>';
	} elsif (-e 'mt4icfg.cgi') {
		# �����ɤ߹���
		%cfg = Config::Read("./mt4icfg.cgi");
	} else {
		print '<p>';
		print '����ե����뤬¸�ߤ��ޤ��󡣽���ͤ��������ޤ���<br />';
		print "��<a href=\"./mt4imgr.cgi?mode=vup&amp;password=$password\">v1.82��1������������ɤ߹��ࡣ</a>";
		print '</p>';
	}

	# �ǥե����������
	if ( !exists $cfg{'MT_DIR'} ) { $cfg{'MT_DIR'} = './'; }
	if ( !exists $cfg{'Blog_ID'} ) { $cfg{'Blog_ID'} = ''; }
	if ( !exists $cfg{'AdmNM'} ) { $cfg{'AdmNM'} = ''; }
	if ( !exists $cfg{'AdmML'} ) { $cfg{'AdmML'} = ''; }
	if ( !exists $cfg{'Logo_i'} ) { $cfg{'Logo_i'} = ''; }
	if ( !exists $cfg{'Logo_o'} ) { $cfg{'Logo_o'} = ''; }
	if ( !exists $cfg{'Dscrptn'} ) { $cfg{'Dscrptn'} = 'yes'; }
	if ( !exists $cfg{'DispNum'} ) { $cfg{'DispNum'} = 10; }
	if ( !exists $cfg{'DT'} ) { $cfg{'DT'} = 'dt'; }
	if ( !exists $cfg{'TitleColor'} ) { $cfg{'TitleColor'} = '#FF0000'; }
	if ( !exists $cfg{'BgColor'} ) { $cfg{'BgColor'} = '#FFFFFF'; }
	if ( !exists $cfg{'TxtColor'} ) { $cfg{'TxtColor'} = '#000000'; }
	if ( !exists $cfg{'LnkColor'} ) { $cfg{'LnkColor'} = '#0000FF'; }
	if ( !exists $cfg{'AlnkColor'} ) { $cfg{'AlnkColor'} = '#FF0000'; }
	if ( !exists $cfg{'VlnkColor'} ) { $cfg{'VlnkColor'} = '#800080'; }
	if ( !exists $cfg{'CommentColor'} ) { $cfg{'CommentColor'} = '#FF0000'; }
	if ( !exists $cfg{'TbColor'} ) { $cfg{'TbColor'} = '#00CC00'; }
	if ( !exists $cfg{'Z2H'} ) { $cfg{'Z2H'} = 'yes'; }
	if ( !exists $cfg{'BQ2P'} ) { $cfg{'BQ2P'} = 'no'; }
	if ( !exists $cfg{'BqColor'} ) { $cfg{'BqColor'} = '#008000'; }
	if ( !exists $cfg{'SprtStr'} ) { $cfg{'SprtStr'} = '<br />,<br>,</p>'; }
	if ( !exists $cfg{'SprtLimit'} ) { $cfg{'SprtLimit'} = 4096; }
	if ( !exists $cfg{'MyName'} ) { $cfg{'MyName'} = 'mt4i.cgi'; }
	if ( !exists $cfg{'AccessKey'} ) { $cfg{'AccessKey'} = 'yes'; }
	if ( !exists $cfg{'ImageAutoReduce'} ) { $cfg{'ImageAutoReduce'} = 'yes'; }
	if ( !exists $cfg{'PhotoWidth'} ) { $cfg{'PhotoWidth'} = 144; }
	if ( !exists $cfg{'PngWidth'} ) { $cfg{'PngWidth'} = 48; }
	if ( !exists $cfg{'CatDescReplace'} ) { $cfg{'CatDescReplace'} = 'no'; }
	if ( !exists $cfg{'CatDescSort'} ) { $cfg{'CatDescSort'} = 'none'; }
	if ( !exists $cfg{'PostFromEssential'} ) { $cfg{'PostFromEssential'} = 'yes'; }
	if ( !exists $cfg{'PostMailEssential'} ) { $cfg{'PostMailEssential'} = 'yes'; }
	if ( !exists $cfg{'PostTextEssential'} ) { $cfg{'PostTextEssential'} = 'yes'; }
	if ( !exists $cfg{'RecentComment'} ) { $cfg{'RecentComment'} = 15; }
	if ( !exists $cfg{'RecentTB'} ) { $cfg{'RecentTB'} = 10; }
	if ( !exists $cfg{'Photo_Host_Original'} ) { $cfg{'Photo_Host_Original'} = ''; }
	if ( !exists $cfg{'Photo_Host_Replace'} ) { $cfg{'Photo_Host_Replace'} = 'localhost'; }
	if ( !exists $cfg{'MyArcURL'} ) { $cfg{'MyArcURL'} = ''; }
	if ( !exists $cfg{'CommentNotes'} ) { $cfg{'CommentNotes'} = ''; }
	if ( !exists $cfg{'ExitChtmlTrans'} ) { $cfg{'ExitChtmlTrans'} = '�����б�'; }
	if ( !exists $cfg{'Ainori'} ) { $cfg{'Ainori'} = 'no'; }
	if ( !exists $cfg{'RIT_ID'} ) { $cfg{'RIT_ID'} = 'ALL'; }
	if ( !exists $cfg{'RAT_ID'} ) { $cfg{'RAT_ID'} = 'ALL'; }
	if ( !exists $cfg{'ApproveComment'} ) { $cfg{'ApproveComment'} = 'yes'; }
	if ( !exists $cfg{'AdminHelper'} ) { $cfg{'AdminHelper'} = 'no'; }
	if ( !exists $cfg{'AdminHelperID'} ) { $cfg{'AdminHelperID'} = ''; }
	if ( !exists $cfg{'AdminHelperNM'} ) { $cfg{'AdminHelperNM'} = ''; }
	if ( !exists $cfg{'AdminHelperML'} ) { $cfg{'AdminHelperML'} = ''; }
	if ( !exists $cfg{'AuthorName'} ) { $cfg{'AuthorName'} = ''; }
	if ( !exists $cfg{'AdminDoor'} ) { $cfg{'AdminDoor'} = 'no'; }
	if ( !exists $cfg{'AdminPassword'} ) { $cfg{'AdminPassword'} = 'password'; }
	if ( !exists $cfg{'IndividualCatLabelDisp'} ) { $cfg{'IndividualCatLabelDisp'} = 'no'; }
	if ( !exists $cfg{'IndividualAuthorDisp'} ) { $cfg{'IndividualAuthorDisp'} = 'no'; }

	#----------------------------------------------------------------------------------------------------
	print '<table><tr><td>';
	print '<ul>';
	print '	<li><span style="font-weight:bold;color:#FF0000;">ɬ���������</span>';
	print '	<ul>';
	print '		<li><a href="#MT_DIR">MT_DIR - MT�ۡ���ǥ��쥯�ȥ�</a></li>';
	print '		<li><a href="#Blog_ID">Blog_ID - Movable Type ��ǻ��Ѥ��Ƥ���Blog��ͭ��ID</a></li>';
	print '	</ul>';
	print '	</li>';
	print '</ul>';
	print '<ul>';
	print '	<li>�����ԥ⡼���������';
	print '	<ul>';
	print '		<li><a href="#AdminHelper">AdminHelper - ��������ƻ��δ����Ծ����������</a></li>';
	print '		<li><a href="#AuthorName">AuthorName - Entry��ƻ���Author��̾��</a></li>';
	print '		<li><a href="#AdminDoor">AdminDoor - �������ѥХå��ɥ���ɽ��</a></li>';
	print '		<li><a href="#AdminPassword">AdminPassword - ������URL�����ѥ����</a></li>';
	print '	</ul>';
	print '	</li>';
	print '</ul>';
	print '<ul>';
	print '	<li>ɽ����Ϣ�������';
	print '	<ul>';
	print '		<li><a href="#AdmNML">������̾��ɽ���ȥ᡼�륢�ɥ쥹</a></li>';
	print '		<li><a href="#Logo">�����ȥ�����������ꤹ��</a></li>';
	print '		<li><a href="#Dscrptn">Dscrptn - �ȥåפؤγ��פ�ɽ��</a></li>';
	print '		<li><a href="#DispNum">DispNum - �ȥåסʵ��������ˤ�ɽ�������뵭����</a></li>';
	print '		<li><a href="#DT">DT - �ȥåסʵ��������ˤǤ����������ɽ��</a></li>';
	print '		<li><a href="#Colors">��������</a></li>';
	print '		<li><a href="#CommentNotes">CommentNotes - ��������ƥե�������ս�</a></li>';
	print '		<li><a href="#IndividualCatLabelDisp">IndividualCatLabelDisp - ���̵������̤ǤΥ��ƥ���̾ɽ��</a></li>';
	print '		<li><a href="#IndividualAuthorDisp">IndividualAuthorDisp - ���̵������̤Ǥ�Author̾ɽ��</a></li>';
	print '	</ul>';
	print '	</li>';
	print '</ul>';
	print '</td><td>';
	print '<ul>';
	print '	<li>����¾Ǥ���������';
	print '	<ul>';
	print '		<li><a href="#Z2H">Z2H - ���Ѣ�Ⱦ���Ѵ�</a></li>';
	print '		<li><a href="#BQ2P">BQ2P - &lt;blockquote&gt;��&lt;p&gt;�Ѵ�</a></li>';
	print '		<li><a href="#SprtStr">SprtStr - ����ʬ����ζ��ڤ�ʸ����</a></li>';
	print '		<li><a href="#SprtLimit">SprtLimit - ������ʸ��ʬ��򤹤����¥Х��ȿ�</a></li>';
	print '		<li><a href="#MyName">MyName - MT4i���ΤΥե�����̾</a></li>';
	print '		<li><a href="#AccessKey">AccessKey - �������äγ�ʸ���ڤӥ�����������</a></li>';
	print '		<li><a href="#ImageAutoReduce">ImageAutoReduce - �����μ�ư�̾�</a></li>';
	print '		<li><a href="#PhotoWidth">PhotoWidth - �ǥե���Ȳ����β���</a></li>';
	print '		<li><a href="#PngWidth">PngWidth - vodafone�����굡��(6����)��PNG�����β���</a></li>';
	print '		<li><a href="#CatDescReplace">CatDescReplace - ���ƥ���̾��Description�ִ�</a></li>';
	print '		<li><a href="#CatDescSort">CatDescSort - ���ƥ���̾�Υ�����</a></li>';
	print '		<li><a href="#PostEssential">��������ƻ�����ɬ�ܹ��ܤλ���</a></li>';
	print '		<li><a href="#RecentComment">RecentComment - �Ƕ�Υ����Ȱ���ɽ�������ȿ�</a></li>';
	print '		<li><a href="#RecentTB">RecentTB - �Ƕ�Υȥ�å��Хå�ɽ����</a></li>';
	print '		<li><a href="#Photo_Host">Photo_Host_Original/Replace - ���𥵡��Фγ�/�����ۥ���̾</a></li>';
	print '		<li><a href="#MyArcURL">MyArcURL - ������������URL������ɽ��</a></li>';
	print '		<li><a href="#ExitChtmlTrans">ExitChtmlTrans - chtmltrans�Ѵ���̵����</a></li>';
	print '		<li><a href="#Ainori">Ainori - �����Τ굡ǽ</a></li>';
	print '		<li><a href="#RIAT_ID">��������ƻ���Rebuild�оݥƥ�ץ졼�Ȥ���ꤹ��</a></li>';
	print '		<li><a href="#ApproveComment">ApproveComment - �����ȷǺܤξ�����MT3.0�ʾ��ͭ����</a></li>';
	print '	</ul>';
	print '	</li>';
	print '</ul>';
	print '</td></tr></table>';
	#----------------------------------------------------------------------------------------------------

	print "<form action=\"./mt4imgr.cgi\" method=\"post\">";
	print '<input type="submit" name="submit" value="��¸" /><br />';

	#----------------------------------------------------------------------------------------------------
	print '<h3>ɬ���������</h3>';
	print '<h4 id="MT_DIR">MT_DIR - MT�ۡ���ǥ��쥯�ȥ�</h4>';
	print '<div class="description">';
	print 'Movable Type �򥤥󥹥ȡ��뤷���ǥ��쥯�ȥ��mt.cgi�Τ�����ˤ����Хѥ����뤤�����Хѥ��ǻ��ꡣ<br />��"http://��" �ǻϤޤ�URL�ǤϤʤ��פΤ���ա�<br />�ޤ�MT3.0�ʾ�Ǥϡ�MT�ۡ���ǥ��쥯�ȥ�ʳ��Υǥ��쥯�ȥ��MT4i�򥤥󥹥ȡ��뤷�����Хѥ��ˤ�MT�ۡ���ǥ��쥯�ȥ����ꤷ����硢������ǽ�������ư��ʤ����Ȥ��ǧ���Ƥ��ޤ���Plugin�ˤ��ɲä����ƥ����ȥե����ޥåȤ��ɥ�åץ�����ꥹ�Ȥ˸����ʤ��ʤɡˡ�<br />MT3.0�ʾ����Ѥ��Ƥ�����ϡ����Хѥ��ǻ��ꤷ�Ƥ���������<br />';
	print '</div>';
	print '<div class="input">';
	print '<input type="text" name="MT_DIR" value="' . $cfg{MT_DIR} . '" /><br />';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="Blog_ID">Blog_ID - Movable Type ��ǻ��Ѥ��Ƥ���Blog��ͭ��ID</h4>';
	print '<div class="description">';
	print 'Movable Type ���ָ塢�ǥե���ȤǺ��������Blog��ID�� "1"��<br />���θ塢Blog���ɲä������Ϣ�֤���Ϳ����롣<br />�����ǻ��ꤷ�ʤ��Ƥ⡢������������ݤ�URL�� "?id=" �Ȥ����Ϥ��Ƥ�äƤ��ɤ���<br />MT4i�ؤ�URL�� "http://your-domain/mt4i.cgi"��Blog��ID�� "1" �ʤ�С�<br />"http://your-domain/mt4i.cgi?id=1" �Ȥʤ롣<br />�ɤ�ʬ����ʤ����Ϥ����ǻ��ꤻ�������֡�������������Ȳ����ɽ������ΤǤ�����򻲾ȤΤ��ȡ�<br />';
	print '</div>';
	print '<div class="input">';
	print '<input type="text" name="Blog_ID" value="' . $cfg{Blog_ID} . '" /><br />';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	#----------------------------------------------------------------------------------------------------
	print '<h3>Ǥ���������</h3>';
	print '<h4 id="AdmNML">������̾��ɽ���ȥ᡼�륢�ɥ쥹</h4>';
	print '<div class="description">';
	print '�Ʋ��̲��˴�����̾��ɽ��������ˤϴ�����̾�����Ϥ��롣<br />';
	print '�������Ϥ���Ƥ��ʤ������ɽ����';
	print '</div>';
	print '<div class="input">';
	print '������̾�� <input type="text" name="AdmNM" value="' . $cfg{AdmNM} . '" /><br />';
	print '</div>';
	print '<div class="description">';
	print '�嵭������̾�ˡ�"mailto:��" �Υϥ��ѡ���󥯤�Ž����ˤϴ����ԥ᡼�륢�ɥ쥹�����Ϥ��롣<br />ɬ��Ū�˾嵭������̾�����꤬ɬ�ܡ�<br />�᡼�륢�ɥ쥹��ɽ������"@" �� "." �Τ߿���ʸ�����Ȥ��Ѵ���SPAM�᡼���к��ˡ�<br />';
	print '</div>';
	print '<div class="input">';
	print '�����ԥ᡼�륢�ɥ쥹�� <input type="text" name="AdmML" value="' . $cfg{AdmML} . '" style="width:200px;" /><br />';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="Logo">Logo - �����ȥ�������λ���</h4>';
	print '<div class="description">';
	print '�ȥåפ�ɽ�����륿���ȥ�����ɽ����������硢ɽ��������������URL�����ϡ����Хѥ��Ǥ�ġ�̤���Ϥʤ�ƥ����Ȥ�ɽ����i-mode�Ѥ�GIF��i-mode�ʳ��Ѥ�PNG��������ꤹ�뤳�ȡ�<br />';
	print '</div>';
	print '<div class="input">';
	print 'i-mode�ѡ� ';
	print '<input type="text" name="Logo_i" value="' . $cfg{Logo_i} . '" style="width:400px;" /><br />';
	print 'i-mode�ʳ��ѡ� ';
	print '<input type="text" name="Logo_o" value="' . $cfg{Logo_o} . '" style="width:400px;" /><br />';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="Dscrptn">Dscrptn - �ȥåפؤγ��פ�ɽ��</h4>';
	print '<div class="description">';
	print '�ֳ��ספȤϡ�Movable Type �ˤƳ�Blog����Ͽ����Ƥ��복�ס�Description�ˤΤ��ȡ�<br />ɽ��������ˤ� "yes"��ɽ�����ʤ����ˤ� "no" ������<br />';
	print '</div>';
	print '<div class="input">';
	print '<select name="Dscrptn">';
	if ($cfg{Dscrptn} eq 'yes') {
		print '<option value="yes" selected>yes</option>';
		print '<option value="no">no</option>';
	} else {
		print '<option value="yes">yes</option>';
		print '<option value="no" selected>no</option>';
	}
	print '</select>';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="DispNum">DispNum - �ȥåסʵ��������ˤ�ɽ�������뵭����</h4>';
	print '<div class="input">';
	print '<input type="text" name="DispNum" value="' . $cfg{DispNum} . '" /><br />';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="DT">DT - �ȥåסʵ��������ˤǤ����������ɽ��</h4>';
	print '<div class="input">';
	print '<select name="DT">';
	if ($cfg{DT} eq 'dt') {
		print '<option value="dt" selected>���� + ����</option>';
		print '<option value="d">���դΤ�</option>';
		print '<option value="no">ɽ�����ʤ�</option>';
	} elsif ($cfg{DT} eq 'd') {
		print '<option value="dt">���� + ����</option>';
		print '<option value="d" selected>���դΤ�</option>';
		print '<option value="no">ɽ�����ʤ�</option>';
	} else {
		print '<option value="dt">���� + ����</option>';
		print '<option value="d">���դΤ�</option>';
		print '<option value="no" selected>ɽ�����ʤ�</option>';
	}
	print '</select>';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="Colors">��������</h4>';
	print '<div class="input">';
	print '<table border="0">';
	print '<tr><td>';
	print '�ȥåץ����ȥ�ο���';
	print '</td><td>';
	print '<input type="text" name="TitleColor" value="' . $cfg{TitleColor} . '" /><br />';
	print '</td></tr><tr><td>';
	print '�طʿ�(bgcolor)��';
	print '</td><td>';
	print '<input type="text" name="BgColor" value="' . $cfg{BgColor} . '" /><br />';
	print '</td></tr><tr><td>';
	print '�ƥ����Ȥο�(text)��';
	print '</td><td>';
	print '<input type="text" name="TxtColor" value="' . $cfg{TxtColor} . '" /><br />';
	print '</td></tr><tr><td>';
	print '��󥯿�(link)��';
	print '</td><td>';
	print '<input type="text" name="LnkColor" value="' . $cfg{LnkColor} . '" /><br />';
	print '</td></tr><tr><td>';
	print '�����ƥ��֤ʥ�󥯿�(alink)��';
	print '</td><td>';
	print '<input type="text" name="AlnkColor" value="' . $cfg{AlnkColor} . '" /><br />';
	print '</td></tr><tr><td>';
	print '��ˬ��Υ�󥯿�(vlink)��';
	print '</td><td>';
	print '<input type="text" name="VlnkColor" value="' . $cfg{VlnkColor} . '" /><br />';
	print '</td></tr><tr><td>';
	print '����ɽ���������ȿ��ο���';
	print '</td><td>';
	print '<input type="text" name="CommentColor" value="' . $cfg{CommentColor} . '" />';
	print ' Entry�Υ����ȥ벣��ɽ������������"no"�������ɽ����';
	print '</td></tr><tr><td>';
	print '����ɽ�����ȥ�å��Хå����ο���';
	print '</td><td>';
	print '<input type="text" name="TbColor" value="' . $cfg{TbColor} . '" />';
	print ' Entry�Υ����ȥ벣��ɽ������������"no"�������ɽ����';
	print '</td></tr><tr><td>';
	print 'Entry��ʸ&lt;blockquote&gt;���ο��� ';
	print '</td><td>';
	print '<input type="text" name="BqColor" value="' . $cfg{BqColor} . '" />';
	print ' Movable Type ������ǡ�convert_breaks �� ON �ˤʤäƤ��뤳�Ȥ�����';
	print '</td></tr>';
	print '</table>';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="Z2H">Z2H - ���Ѣ�Ⱦ���Ѵ�</h4>';
	print '<div class="input">';
	print '<select name="Z2H">';
	if ($cfg{Z2H} eq 'yes') {
		print '<option value="yes" selected>����</option>';
		print '<option value="no">���ʤ�</option>';
	} else {
		print '<option value="yes">����</option>';
		print '<option value="no" selected>���ʤ�</option>';
	}
	print '</select>';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="BQ2P">BQ2P - &lt;blockquote&gt;��&lt;p&gt;�Ѵ�</h4>';
	print '<div class="description">';
	print 'Movable Type ������ǡ�convert_breaks �� ON �ˤʤäƤ��뤳�Ȥ�����';
	print '</div>';
	print '<div class="input">';
	print '<select name="BQ2P">';
	if ($cfg{BQ2P} eq 'yes') {
		print '<option value="yes" selected>����</option>';
		print '<option value="no">���ʤ�</option>';
	} else {
		print '<option value="yes">����</option>';
		print '<option value="no" selected>���ʤ�</option>';
	}
	print '</select>';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="SprtStr">SprtStr - ����ʬ����ζ��ڤ�ʸ����</h4>';
	print '<div class="description">';
	print '����ޤǶ��ڤä�ʣ���ѥ�������ꤹ�뤳�Ȥ��Ǥ��ޤ���<br />';
	print '1���ܤ˻��ꤷ��ʸ���󤬥ޥå����ʤ��ä���2���ܡ��Ƚ��֤˥ޥå��󥰤��ޤ���<br />';
	print '�㡧&lt;br /&gt;,&lt;br&gt;,&lt;/p&gt;';
	print '</div>';
	print '<div class="input">';
	print '<input type="text" name="SprtStr" value="' . $cfg{SprtStr} . '" /><br />';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="SprtLimit">SprtLimit - ������ʸ��ʬ��򤹤����¥Х��ȿ��ʥإå���եå����θ���뤳�ȡ�</h4>';
	print '<div class="input">';
	print '<input type="text" name="SprtLimit" value="' . $cfg{SprtLimit} . '" /><br />';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="">MyName - MT4i���ΤΥե�����̾��index.cgi�ʤɤ��ѹ����������ѡ�</h4>';
	print '<div class="input">';
	print '<input type="text" name="MyName" value="' . $cfg{MyName} . '" /><br />';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="AccessKey">AccessKey - �������äγ�ʸ���ڤӥ�����������</h4>';
	print '<div class="description">';
	print '�����ͭ���ˤ���ȡ��������ä��饢���������줿�ݡ���ưŪ�˵���������ɽ������뵭������6��ʲ���Ĵ������ޤ���<br />';
	print '</div>';
	print '<div class="input">';
	print '<select name="AccessKey">';
	if ($cfg{AccessKey} eq 'yes') {
		print '<option value="yes" selected>ͭ��</option>';
		print '<option value="no">̵��</option>';
	} else {
		print '<option value="yes">ͭ��</option>';
		print '<option value="no" selected>̵��</option>';
	}
	print '</select>';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="ImageAutoReduce">ImageAutoReduce - �����μ�ư�̾�</h4>';
	print '<div class="input">';
	print '<select name="ImageAutoReduce">';
	if ($cfg{ImageAutoReduce} eq 'yes') {
		print '<option value="yes" selected>����</option>';
		print '<option value="no">���ʤ�</option>';
	} else {
		print '<option value="yes">����</option>';
		print '<option value="no" selected>���ʤ�</option>';
	}
	print '</select>';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="PhotoWidth">PhotoWidth - �ǥե���Ȳ����β���</h4>';
	print '<div class="input">';
	print '<input type="text" name="PhotoWidth" value="' . $cfg{PhotoWidth} . '" /><br />';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="PngWidth">PngWidth - vodafone�����굡��(6����)��PNG�����β���</h4>';
	print '<div class="input">';
	print '<input type="text" name="PngWidth" value="' . $cfg{PngWidth} . '" /><br />';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="CatDescReplace">CatDescReplace - ���ƥ���̾��Description�ִ�</h4>';
	print '<div class="description">';
	print '���ƥ���̾�����ܸ첽��MTCategoryDescription�ǹԤäƤ��뤫��';
	print '</div>';
	print '<div class="input">';
	print '<select name="CatDescReplace">';
	if ($cfg{CatDescReplace} eq 'yes') {
		print '<option value="yes" selected>�ԤäƤ���</option>';
		print '<option value="no">�ԤäƤ��ʤ�</option>';
	} else {
		print '<option value="yes">�ԤäƤ���</option>';
		print '<option value="no" selected>�ԤäƤ��ʤ�</option>';
	}
	print '</select>';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="CatDescSort">CatDescSort - ���ƥ���̾�Υ�����</h4>';
	print '<div class="input">';
	print '<select name="CatDescSort">';
	if ($cfg{CatDescSort} eq 'none') {
		print '<option value="none" selected>���ʤ�</option>';
		print '<option value="asc">����</option>';
		print '<option value="desc">�߽�</option>';
	} elsif ($cfg{CatDescSort} eq 'asc') {
		print '<option value="none">���ʤ�</option>';
		print '<option value="asc" selected>����</option>';
		print '<option value="desc">�߽�</option>';
	} else {
		print '<option value="none">���ʤ�</option>';
		print '<option value="asc">����</option>';
		print '<option value="desc" selected>�߽�</option>';
	}
	print '</select>';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="PostEssential">��������ƻ�����ɬ�ܹ��ܤλ���</h4>';
	print '<div class="input">';
	print '<table border="0">';
	print '<tr><td>';
	print '��Ƽ�̾��';
	print '</td><td>';
	print '<select name="PostFromEssential">';
	if ($cfg{PostFromEssential} eq 'yes') {
		print '<option value="yes" selected>ɬ��</option>';
		print '<option value="no">��ά��</option>';
	} else {
		print '<option value="yes">ɬ��</option>';
		print '<option value="no" selected>��ά��</option>';
	}
	print '</select>';
	print '</td></tr><tr><td>';
	print '�᡼�륢�ɥ쥹��';
	print '</td><td>';
	print '<select name="PostMailEssential">';
	if ($cfg{PostMailEssential} eq 'yes') {
		print '<option value="yes" selected>ɬ��</option>';
		print '<option value="no">��ά��</option>';
	} else {
		print '<option value="yes">ɬ��</option>';
		print '<option value="no" selected>��ά��</option>';
	}
	print '</select>';
	print '</td></tr><tr><td>';
	print '��������ʸ��';
	print '</td><td>';
	print '<select name="PostTextEssential">';
	if ($cfg{PostTextEssential} eq 'yes') {
		print '<option value="yes" selected>ɬ��</option>';
		print '<option value="no">��ά��</option>';
	} else {
		print '<option value="yes">ɬ��</option>';
		print '<option value="no" selected>��ά��</option>';
	}
	print '</select>';
	print '</td></tr>';
	print '</table>';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="RecentComment">RecentComment - �Ƕ�Υ����Ȱ���ɽ�������ȿ�</h4>';
	print '<div class="input">';
	print '<input type="text" name="RecentComment" value="' . $cfg{RecentComment} . '" /><br />';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="RecentTB">RecentTB - �Ƕ�Υȥ�å��Хå�ɽ����</h4>';
	print '<div class="input">';
	print '<input type="text" name="RecentTB" value="' . $cfg{RecentTB} . '" /><br />';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="Photo_Host">Photo_Host_Original/Replace - ���𥵡��Фγ����������ۥ���̾</h4>';
	print '<div class="description">';
	print '���𥵡��б������ǲ����̾���ư���ʤ���硢\'Photo_Host_Original\'�˳����鸫����ۥ���̾�����ϡ�<br />';
	print '(������)\'www.hazama.nu\'�ξ�硢<br />';
	print 'http://www.hazama.nu/archive/test.jpg �� http://localhost/archive/test.jpg ���ִ�����뤳�Ȥǡ����ۥ��Ȥβ����ǡ������ɤ߹��ळ�Ȥ��Ǥ���褦�ˤʤ��礢�ꡣ<br />';
	print '\'Photo_Host_Original\'̤���Ϥǵ�ǽ���ա�<br />';
	print '</div>';
	print '<div class="input">';
	print '�����ۥ���̾: ';
	print '<input type="text" name="Photo_Host_Original" value="' . $cfg{Photo_Host_Original} . '" /><br />';
	print '�����ۥ���̾: ';
	print '<input type="text" name="Photo_Host_Replace" value="' . $cfg{Photo_Host_Replace} . '" /><br />';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="MyArcURL">MyArcURL - ������������URL������ɽ��</h4>';
	print '<div class="description">';
	print 'ʸ�����Ŭ�礹��URL�ؤΥ�󥯤�MT4i�θ��̵���URL���Ѵ����롣<br />';
	print '��������parmalink��EntryID���ޤޤ�Ƥ��뤳�Ȥ������<br />';
	print '̤���Ϥǵ�ǽ���ա�<br />';
	print '�ޤ��������Τ굡ǽ����Ǥⵡǽ���ա�<br />';
	print '�㡧http://yourdomain/archives/(\d\d\d\d\d\d).html<br />';
	print '</div>';
	print '<div class="input">';
	print '<input type="text" name="MyArcURL" value="' . $cfg{MyArcURL} . '" style="width:400px;" /><br />';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="CommentNotes">CommentNotes - ��������ƥե�������ս�</h4>';
	print '<div class="description">';
	print '���ꤵ�줿ʸ����򥳥�����ƥե�����κǾ�����ɽ�����롣<br />';
	print 'ɽ�����ʤ����ϲ������Ϥ��ʤ���<br />';
	print '��MTML�������Ѳġ����Ԥ���¸���˺������ޤ���<br />';
	print '</div>';
	print '<div class="input">';
	print '<textarea name="CommentNotes" rows="5" style="width:400px;">';
	print $cfg{CommentNotes};
	print '</textarea>';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="ExitChtmlTrans">ExitChtmlTrans - chtmltrans�Ѵ���̵����</h4>';
	print '<div class="description">';
	print 'A������TITLE°�������ꤷ��ʸ�����ޤ��硢chtmltrans�Ѵ����ʤ���<br />';
	print '</div>';
	print '<div class="input">';
	print '<input type="text" name="ExitChtmlTrans" value="' . $cfg{ExitChtmlTrans} . '" /><br />';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="Ainori">Ainori - �����Τ굡ǽ</h4>';
	print '<div class="input">';
	print '<select name="Ainori">';
	if ($cfg{Ainori} eq 'yes') {
		print '<option value="yes" selected>ON</option>';
		print '<option value="no">OFF</option>';
	} else {
		print '<option value="yes">ON</option>';
		print '<option value="no" selected>OFF</option>';
	}
	print '</select>';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="RIAT_ID">��������ƻ���Rebuild�оݥƥ�ץ졼�Ȥ���ꤹ��</h4>';
	print '<div class="description">';
	print '��������ƻ���Rebuild���оݤȤ���Index�ƥ�ץ졼�Ȥ�Templete ID����ꤹ�롣<br />';
	print 'Index�ƥ�ץ졼�Ȥ��٤Ƥ��оݤȤ���ʤ�"ALL"�Ȼ��ꤹ�롣<br />';
	print '��ID�ϥ���ޡ�,�ˤǶ��ڤ�������ڡ���������ʤ����ȡ�<br />';
	print '�㡧10,13,20<br />';
	print '</div>';
	print '<div class="input">';
	print 'Index�ƥ�ץ졼�ȡ�<input type="text" name="RIT_ID" value="' . $cfg{RIT_ID} . '" style="width:300px;" /><br />';
	print '</div>';
	print '<div class="description">';
	print '��������ƻ���Rebuild���оݤȤ���Archive�ƥ�ץ졼�Ȥ���ꤹ�롣<br />';
	print 'Archive�ƥ�ץ졼�Ȥ��٤Ƥ��оݤȤ���ʤ�"ALL"�Ȼ��ꤹ�롣';
	print '��ID�ϥ���ޡ�,�ˤǶ��ڤ�������ڡ���������ʤ����ȡ�<br />';
	print '�㡧Individual,Daily,Weekly,Monthly,Category<br />';
	print '</div>';
	print '<div class="input">';
	print 'Archive�ƥ�ץ졼�ȡ�<input type="text" name="RAT_ID" value="' . $cfg{RAT_ID} . '" style="width:300px;" /><br />';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="IndividualCatLabelDisp">IndividualCatLabelDisp - ���̵������̤ǤΥ��ƥ���̾ɽ��</h4>';
	print '<div class="description">';
	print '�����ȥ벣�ؤΥ��ƥ���̾ɽ����';
	print '</div>';
	print '<div class="input">';
	print '<select name="IndividualCatLabelDisp">';
	if ($cfg{IndividualCatLabelDisp} eq 'yes') {
		print '<option value="yes" selected>ɽ������</option>';
		print '<option value="no">ɽ�����ʤ�</option>';
	} else {
		print '<option value="yes">ɽ������</option>';
		print '<option value="no" selected>ɽ�����ʤ�</option>';
	}
	print '</select>';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="IndividualAuthorDisp">IndividualAuthorDisp - ���̵������̤Ǥ�Author̾ɽ��</h4>';
	print '<div class="description">';
	print '�����ȥ벣�ؤ�Author̾ɽ����<br />';
	print '�˥å��͡��ब���Ϥ���Ƥ���С��˥å��͡����ɽ�����롣<br />';
	print 'Author��ʣ��������ʤɤˡ�<br />';
	print '</div>';
	print '<div class="input">';
	print '<select name="IndividualAuthorDisp">';
	if ($cfg{IndividualAuthorDisp} eq 'yes') {
		print '<option value="yes" selected>ɽ������</option>';
		print '<option value="no">ɽ�����ʤ�</option>';
	} else {
		print '<option value="yes">ɽ������</option>';
		print '<option value="no" selected>ɽ�����ʤ�</option>';
	}
	print '</select>';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="ApproveComment">ApproveComment - �����ȷǺܤξ�����MT3.0�ʾ��ͭ����</h4>';
	print '<div class="input">';
	print '<select name="ApproveComment">';
	if ($cfg{ApproveComment} eq 'yes') {
		print '<option value="yes" selected>¨��������</option>';
		print '<option value="no">��ö��α����</option>';
	} else {
		print '<option value="yes">¨��������</option>';
		print '<option value="no" selected>��ö��α����</option>';
	}
	print '</select>';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	#----------------------------------------------------------------------------------------------------
	print '<h3>�����ԥ⡼���������</h3>';
	print '<h4 id="AdminHelper">AdminHelper - ��������ƻ��δ����Ծ������Ϥ�����</h4>';
	print '<div class="description">';
	print '̾���������ID������������ǡ�̾�����᡼�륢�ɥ쥹����ưŪ�˵�������롣<br />';
	print '�����ԥ⡼�ɤǤΤ�ͭ����<br />';
	print '</div>';
	print '<div class="input">';
	print '<table border="0">';
	print '<tr><td>';
	print 'AdminHelper����Ѥ���';
	print '</td><td>';
	print '<select name="AdminHelper">';
	if ($cfg{AdminHelper} eq 'yes') {
		print '<option value="yes" selected>�Ϥ�</option>';
		print '<option value="no">������</option>';
	} else {
		print '<option value="yes">�Ϥ�</option>';
		print '<option value="no" selected>������</option>';
	}
	print '</select>';
	print '</td></tr><tr><td>';
	print 'ID��';
	print '</td><td>';
	print '<input type="text" name="AdminHelperID" value="' . $cfg{AdminHelperID} . '" /><br />';
	print '</td></tr><tr><td>';
	print '̾����';
	print '</td><td>';
	print '<input type="text" name="AdminHelperNM" value="' . $cfg{AdminHelperNM} . '" /><br />';
	print '</td></tr><tr><td>';
	print '�᡼�륢�ɥ쥹��';
	print '</td><td>';
	print '<input type="text" name="AdminHelperML" value="' . $cfg{AdminHelperML} . '" style="width:200px;" /><br />';
	print '</td></tr>';
	print '</table>';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="AuthorName">AuthorName - Entry��ƻ���Author��̾��</h4>';
	print '<div class="description">';
	print 'MovableType����Ͽ�Ѥߤ�Author̾����ꤹ�롣<br />';
	print '</div>';
	print '<div class="input">';
	print '<input type="text" name="AuthorName" value="' . $cfg{AuthorName} . '" /><br />';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="AdminDoor">AdminDoor - �������ѥХå��ɥ���ɽ��</h4>';
	print '<div class="description">';
	print '���ư���ִ����Ը���URL�����ץ�󥯤�ɽ�����롣<br />';
	print '�����Ը���URL��֥å��ޡ����������ɬ�� "no" �����ꤹ�뤳�ȡ�<br />';
	print '</div>';
	print '<div class="input">';
	print '<select name="AdminDoor">';
	if ($cfg{AdminDoor} eq 'yes') {
		print '<option value="yes" selected>yes</option>';
		print '<option value="no">no</option>';
	} else {
		print '<option value="yes">yes</option>';
		print '<option value="no" selected>no</option>';
	}
	print '</select>';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	print '<h4 id="AdminPassword">AdminPassword - �ִ����Ը���URL�����פΰ٤Υѥ����</h4>';
	print '<div class="description">';
	print '�ѿ�����ɬ���ǥե���ȤΥѥ���ɤ����ѹ����뤳�ȡ�<br />';
	print '</div>';
	print '<div class="input">';
	print '<input type="text" name="AdminPassword" value="' . $cfg{AdminPassword} . '" /><br />';
	print '</div><div class="backlink"><a href="#top">�ڡ�����TOP�����</a></div>';

	#----------------------------------------------------------------------------------------------------
	print '<input type="submit" name="submit" value="��¸">';
	print '<input type="hidden" name="mode" value="save">';
	print "<input type=\"hidden\" name=\"password\" value=\"$password\">";
	print '</form>';

	print '</body>';
	print '</html>';
}

sub save {
	####################
	# �����μ���
	$cfg{'MT_DIR'} = del_rn($q->param('MT_DIR'));
	$cfg{'Blog_ID'} = del_rn($q->param('Blog_ID'));
	$cfg{'AdmNM'} = del_rn($q->param('AdmNM'));
	$cfg{'AdmML'} = del_rn($q->param('AdmML'));
	$cfg{'Logo_i'} = del_rn($q->param('Logo_i'));
	$cfg{'Logo_o'} = del_rn($q->param('Logo_o'));
	$cfg{'Dscrptn'} = del_rn($q->param('Dscrptn'));
	$cfg{'DispNum'} = del_rn($q->param('DispNum'));
	$cfg{'DT'} = del_rn($q->param('DT'));
	$cfg{'TitleColor'} = del_rn($q->param('TitleColor'));
	$cfg{'BgColor'} = del_rn($q->param('BgColor'));
	$cfg{'TxtColor'} = del_rn($q->param('TxtColor'));
	$cfg{'LnkColor'} = del_rn($q->param('LnkColor'));
	$cfg{'AlnkColor'} = del_rn($q->param('AlnkColor'));
	$cfg{'VlnkColor'} = del_rn($q->param('VlnkColor'));
	$cfg{'CommentColor'} = del_rn($q->param('CommentColor'));
	$cfg{'TbColor'} = del_rn($q->param('TbColor'));
	$cfg{'Z2H'} = del_rn($q->param('Z2H'));
	$cfg{'BQ2P'} = del_rn($q->param('BQ2P'));
	$cfg{'BqColor'} = del_rn($q->param('BqColor'));
	$cfg{'SprtStr'} = del_rn($q->param('SprtStr'));
	#$cfg{'SprtStr'} =~ s/ /&nbsp;/g;
	$cfg{'SprtLimit'} = del_rn($q->param('SprtLimit'));
	$cfg{'MyName'} = del_rn($q->param('MyName'));
	$cfg{'AccessKey'} = del_rn($q->param('AccessKey'));
	$cfg{'ImageAutoReduce'} = del_rn($q->param('ImageAutoReduce'));
	$cfg{'PhotoWidth'} = del_rn($q->param('PhotoWidth'));
	$cfg{'PngWidth'} = del_rn($q->param('PngWidth'));
	$cfg{'CatDescReplace'} = del_rn($q->param('CatDescReplace'));
	$cfg{'CatDescSort'} = del_rn($q->param('CatDescSort'));
	$cfg{'PostFromEssential'} = del_rn($q->param('PostFromEssential'));
	$cfg{'PostMailEssential'} = del_rn($q->param('PostMailEssential'));
	$cfg{'PostTextEssential'} = del_rn($q->param('PostTextEssential'));
	$cfg{'RecentComment'} = del_rn($q->param('RecentComment'));
	$cfg{'RecentTB'} = del_rn($q->param('RecentTB'));
	$cfg{'Photo_Host_Original'} = del_rn($q->param('Photo_Host_Original'));
	$cfg{'Photo_Host_Replace'} = del_rn($q->param('Photo_Host_Replace'));
	$cfg{'MyArcURL'} = del_rn($q->param('MyArcURL'));
	$cfg{'CommentNotes'} = del_rn($q->param('CommentNotes'));
	$cfg{'ExitChtmlTrans'} = del_rn($q->param('ExitChtmlTrans'));
	$cfg{'Ainori'} = del_rn($q->param('Ainori'));
	$cfg{'RIT_ID'} = del_rn($q->param('RIT_ID'));
	$cfg{'RAT_ID'} = del_rn($q->param('RAT_ID'));
	$cfg{'ApproveComment'} = del_rn($q->param('ApproveComment'));
	$cfg{'AdminHelper'} = del_rn($q->param('AdminHelper'));
	$cfg{'AdminHelperID'} = del_rn($q->param('AdminHelperID'));
	$cfg{'AdminHelperNM'} = del_rn($q->param('AdminHelperNM'));
	$cfg{'AdminHelperML'} = del_rn($q->param('AdminHelperML'));
	$cfg{'AuthorName'} = del_rn($q->param('AuthorName'));
	$cfg{'AdminDoor'} = del_rn($q->param('AdminDoor'));
	$cfg{'AdminPassword'} = del_rn($q->param('AdminPassword'));
	$cfg{'IndividualCatLabelDisp'} = del_rn($q->param('IndividualCatLabelDisp'));
	$cfg{'IndividualAuthorDisp'} = del_rn($q->param('IndividualAuthorDisp'));
	my $sendpass = $q->param('password');
	
	####################
	# �񤭹���
	my $cfg_file = "./mt4icfg.cgi";
	if (!-e $cfg_file) {
		open(OUT,"> $cfg_file") or die "Can't open		: $!";	# ̵����о�񤭥⡼�ɤǿ�������
	} else {
		open(OUT,"+< $cfg_file") or die "Can't open		: $!";	# ͭ����ɤ߽񤭥⡼�ɤǳ���
	}
	flock(OUT, 2) or die "Can't flock					: $!";	# ��å���ǧ����å�
	seek(OUT, 0, 0) or die "Can't seek					: $!";	# �ե�����ݥ��󥿤���Ƭ�˥��å�
	while ( my ( $key , $value ) = each %cfg ) {
		print OUT "$key<>$value\n" or die "Can't print	: $!";	# �񤭹���
	}
	truncate(OUT, tell(OUT)) or die "Can't truncate		: $!";	# �ե����륵������񤭹�����������ˤ���
	close(OUT);													# close����м�ư�ǥ�å����

	# ����
	print "Content-type: text/html; charset=EUC-JP\n\n";

	print '<?xml version="1.0" encoding="EUC-JP"?>';
	print '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">';
	print '<html xmlns="http://www.w3.org/1999/xhtml" lang="ja" xml:lang="ja">';
	print '<head>';
	print '<meta http-equiv="Content-Type" content="text/html; charset=EUC-JP" />';
	print '<title>MT4i Manager</title>';
	print '<style type="text/css">';
	print 'body { background-color:#ffffcc; }';
	print 'h2 { background-color:#ccffcc;border:solid 2px;text-align:center; }';
	print 'div.input { margin-left:20px;margin-right:20px;margin-bottom:20px; }';
	print 'input { height:22px;margin-bottom:10px; }';
	print '</style>';
	print '</head>';
	print '<body>';
	print '<h2>MT4i Manager '.$version.'</h2>';
	print '�������¸���ޤ�����';
	print "<form action=\"./mt4imgr.cgi\" method=\"post\">";
	print '<input type="submit" name="submit" value="���" />';
	print '<input type="hidden" name="password" value="' . $sendpass . '" />';
	print '<input type="hidden" name="mode" value="edit" />';
	print '</form>';
	print "</body>";
	print "</html>";
}

############################################################
# ���Ԥ���
############################################################
sub del_rn {
	my ($val) = @_;
	$val =~ s/\r//g;
	$val =~ s/\n//g;
	return $val;
}

############################################################
# '<'��'>'����λ��Ȥ��Ѵ�����
############################################################
sub enc_tag {
	my ($val) = @_;
	$val =~ s/</&lt;/g;
	$val =~ s/>/&gt;/g;
	return $val;
}

############################################################
# Error�ν���
############################################################
sub errorout {
	my ($val) = @_;
	print "Content-type: text/plain; charset=EUC-JP\n\nError!\n$val";
}