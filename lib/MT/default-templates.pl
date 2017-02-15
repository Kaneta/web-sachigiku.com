[
          {
            'outfile' => 'index.html',
            'text' => '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=<$MTPublishCharset$>" />
<meta name="generator" content="http://www.movabletype.org/" />

<title><$MTBlogName encode_html="1"$></title>

<link rel="stylesheet" href="<$MTBlogURL$>styles-site.css" type="text/css" />
<link rel="alternate" type="application/atom+xml" title="Atom" href="<$MTBlogURL$>atom.xml" />
<link rel="alternate" type="application/rss+xml" title="RSS 1.0" href="<$MTBlogURL$>index.rdf" />
<link rel="alternate" type="application/rss+xml" title="RSS 2.0" href="<$MTBlogURL$>index.xml" />
<link rel="EditURI" type="application/rsd+xml" title="RSD" href="<$MTBlogURL$>rsd.xml" />

<MTBlogIfCCLicense>
<$MTCCLicenseRDF$>
</MTBlogIfCCLicense>

</head>

<body>

<div id="container">

<div id="banner">
<h1><a href="<$MTBlogURL$>" accesskey="1"><$MTBlogName encode_html="1"$></a></h1>
<h2><$MTBlogDescription$></h2>
</div>

<div id="center">
<div class="content">

<MTEntries>
<$MTEntryTrackbackData$>

<MTDateHeader>
<h2><$MTEntryDate format="%x"$></h2>
</MTDateHeader>

<h3 id="a<$MTEntryID pad="1"$>"><$MTEntryTitle$></h3>

<$MTEntryBody$>

<MTEntryIfExtended>
<p class="extended"><a href="<$MTEntryPermalink$>#more"><MT_TRANS phrase="Continue reading"> "<$MTEntryTitle$>"</a></p>
</MTEntryIfExtended>

<p class="posted"><MT_TRANS phrase="Posted by"> <$MTEntryAuthor$> <MT_TRANS phrase="at"> <a href="<$MTEntryPermalink valid_html="1"$>"><$MTEntryDate format="%X"$></a>
<MTEntryIfAllowComments>
| <a href="<$MTEntryPermalink archive_type="Individual"$>#comments"><MT_TRANS phrase="Comments"> (<$MTEntryCommentCount$>)</a>
</MTEntryIfAllowComments>
<MTEntryIfAllowPings>
| <a href="<$MTEntryPermalink archive_type="Individual"$>#trackbacks"><MT_TRANS phrase="TrackBack"> (<$MTEntryTrackbackCount$>)</a>
</MTEntryIfAllowPings>
</p>

</MTEntries>

</div>
</div>

<div id="right">
<div class="sidebar">

<div id="calendar">

<table summary="<MT_TRANS phrase="Monthly calendar with links to each day\'s posts">">
<caption><$MTDate format="%B %Y"$></caption>
<tr>
<th abbr="<MT_TRANS phrase="Sunday">"><MT_TRANS phrase="Sun"></th>
<th abbr="<MT_TRANS phrase="Monday">"><MT_TRANS phrase="Mon"></th>
<th abbr="<MT_TRANS phrase="Tuesday">"><MT_TRANS phrase="Tue"></th>
<th abbr="<MT_TRANS phrase="Wednesday">"><MT_TRANS phrase="Wed"></th>
<th abbr="<MT_TRANS phrase="Thursday">"><MT_TRANS phrase="Thu"></th>
<th abbr="<MT_TRANS phrase="Friday">"><MT_TRANS phrase="Fri"></th>
<th abbr="<MT_TRANS phrase="Saturday">"><MT_TRANS phrase="Sat"></th>
</tr>

<MTCalendar>
<MTCalendarWeekHeader><tr></MTCalendarWeekHeader>

<td><MTCalendarIfEntries><MTEntries lastn="1"><a href="<$MTEntryPermalink$>"><$MTCalendarDay$></a></MTEntries></MTCalendarIfEntries><MTCalendarIfNoEntries><$MTCalendarDay$></MTCalendarIfNoEntries><MTCalendarIfBlank>&nbsp;</MTCalendarIfBlank></td><MTCalendarWeekFooter></tr></MTCalendarWeekFooter>
</MTCalendar>

</table>
</div>

<h2><MT_TRANS phrase="Search"></h2>
 
<div class="link-note">
<form method="get" action="<$MTCGIPath$><$MTSearchScript$>">
<input type="hidden" name="IncludeBlogs" value="<$MTBlogID$>" />
<label for="search" accesskey="4"><MT_TRANS phrase="Search this site:"></label><br />
<input id="search" name="search" size="20" /><br />
<input type="submit" value="<MT_TRANS phrase="Search">" />
</form>
</div>

<div id="categories">
<h2><MT_TRANS phrase="Categories"></h2>

<MTSubCategories>
<MTSubCatIsFirst><ul></MTSubCatIsFirst>
<MTIfNonZero tag="MTCategoryCount">
<li><a href="<$MTCategoryArchiveLink$>" title="<$MTCategoryDescription$>"><MTCategoryLabel></a>
<MTElse>
<li><MTCategoryLabel>
</MTElse>
</MTIfNonZero>
<MTSubCatsRecurse max_depth="3">
</li>
<MTSubCatIsLast></ul></MTSubCatIsLast>
</MTSubCategories>
</div>

<h2><MT_TRANS phrase="Archives"></h2>

<ul>
<MTArchiveList archive_type="Monthly">
<li><a href="<$MTArchiveLink$>"><$MTArchiveTitle$></a></li>
</MTArchiveList>
</ul>

<h2><MT_TRANS phrase="Recent Entries"></h2>

<ul>
<MTEntries lastn="10">
<li><a href="<$MTEntryPermalink$>"><$MTEntryTitle$></a></li>
</MTEntries>
</ul>

<div class="link-note">
<a href="<$MTBlogURL$>index.rdf"><MT_TRANS phrase="Syndicate this site"> (XML)</a>
</div>

<MTBlogIfCCLicense>
<div class="link-note">
<a href="<$MTBlogCCLicenseURL$>"><img alt="Creative Commons License" src="<$MTBlogCCLicenseImage$>" /></a><br />
<MT_TRANS phrase="This weblog is licensed under a"> <a href="<$MTBlogCCLicenseURL$>">Creative Commons License</a>.
</div>
</MTBlogIfCCLicense>

<div id="powered">
<MT_TRANS phrase="Powered by"><br /><a href="http://www.movabletype.jp">Movable Type <$MTVersion$></a><br />    
</div>

</div>
</div>

<div style="clear: both;">&#160;</div>

</div>

</body>
</html>
',
            'name' => 'Main Index',
            'type' => 'index',
            'rebuild_me' => '1'
          },
          {
              'outfile' => 'mtview.php',
              'text' => '<?php
    include(\'<$MTCGIServerPath$>/php/mt.php\');
    $mt = new MT(<$MTBlogID$>, \'<$MTCGIServerPath$>/mt.cfg\');
    $mt->view();
?>',
              'name' => 'Dynamic Site Bootstrapper',
              'type' => 'index',
              'rebuild_me' => 1,
          },
          {
            'outfile' => 'rsd.xml',
            'text' => '<?xml version="1.0"?> 
<rsd version="1.0" xmlns="http://archipelago.phrasewise.com/rsd">
<service>
<engineName>Movable Type <$MTVersion$></engineName> 
<engineLink>http://www.movabletype.org/</engineLink>
<homePageLink><$MTBlogURL$></homePageLink>
<apis>
<api name="MetaWeblog" preferred="true" apiLink="<$MTCGIPath$><$MTXMLRPCScript$>" blogID="<$MTBlogID$>" />
<api name="Blogger" preferred="false" apiLink="<$MTCGIPath$><$MTXMLRPCScript$>" blogID="<$MTBlogID$>" />
</apis>
</service>
</rsd>',
            'name' => 'RSD',
            'type' => 'index',
            'rebuild_me' => '1'
          },
          {
            'outfile' => 'atom.xml',
            'text' => '<?xml version="1.0" encoding="<$MTPublishCharset$>"?>
<feed version="0.3" xmlns="http://purl.org/atom/ns#" xmlns:dc="http://purl.org/dc/elements/1.1/" xml:lang="<$MTDefaultLanguage$>">
<title><$MTBlogName remove_html="1" encode_xml="1"$></title>
<link rel="alternate" type="text/html" href="<$MTBlogURL encode_xml="1"$>" />
<modified><MTEntries lastn="1"><$MTEntryModifiedDate utc="1" format="%Y-%m-%dT%H:%M:%SZ"$></MTEntries></modified>
<tagline><$MTBlogDescription remove_html="1" encode_xml="1"$></tagline>
<id>tag:<$MTBlogHost exclude_port="1" encode_xml="1"$>,<$MTDate format="%Y"$>:<$MTBlogRelativeURL encode_xml="1"$>/<$MTBlogID$></id>
<generator url="http://www.movabletype.org/" version="<$MTVersion$>">Movable Type</generator>
<copyright><MTEntries lastn="1">Copyright (c) <$MTEntryDate format="%Y"$>, <$MTEntryAuthor encode_xml="1"$></MTEntries></copyright>
<MTEntries lastn="15">
<entry>
<title><$MTEntryTitle remove_html="1" encode_xml="1"$></title>
<link rel="alternate" type="text/html" href="<$MTEntryPermalink encode_xml="1"$>" />
<modified><$MTEntryModifiedDate utc="1" format="%Y-%m-%dT%H:%M:%SZ"$></modified>
<issued><$MTEntryDate utc="1" format="%Y-%m-%dT%H:%M:%SZ"$></issued>
<id>tag:<$MTBlogHost exclude_port="1" encode_xml="1"$>,<$MTEntryDate format="%Y">:<$MTBlogRelativeURL encode_xml="1"$>/<$MTBlogID$>.<$MTEntryID$></id>
<created><$MTEntryDate utc="1" format="%Y-%m-%dT%H:%M:%SZ"$></created>
<summary type="text/plain"><$MTEntryExcerpt remove_html="1" encode_xml="1"$></summary>
<author>
<name><$MTEntryAuthor encode_xml="1"$></name>
<MTIfNonEmpty tag="MTEntryAuthorURL"><url><$MTEntryAuthorURL encode_xml="1"$></url></MTIfNonEmpty>
<MTIfNonEmpty tag="MTEntryAuthorEmail"><email><$MTEntryAuthorEmail encode_xml="1"$></email></MTIfNonEmpty>
</author>
<MTIfNonEmpty tag="MTEntryCategory"><dc:subject><$MTEntryCategory encode_xml="1"$></dc:subject></MTIfNonEmpty>
<content type="text/html" mode="escaped" xml:lang="<$MTDefaultLanguage$>" xml:base="<$MTBlogURL encode_xml="1"$>">
<$MTEntryBody encode_xml="1"$>
<$MTEntryMore encode_xml="1"$>
</content>
</entry>
</MTEntries>
</feed>',
            'name' => 'Atom Index',
            'type' => 'index',
            'rebuild_me' => '1'
          },
          {
            'outfile' => 'index.xml',
            'text' => '<?xml version="1.0" encoding="<$MTPublishCharset$>"?>
<rss version="2.0">
<channel>
<title><$MTBlogName remove_html="1" encode_xml="1"$></title>
<link><$MTBlogURL$></link>
<description><$MTBlogDescription remove_html="1" encode_xml="1"$></description>
<language><$MTDefaultLanguage$></language>
<copyright>Copyright <$MTDate format="%Y"$></copyright>
<lastBuildDate><MTEntries lastn="1"><$MTEntryDate format_name="rfc822"$></MTEntries></lastBuildDate>
<generator>http://www.movabletype.org/?v=<$MTVersion$></generator>
<docs>http://blogs.law.harvard.edu/tech/rss</docs> 

<MTEntries lastn="15">
<item>
<title><$MTEntryTitle remove_html="1" encode_xml="1"$></title>
<description><$MTEntryBody encode_xml="1"$></description>
<link><$MTEntryPermalink encode_xml="1"$></link>
<guid><$MTEntryPermalink encode_xml="1"$></guid>
<category><$MTEntryCategory remove_html="1" encode_xml="1"$></category>
<pubDate><$MTEntryDate format_name="rfc822"$></pubDate>
</item>
</MTEntries>

</channel>
</rss>',
            'name' => 'RSS 2.0 Index',
            'type' => 'index',
            'rebuild_me' => '1'
          },
          {
            'outfile' => 'archives.html',
            'text' => '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=<$MTPublishCharset$>" />
<meta name="generator" content="http://www.movabletype.org/" />
<title><$MTBlogName encode_html="1"$> Archives</title>

<link rel="stylesheet" href="<$MTBlogURL$>styles-site.css" type="text/css" />
<link rel="alternate" type="application/rss+xml" title="RSS" href="<$MTBlogURL$>index.rdf" />
<link rel="alternate" type="application/atom+xml" title="Atom" href="<$MTBlogURL$>atom.xml" />

</head>

<body>

<div id="container">

<div id="banner">
<h1><a href="<$MTBlogURL$>" accesskey="1"><$MTBlogName encode_html="1"$></a></h1>
<h2><$MTBlogDescription$></h2>
</div>

<div class="content">

<h2><MT_TRANS phrase="Archives"></h2>
<p>
<MTArchiveList>
<a href="<$MTArchiveLink$>"><$MTArchiveTitle$></a><br />
</MTArchiveList>
</p>

</div>
</div>

</body>
</html>',
            'name' => 'Master Archive Index',
            'type' => 'index',
            'rebuild_me' => '1'
          },
          {
            'text' => '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=<$MTPublishCharset$>" />
<meta name="generator" content="http://www.movabletype.org/" />

<title><$MTBlogName encode_html="1"$>: <MT_TRANS phrase="Comment Preview"></title>
<link rel="stylesheet" href="<$MTBlogURL$>styles-site.css" type="text/css" />

<MTInclude module="Remember Me">
</head>

<body>

<div id="container">

<div id="banner">
<h1><a href="<$MTBlogURL$>" accesskey="1"><$MTBlogName encode_html="1"$></a></h1>
<h2><$MTBlogDescription$></h2>
</div>

<div class="content">

<h2><MT_TRANS phrase="Previewing your Comment"></h2>

<$MTCommentPreviewBody$>
<p class="posted"><MT_TRANS phrase="Posted by"> <$MTCommentPreviewAuthorLink spam_protect="1"$> <MT_TRANS phrase="at"> <$MTCommentPreviewDate$></p>

<MTIfCommentsAllowed>

<MTCommentFields preview="1" static="1">

</MTIfCommentsAllowed>

<h2><MT_TRANS phrase="Previous Comments"></h2>

<MTComments>
<$MTCommentBody$>
<p class="posted"><MT_TRANS phrase="Posted by"> <$MTCommentAuthorLink default_name="Anonymous" spam_protect="1"$> <MT_TRANS phrase="at"> <$MTCommentDate$></p>
</MTComments>

</div>
</div>

</body>
</html>',
            'name' => 'Comment Preview Template',
            'type' => 'comment_preview',
            'rebuild_me' => '0'
          },
          {
            'text' => '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=<$MTPublishCharset$>" />
<meta name="generator" content="http://www.movabletype.org/" />

<title><$MTBlogName encode_html="1"$>: <MT_TRANS phrase="Thank You for Commenting"></title>
<link rel="stylesheet" href="<$MTBlogURL$>styles-site.css" type="text/css" />

<script language="JavaScript">
function getCookie (name) {
    var prefix = name + \'=\';
    var c = document.cookie;
    var nullstring = \'\';
    var cookieStartIndex = c.indexOf(prefix);
    if (cookieStartIndex == -1)
        return nullstring;
    var cookieEndIndex = c.indexOf(";", cookieStartIndex + prefix.length);
    if (cookieEndIndex == -1)
        cookieEndIndex = c.length;
    return unescape(c.substring(cookieStartIndex + prefix.length, cookieEndIndex));
}
</script>
</head>

<body>

<div id="container">

<div id="banner">
<h1><a href="<$MTBlogURL$>" accesskey="1"><$MTBlogName encode_html="1"$></a></h1>
<h2><$MTBlogDescription$></h2>
</div>

<div class="content">

<h2><MT_TRANS phrase="Thank You for Commenting"></h2>

<p><MT_TRANS phrase="Your comment has been received. To protect against malicious comments, I have enabled a feature that allows your comments to be held for approval the first time you post a comment. I\'ll approve your comment when convenient; there is no need to re-post your comment.">

<a href="<MTEntryLink>"><MT_TRANS phrase="Return to the comment page"></a></p>

</div>
</div>

</body>
</html>',
            'name' => 'Comment Pending Message',
            'type' => 'comment_pending',
            'rebuild_me' => '0'
          },
          {
            'text' => '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=<$MTPublishCharset$>" />
<meta name="generator" content="http://www.movabletype.org/" />

<title><$MTBlogName encode_html="1"$>: <MT_TRANS phrase="Comment Submission Error"></title>
<link rel="stylesheet" href="<$MTBlogURL$>styles-site.css" type="text/css" />

<MTInclude module="Remember Me">
</head>

<body>

<div id="container">

<div id="banner">
<h1><a href="<$MTBlogURL$>" accesskey="1"><$MTBlogName encode_html="1"$></a></h1>
<h2><$MTBlogDescription$></h2>
</div>

<div class="content">

<h2><MT_TRANS phrase="Comment Submission Error"></h2>

<p><MT_TRANS phrase="Your comment submission failed for the following reasons:"></p>

<blockquote><strong><$MTErrorMessage$></strong></blockquote>

<MTIfCommentsAllowed>

<MTCommentFields preview="1" static="1">

</MTIfCommentsAllowed>

</div>
</div>

</body>
</html>',
            'name' => 'Comment Error Template',
            'type' => 'comment_error',
            'rebuild_me' => '0'
          },
          {
            'text' => '<html>
<body topmargin="0" leftmargin="0" marginheight="0" marginwidth="0">

<img src="<$MTImageURL$>" width="<$MTImageWidth$>" height="<$MTImageHeight$>" />

</body>
</html>',
            'name' => 'Uploaded Image Popup Template',
            'type' => 'popup_image',
            'rebuild_me' => '0'
          },
          {
            'text' => '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=<$MTPublishCharset$>" />
<meta name="generator" content="http://www.movabletype.org/" />

<title><$MTBlogName encode_html="1"$>: <MT_TRANS phrase="Comment on"> <$MTEntryTitle$></title>

<link rel="stylesheet" href="<$MTBlogURL$>styles-site.css" type="text/css" />
<MTInclude module="Remember Me">
</head>

<body>

<div id="banner">
<h1><$MTBlogName encode_html="1"$></h1>
</div>

<div class="content">

<$MTErrorMessage$>

<h2><MT_TRANS phrase="Comments:"> <$MTEntryTitle$></h2>

<MTComments>
<$MTCommentBody$>
<p class="posted"><MT_TRANS phrase="Posted by"> <$MTCommentAuthorLink default_name="Anonymous" spam_protect="1"$> <MT_TRANS phrase="at"> <$MTCommentDate$></p>
</MTComments>

<MTEntryIfCommentsOpen>

<MTIfCommentsAllowed>

<h2><MT_TRANS phrase="Post a comment"></h2>

<MTCommentFields>

</MTIfCommentsAllowed>

</MTEntryIfCommentsOpen>

</div>

</body>
</html>',
            'name' => 'Comment Listing Template',
            'type' => 'comments',
            'rebuild_me' => '0'
          },
 {
     'text' => '<p>The requested page could not be found.</p>
<h4 class="error-message"><$MTErrorMessage$></h4>',
     'name' => 'Dynamic Pages Error Template',
     'type' => 'dynamic_error',
     'rebuild_me' => '0'
 },
          {
            'outfile' => 'index.rdf',
            'text' => '<?xml version="1.0" encoding="<$MTPublishCharset$>"?>

<rdf:RDF
xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
xmlns:dc="http://purl.org/dc/elements/1.1/"
xmlns:sy="http://purl.org/rss/1.0/modules/syndication/"
xmlns:admin="http://webns.net/mvcb/"
xmlns:cc="http://web.resource.org/cc/"
xmlns="http://purl.org/rss/1.0/">

<channel rdf:about="<$MTBlogURL$>">
<title><$MTBlogName encode_xml="1"$></title>
<link><$MTBlogURL$></link>
<description><$MTBlogDescription encode_xml="1"$></description>
<dc:language><$MTDefaultLanguage$></dc:language>
<dc:creator></dc:creator>
<dc:date><MTEntries lastn="1"><$MTEntryDate format="%Y-%m-%dT%H:%M:%S" language="en"$><$MTBlogTimezone$></MTEntries></dc:date>
<admin:generatorAgent rdf:resource="http://www.movabletype.org/?v=<$MTVersion$>" />
<MTBlogIfCCLicense>
<cc:license rdf:resource="<$MTBlogCCLicenseURL$>" />
</MTBlogIfCCLicense>

<items>
<rdf:Seq><MTEntries lastn="15">
<rdf:li rdf:resource="<$MTEntryPermalink encode_xml="1"$>" />
</MTEntries></rdf:Seq>
</items>

</channel>

<MTEntries lastn="15">
<item rdf:about="<$MTEntryPermalink encode_xml="1"$>">
<title><$MTEntryTitle encode_xml="1"$></title>
<link><$MTEntryPermalink encode_xml="1"$></link>
<description><$MTEntryBody encode_xml="1"$></description>
<dc:subject><$MTEntryCategory encode_xml="1"$></dc:subject>
<dc:creator><$MTEntryAuthor encode_xml="1"$></dc:creator>
<dc:date><$MTEntryDate format="%Y-%m-%dT%H:%M:%S" language="en"$><$MTBlogTimezone$></dc:date>
</item>
</MTEntries>

</rdf:RDF>',
            'name' => 'RSS 1.0 Index',
            'type' => 'index',
            'rebuild_me' => '1'
          },
          {
            'outfile' => 'styles-site.css',
            'text' => 'body {
	margin: 0px 0px 20px 0px;
		background-color: #8FABBE;
	
        	text-align: center;
        
	}

a {
	text-decoration: underline;
	
	
	}

a:link {
	color: #8FABBE;
	}

a:visited {
	color: #8FABBE;
	}

a:active {
	color: #8FABBE;
	}

a:hover {
	color: #006699;
	}

h1, h2, h3 {
	margin: 0px;
	padding: 0px;
	font-weight: normal;
	}

#container {
	line-height: 140%;
		margin-right: auto;
	margin-left: auto;
	text-align: left;
	padding: 0px;
	width: 700px;
	
	background-color: #FFFFFF;
	border: 1px solid #FFFFFF;
	}

#banner {
	font-family: Verdana, Arial, sans-serif;
	color: #FFFFFF;
	background-color: #999999;
	text-align: left;
	padding: 15px;
	border-bottom: 1px solid #FFFFFF;
	height: 39px;
	}

#banner-img {
	display: none;
	}


