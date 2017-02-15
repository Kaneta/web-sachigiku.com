# Copyright 2001-2004 Six Apart. This code cannot be redistributed without
# permission from www.movabletype.org
#
# $Id: I18N.pm,v 1.25 2004/10/19 03:43:40 hirata Exp $   

package MT::I18N;

use strict;
use MT::ConfigMgr;
use Jcode;
use MT::Util qw(remove_html);

use vars qw ( %Charset );

my %Charset = (
   'shift_jis' => 'sjis', 
   'iso-2022-jp' => 'jis', 
   'euc-jp' => 'euc', 
   'utf-8' => 'utf8',
   'ascii' => 'utf8',
);
	    
sub guess_encoding {
    my ($text) = @_;
    my $enc = Jcode::getcode($text);
    if (!$enc) {
	$enc = MT::ConfigMgr->instance->PublishCharset || 'utf-8';
    }    
    if ($enc eq 'ascii') {
	$enc = 'utf-8';
    }
    if ($enc eq 'binary') {
	$enc = MT::ConfigMgr->instance->PublishCharset || 'utf-8';
    }    
    $enc = lc $enc;
    $enc = $Charset{$enc} ? $Charset{$enc} : $enc;
    return $enc;
}

sub encode_text {
    my ($text, $from, $to) = @_;
    if (!$from) {
        $from = guess_encoding($text);
    }
    if (!$to) {
	$to = MT::ConfigMgr->instance->PublishCharset || 'utf-8';
    }
    $from = lc $from;
    $from = $Charset{$from} ? $Charset{$from} : $from;
    $to = lc $to;
    $to = $Charset{$to} ? $Charset{$to} : $to;    
    return $text if ($from eq $to);
    return Jcode->new($text,$from)->$to();
}

sub substr_text {
    my ($text, $startpos, $length) = @_;
    if ($length == 0) {
        $length = -1;
    }
    my $enc = guess_encoding($text);
    my $euc_text = encode_text($text,$enc,'euc-jp');
    my $out = '';
    my $c = 0;
    for (my $i=0;$i<length($euc_text);$i++) {
        last if ($length == 0);
        if ( substr($euc_text,$i,2) =~ /[\xA1-\xFE][\xA1-\xFE]/ ||
             substr($euc_text,$i,2) =~ /[\x8E][\xA1-\xDF]/) {
            if ($c >= $startpos && ($length-->0 || $length < 0)) {
                $out .= substr($euc_text,$i,2);
            }
            $c++;$i++;
            next;
        }
        if ( substr($euc_text,$i,3) =~ /[\x8F][\xA1-\xFE][\xA1-\xFE]/) {
            if ($c >= $startpos && ($length-->0 || $length < 0)) {
                $out .= substr($euc_text,$i,3);
            }
            $c++;$i+=2;
            next;
        }
        if ( ord(substr($euc_text,$i,1)) < 0x80 ) {
            if ($c >= $startpos && ($length-->0 || $length < 0)) {
                $out .= substr($euc_text,$i,1);
            }
            $c++;
            next;
        }
    }
    return encode_text($out, 'euc-jp', $enc);
}

sub wrap_text {
    my ($text, $cols, $tab_init, $tab_sub) = @_;
    my $enc = guess_encoding($text);
    if (!$cols) {
	$cols = 72;
    }
    my $t = Jcode->new($text,$enc)->euc();
    $text = join "\n", Jcode->new($t)->jfold($cols);
    return encode_text($text,'euc-jp', $enc);
}

sub length_text {
    my ($text) = @_;
    my $enc = guess_encoding($text);
    my $euc_text= encode_text($text, $enc, 'euc-jp');
    my $len = Jcode->new($euc_text, 'euc')->jlength();
    return $len;
}

sub first_n_text {
    my ($text, $length) = @_;
    my $enc = guess_encoding($text);
    my $euc_text = Jcode->new($text,$enc)->euc();
    $euc_text = remove_html($euc_text);
    $euc_text =~ s/(\r?\n)+/ /g;
    my $out = substr_text($euc_text, 0, $length);
    return encode_text($out,'euc-jp', $enc);
}