#banner a {
	color: #FFFFFF;
	text-decoration: none;
	}

#banner h1 {
	font-size: xx-large;
	
	
	
	}

#banner h2 {
	font-size: small;
	}

#center {
		float: left;
	width: 500px;
	
	
	overflow: hidden;
	}

.content {
	padding: 15px 15px 5px 15px;
	background-color: #FFFFFF;
	
	color: #666666;
	font-family: Verdana, Arial, sans-serif;
	font-size: x-small;
	}

#right {
		float: left;
	
	
	width: 200px;
	background-color: #FFFFFF;
	
	overflow: hidden;
	}

.content p {
	color: #666666;
	font-family: Verdana, Arial, sans-serif;
	font-size: x-small;
	font-weight: normal;
	line-height: 150%;
	text-align: left;
	margin-bottom: 10px;
	}

.content blockquote {
	line-height: 150%;
	}

.content li {
	line-height: 150%;
	}

.content h2 {
	color: #666666;
	font-family: Verdana, Arial, sans-serif;
	font-size: x-small;
	
	text-align: left;
	font-weight: bold;
	
	
	margin-bottom: 10px;
	
	}

.content h3 {
	color: #666666;
	font-family: Verdana, Arial, sans-serif;
	font-size: small;
	
	text-align: left;
	font-weight: bold;
	
	
	margin-bottom: 10px;
	
	}

.content p.posted {
	color: #999999;
	font-family: Verdana, Arial, sans-serif;
	font-size: x-small;
	border-top: 1px solid #999999;
	text-align: left;
	
	
	
	margin-bottom: 25px;
	line-height: normal;
	padding: 3px;
	}

.sidebar {
	padding: 15px;
	}



#calendar {
  	line-height: 140%;
	color: #666666;
	font-family: Verdana, Arial, sans-serif;
	font-size: x-small;
	
	
	
  	padding: 2px;
	text-align: center;
	margin-bottom: 30px;
	}

#calendar table {
	padding: 2px;
	border-collapse: collapse;
	border: 0px;
	width: 100%;
	}

#calendar caption {
	color: #666666;
	font-family: Verdana, Arial, sans-serif;
	font-size: x-small;
	
	text-align: center;
	font-weight: bold;
	
	text-transform: uppercase;
	
	letter-spacing: .3em;
	}

#calendar th {
	text-align: center;
	font-weight: normal;
	}

#calendar td {
	text-align: center;
	}

.sidebar h2 {
	color: #666666;
	font-family: Verdana, Arial, sans-serif;
	font-size: x-small;
	
	text-align: center;
	font-weight: bold;
	
	text-transform: uppercase;
  	
	letter-spacing: .3em;
	}

.sidebar ul {
	padding-left: 0px;
	margin: 0px;
	margin-bottom: 30px;
	}

.sidebar ul ul {
	margin-bottom: 0px;
	}

.sidebar #categories ul {
	padding-left: 15px;
	}

.sidebar li {
	color: #666666;
	font-family: Verdana, Arial, sans-serif;
	font-size: x-small;
	text-align: left;
	line-height: 150%;
	
	
	
	margin-top: 10px;
	list-style-type: none;
	}

.sidebar #categories li {
	list-style-type: circle;
	}

.sidebar img {
	border: 3px solid #FFFFFF;
	}

.photo {
	text-align: left;
	margin-bottom: 20px;
	}

.link-note {
	font-family: Verdana, Arial, sans-serif;
	font-size: x-small;
	line-height: 150%;
	text-align: left;
	padding: 2px;
	margin-bottom: 15px;
	}

#powered {
	font-family: Verdana, Arial, sans-serif;
	font-size: x-small;
	line-height: 150%;
	text-align: left;
	color: #666666;
	margin-top: 50px;
	}

#comment-data {
	float: left;
	width: 180px;
	padding-right: 15px;
	margin-right: 15px;
	text-align: left;
	border-right: 1px dotted #BBB;
	}

textarea[id="comment-text"] {
	width: 80%;
	}

.commenter-profile img {
	vertical-align: middle;
	border-width: 0;
	}
',
            'name' => 'Stylesheet',
            'type' => 'index',
            'rebuild_me' => '1'
          },
          {
            'text' => '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=<$MTPublishCharset$>" />
<meta name="generator" content="http://www.movabletype.org/" />

<title><$MTBlogName encode_html="1"$>: <$MTArchiveTitle$> <MT_TRANS phrase="Archives"></title>

<link rel="stylesheet" href="<$MTBlogURL$>styles-site.css" type="text/css" />
<link rel="alternate" type="application/rss+xml" title="RSS" href="<$MTBlogURL$>index.rdf" />
<link rel="alternate" type="application/atom+xml" title="Atom" href="<$MTBlogURL$>atom.xml" />
<link rel="start" href="<$MTBlogURL$>" title="Home" />
<MTArchivePrevious>
<link rel="prev" href="<$MTArchiveLink$>" title="<$MTArchiveTitle encode_html="1"$>" />
</MTArchivePrevious>
<MTArchiveNext>
<link rel="next" href="<$MTArchiveLink$>" title="<$MTArchiveTitle encode_html="1"$>" />
</MTArchiveNext>

</head>

<body>

<div id="container">

<div id="banner">
<h1><a href="<$MTBlogURL$>" accesskey="1"><$MTBlogName encode_html="1"$></a></h1>
<h2><$MTBlogDescription$></h2>
</div>

<div class="content">

<p align="right">
<MTArchivePrevious>
<a href="<$MTArchiveLink$>">&laquo; <$MTArchiveTitle$></a> |
</MTArchivePrevious>
<a href="<$MTBlogURL$>"><MT_TRANS phrase="Main"></a>
<MTArchiveNext>
| <a href="<$MTArchiveLink$>"><$MTArchiveTitle$> &raquo;</a>
</MTArchiveNext>
</p>

<MTEntries>
<$MTEntryTrackbackData$>

<MTDateHeader>
<h2><$MTEntryDate format="%x"$></h2>
</MTDateHeader>

<h3 id="a<$MTEntryID pad="1"$>"><$MTEntryTitle$></h3>

<$MTEntryBody$>

<MTEntryIfExtended>
<$MTEntryMore$>
</MTEntryIfExtended>

<p class="posted">
<MT_TRANS phrase="Posted by"> <$MTEntryAuthor$> <MT_TRANS phrase="at"> <a href="<$MTEntryPermalink valid_html="1"$>"><$MTEntryDate format="%X"$></a>
<MTEntryIfAllowComments>
| <a href="<$MTEntryPermalink archive_type="Individual"$>#comments"><MT_TRANS phrase="Comments"> (<$MTEntryCommentCount$>)</a>
</MTEntryIfAllowComments>
<MTEntryIfAllowPings>
| <a href="<$MTEntryPermalink archive_type="Individual"$>#trackbacks"><MT_TRANS phrase="TrackBack"></a>
</MTEntryIfAllowPings>
</p>

</MTEntries>

</div>
</div>

</body>
</html>
',
            'name' => 'Date-Based Archive',
            'type' => 'archive',
            'rebuild_me' => '0'
          },
          {
            'text' => '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=<$MTPublishCharset$>" />
<meta name="generator" content="http://www.movabletype.org/" />

<title><$MTBlogName encode_html="1"$>: <$MTArchiveTitle$> <MT_TRANS phrase="Archives"></title>

<link rel="stylesheet" href="<$MTBlogURL$>styles-site.css" type="text/css" />
<link rel="alternate" type="application/rss+xml" title="RSS" href="<$MTBlogURL$>index.rdf" />
<link rel="alternate" type="application/atom+xml" title="Atom" href="<$MTBlogURL$>atom.xml" />
</head>

<body>

<div id="container">

<div id="banner">
<h1><a href="<$MTBlogURL$>" accesskey="1"><$MTBlogName encode_html="1"$></a></h1>
<h2><$MTBlogDescription$></h2>
</div>

<div class="content">
<MTEntries>
<$MTEntryTrackbackData$>

<MTDateHeader>
<h2><$MTEntryDate format="%x"$></h2>
</MTDateHeader>

<h3 id="a<$MTEntryID pad="1"$>"><$MTEntryTitle$></h3>

<$MTEntryBody$>

<MTEntryIfExtended>
<$MTEntryMore$>
</MTEntryIfExtended>

<p class="posted">
<MT_TRANS phrase="Posted by"> <$MTEntryAuthor$> <MT_TRANS phrase="at"> <a href="<$MTEntryPermalink valid_html="1"$>"><$MTEntryDate format="%X"$></a>
<MTEntryIfAllowComments>
| <a href="<$MTEntryPermalink archive_type="Individual"$>#comments"><MT_TRANS phrase="Comments"> (<$MTEntryCommentCount$>)</a>
</MTEntryIfAllowComments>
<MTEntryIfAllowPings>
| <a href="<$MTEntryPermalink archive_type="Individual"$>#trackbacks"><MT_TRANS phrase="TrackBack"></a>
</MTEntryIfAllowPings>
</p>

</MTEntries>

</div>
</div>

</body>
</html>
',
            'name' => 'Category Archive',
            'type' => 'category',
            'rebuild_me' => '0'
          },
          {
            'text' => '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=<$MTPublishCharset$>" />
<meta name="generator" content="http://www.movabletype.org/" />

<title><$MTBlogName encode_html="1"$>: <$MTEntryTitle$></title>

<link rel="stylesheet" href="<$MTBlogURL$>styles-site.css" type="text/css" />
<link rel="alternate" type="application/rss+xml" title="RSS" href="<$MTBlogURL$>index.rdf" />
<link rel="alternate" type="application/atom+xml" title="Atom" href="<$MTBlogURL$>atom.xml" />

<link rel="start" href="<$MTBlogURL$>" title="Home" />
<MTEntryPrevious>
<link rel="prev" href="<$MTEntryPermalink$>" title="<$MTEntryTitle encode_html="1"$>" />
</MTEntryPrevious>
<MTEntryNext>
<link rel="next" href="<$MTEntryPermalink$>" title="<$MTEntryTitle encode_html="1"$>" />
</MTEntryNext>
<MTInclude module="Remember Me">

<$MTEntryTrackbackData$>

<MTBlogIfCCLicense>
<$MTCCLicenseRDF$>
</MTBlogIfCCLicense>

</head>

<body>

<div id="container">

<div id="banner">
<h1><a href="<$MTBlogURL$>" accesskey="1"><$MTBlogName encode_html="1"$></a></h1>
<h2><$MTBlogDescription$></h2>
</div>

<div class="content">

<p align="right">
<MTEntryPrevious>
<a href="<$MTEntryPermalink$>">&laquo; <$MTEntryTitle$></a> |
</MTEntryPrevious>
<a href="<$MTBlogURL$>"><MT_TRANS phrase="Main"></a>
<MTEntryNext>
| <a href="<$MTEntryPermalink$>"><$MTEntryTitle$> &raquo;</a>
</MTEntryNext>
</p>

<h2><$MTEntryDate format="%x"$></h2>

<h3><$MTEntryTitle$></h3>

<$MTEntryBody$>

<div id="a<$MTEntryID pad="1"$>more"><div id="more">
<$MTEntryMore$>
</div></div>

<p class="posted"><MT_TRANS phrase="Posted by"> <$MTEntryAuthor$> <MT_TRANS phrase="at"> <$MTEntryDate$></p>

<MTEntryIfAllowPings>
<h2 id="trackbacks"><MT_TRANS phrase="Trackback Pings"></h2>
<p class="techstuff"><MT_TRANS phrase="TrackBack URL for this entry:"><br />
<$MTEntryTrackbackLink$></p>

<MTIfNonZero tag="MTEntryTrackbackCount">
<p><MT_TRANS phrase="Listed below are links to weblogs that reference"> <a href="<$MTEntryPermalink$>"><$MTEntryTitle$></a>:</p>

<MTPings>
<p id="p<$MTPingID$>">
&raquo; <a href="<$MTPingURL$>"><$MTPingTitle$></a> from <$MTPingBlogName$><br />
<$MTPingExcerpt$> <a href="<$MTPingURL$>">[<MT_TRANS phrase="Read More">]</a>
</p>
<p class="posted"><MT_TRANS phrase="Tracked on"> <$MTPingDate$></p>
</MTPings>
</MTIfNonZero>
</MTEntryIfAllowPings>

<MTEntryIfAllowComments>

<h2 id="comments"><MT_TRANS phrase="Comments"></h2>

<MTComments>
<div id="c<$MTCommentID$>">
<$MTCommentBody$>
</div>
<p class="posted"><MT_TRANS phrase="Posted by:"> <$MTCommentAuthorLink default_name="Anonymous" spam_protect="1"$> <MTCommentAuthorIdentity> <MT_TRANS phrase="at"> <$MTCommentDate$></p>
</MTComments>

<MTEntryIfCommentsOpen>

<MTIfCommentsAllowed>

<h2><MT_TRANS phrase="Post a comment"></h2>

<MTIfRegistrationRequired>

<MTIfNonEmpty tag="MTTypeKeyToken">
<div id="thanks">
<p><MT_TRANS phrase="Thanks for signing in, ">
<script type="text/javascript" src="<MTCGIPath><MTCommentScript>?__mode=cmtr_name_js"></script><script>document.write(commenter_name);</script>.
<MT_TRANS phrase="Now you can comment."> (<a href="<$MTRemoteSignOutLink static="1"$>"><MT_TRANS phrase="sign out"></a>)</p>

<MT_TRANS phrase="(If you haven\'t left a comment here before, you may need to be approved by the site owner before your comment will appear. Until then, it won\'t appear on the entry. Thanks for waiting.)">

<form method="post" action="<$MTCGIPath$><$MTCommentScript$>" name="comments_form" onsubmit="if (this.bakecookie[0].checked) rememberMe(this)">
<input type="hidden" name="static" value="1" />
<input type="hidden" name="entry_id" value="<$MTEntryID$>" />

<p><label for="url"><MT_TRANS phrase="URL">:</label><br />
<input tabindex="1" type="text" name="url" id="url" />
<MT_TRANS phrase="Remember me?">
<input type="radio" id="remember" name="bakecookie" onclick="rememberMe(this.form)" /><label for="remember"><MT_TRANS phrase="Yes"></label><input type="radio" id="forget" name="bakecookie" onclick="forgetMe(this.form)" value="Forget Info" style="margin-left: 15px;" /><label for="forget"><MT_TRANS phrase="No"></label><br style="clear: both;" />

</p>

<p><label for="text"><MT_TRANS phrase="Comments">:</label><br />
<textarea tabindex="2" id="text" name="text" rows="10" cols="50"></textarea></p>

<div align="center">
<input type="submit" tabindex="3" name="preview" value="&nbsp;<MT_TRANS phrase="Preview">&nbsp;" />
<input style="font-weight: bold;" tabindex="4" type="submit" name="post" value="&nbsp;<MT_TRANS phrase="Post">&nbsp;" />
</div>
</form>

</div>

<script language="javascript" type="text/javascript">
<!--
if (commenter_name) {
    document.getElementById(\'thanks\').style.display = \'block\';
} else {
    document.write(\'<MT_TRANS phrase="You are not signed in. You need to be registered to comment on this site."> <a href="<$MTRemoteSignInLink static="1"$>"> <MT_TRANS phrase="Sign in"></a>\');
    document.getElementById(\'thanks\').style.display = \'none\';
}
// -->
</script>

<MTElse>
<MT_TRANS phrase="&#xA1;Comment registration is required but no TypeKey token has been given in weblog configuration!">
</MTElse>
</MTIfNonEmpty>

<MTElse> <MTTemplateNote value="Case of comments not required">

<MTIfNonEmpty tag="MTTypeKeyToken">
<script type="text/javascript" src="<MTCGIPath><MTCommentScript>?__mode=cmtr_name_js"></script>
<script language="javascript" type="text/javascript">
<!--
if (commenter_name) {
    document.write(\'<MT_TRANS phrase="Thanks for signing in, ">\', commenter_name, \'<MT_TRANS phrase=". Now you can comment."> (<a href="<$MTRemoteSignOutLink static="1"$>"><MT_TRANS phrase="sign out"></a>)\');
} else {
    document.write(\'<MT_TRANS phrase="If you have a TypeKey identity, you can"> <a href="<$MTRemoteSignInLink static="1"$>"> <MT_TRANS phrase="sign in"></a> <MT_TRANS phrase="to use it here.">\');
}
// -->
</script>
</MTIfNonEmpty>

<form method="post" action="<$MTCGIPath$><$MTCommentScript$>" name="comments_form" onsubmit="if (this.bakecookie[0].checked) rememberMe(this)">
<input type="hidden" name="static" value="1" />
<input type="hidden" name="entry_id" value="<$MTEntryID$>" />

<div id="name_email">
<p><label for="author"><MT_TRANS phrase="Name">:</label><br />
<input tabindex="1" id="author" name="author" /></p>

<p><label for="email"><MT_TRANS phrase="Email Address">:</label><br />
<input tabindex="2" id="email" name="email" /></p>
</div>

<MTIfNonEmpty tag="MTTypeKeyToken">
<script language="javascript" type="text/javascript">
<!--
if (commenter_name) {
    document.getElementById(\'name_email\').style.display = \'none\';
}
// -->
</script>
</MTIfNonEmpty>

<p><label for="url"><MT_TRANS phrase="URL">:</label><br />
<input tabindex="3" type="text" name="url" id="url" />
<MT_TRANS phrase="Remember Me?">
<input type="radio" id="remember" onclick="rememberMe(this.form)" name="bakecookie" /><label for="remember"><MT_TRANS phrase="Yes"></label><input type="radio" id="forget" name="bakecookie" onclick="forgetMe(this.form)" value="Forget Info" style="margin-left: 15px;" /><label for="forget"><MT_TRANS phrase="No"></label><br style="clear: both;" />
</p>

<p><label for="text"><MT_TRANS phrase="Comments">:</label> <MTIfAllowCommentHTML>
<MT_TRANS phrase="(you may use HTML tags for style)"></MTIfAllowCommentHTML><br/>
<textarea tabindex="4" id="text" name="text" rows="10" cols="50"></textarea></p>

<div align="center">
<input type="submit" name="preview" tabindex="5" 
    value="&nbsp;<MT_TRANS phrase="Preview">&nbsp;" />
<input style="font-weight: bold;" type="submit" name="post" 
    tabindex="6" value="&nbsp;<MT_TRANS phrase="Post">&nbsp;" />
</div>
</form>

</MTElse>

</MTIfRegistrationRequired>
</MTIfCommentsAllowed>

<script type="text/javascript" language="javascript">
<!--
if (document.comments_form.email != undefined)
    document.comments_form.email.value = getCookie("mtcmtmail");
if (document.comments_form.author != undefined)
    document.comments_form.author.value = getCookie("mtcmtauth");
if (document.comments_form.url != undefined)
    document.comments_form.url.value = getCookie("mtcmthome");
if (getCookie("mtcmtauth") || getCookie("mtcmthome")) {
    document.comments_form.bakecookie[0].checked = true;
} else {
    document.comments_form.bakecookie[1].checked = true;
}
//-->
</script>
</MTEntryIfCommentsOpen>

</MTEntryIfAllowComments>

</div>
</div>

</body>
</html>',
            'name' => 'Individual Entry Archive',
            'type' => 'individual',
            'rebuild_me' => '0'
          },
          {
            'text' => '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=<$MTPublishCharset$>" />
<meta name="generator" content="http://www.movabletype.org/" />

<title><$MTBlogName encode_html="1"$>: <MT_TRANS phrase="Discussion on"> <$MTEntryTitle$></title>

<link rel="stylesheet" href="<$MTBlogURL$>styles-site.css" type="text/css" />

</head>

<body onload="window.focus()">

<div id="banner">
<h1><MT_TRANS phrase="Continuing the discussion..."></h1>
</div>

<div class="content">

<p><MT_TRANS phrase="TrackBack URL for this entry:"><br />
<$MTEntryTrackbackLink$></p>

<p><MT_TRANS phrase="Listed below are links to weblogs that reference"> <a href="<$MTEntryPermalink$>">\'<$MTEntryTitle$>\'</a> <MT_TRANS phrase="from"> <a href="<$MTBlogURL$>"><$MTBlogName encode_html="1"$></a>.</p>

<MTPings>
<p id="p<$MTPingID$>">
&raquo; <a href="<$MTPingURL$>"><$MTPingTitle$></a> from <$MTPingBlogName encode_html="1"$><br />
<$MTPingExcerpt$> <a href="<$MTPingURL$>">[<MT_TRANS phrase="Read More">]</a>
</p>
<p class="posted"><MT_TRANS phrase="Tracked on"> <$MTPingDate$></p>
</MTPings>

</div>

</body>
</html>',
            'name' => 'TrackBack Listing Template',
            'type' => 'pings',
            'rebuild_me' => '0'
          },
          { 'type' => 'custom',
            'name' => 'Remember Me',
            'text' => '<script type="text/javascript" language="javascript">
<!--

var HOST = \'<$MTBlogHost$>\';

// Copyright (c) 1996-1997 Athenia Associates.
// http://www.webreference.com/js/
// License is granted if and only if this entire
// copyright notice is included. By Tomer Shiran.

function setCookie (name, value, expires, path, domain, secure) {
    var curCookie = name + "=" + escape(value) + (expires ? "; expires=" + expires : "") + (path ? "; path=" + path : "") + (domain ? "; domain=" + domain : "") + (secure ? "secure" : "");
    document.cookie = curCookie;
}

function getCookie (name) {
    var prefix = name + \'=\';
    var c = document.cookie;
    var nullstring = \'\';
    var cookieStartIndex = c.indexOf(prefix);
    if (cookieStartIndex == -1)
        return nullstring;
    var cookieEndIndex = c.indexOf(";", cookieStartIndex + prefix.length);
    if (cookieEndIndex == -1)
        cookieEndIndex = c.length;
    return unescape(c.substring(cookieStartIndex + prefix.length, cookieEndIndex));
}

function deleteCookie (name, path, domain) {
    if (getCookie(name))
        document.cookie = name + "=" + ((path) ? "; path=" + path : "") + ((domain) ? "; domain=" + domain : "") + "; expires=Thu, 01-Jan-70 00:00:01 GMT";
}

function fixDate (date) {
    var base = new Date(0);
    var skew = base.getTime();
    if (skew > 0)
        date.setTime(date.getTime() - skew);
}

function rememberMe (f) {
    var now = new Date();
    fixDate(now);
    now.setTime(now.getTime() + 365 * 24 * 60 * 60 * 1000);
    now = now.toGMTString();
    if (f.author != undefined)
       setCookie(\'mtcmtauth\', f.author.value, now, \'/\', \'\', \'\');
    if (f.email != undefined)
       setCookie(\'mtcmtmail\', f.email.value, now, \'/\', \'\', \'\');
    if (f.url != undefined)
       setCookie(\'mtcmthome\', f.url.value, now, \'/\', \'\', \'\');
}

function forgetMe (f) {
    deleteCookie(\'mtcmtmail\', \'/\', \'\');
    deleteCookie(\'mtcmthome\', \'/\', \'\');
    deleteCookie(\'mtcmtauth\', \'/\', \'\');
    f.email.value = \'\';
    f.author.value = \'\';
    f.url.value = \'\';
}

//-->
</script>',
            },
        ];
