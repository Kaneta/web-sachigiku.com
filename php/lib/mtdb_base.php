<?php
# Copyright 2001-2004 Six Apart. This code cannot be redistributed without
# permission from www.movabletype.org.
#
# $Id: mtdb_base.php,v 1.13.2.1 2004/10/07 17:41:50 bchoate Exp $

class MTDatabaseBase extends ezsql {
    var $savedqueries = array();
    var $_entry_id_cache = array();
    var $_author_id_cache = array();
    var $_comment_count_cache = array();
    var $_ping_count_cache = array();
    var $_cat_id_cache = array();
    var $_blog_id_cache = array();
    var $_entry_link_cache = array();
    var $_cat_link_cache = array();
    var $_archive_link_cache = array();
    var $id;

    function MTDatabaseBase($dbuser, $dbpassword, $dbname, $dbhost) {
        $this->id = md5(uniqid('MTDatabaseBase',true));
        $this->db($dbuser, $dbpassword, $dbname, $dbhost);
    }

    function query($query) {
        $this->savedqueries[] = $query;
        parent::query($query);
    }

    function &resolve_url($path, $blog_id) {
        $path = preg_replace('!/$!', '', $path);
        $path = $this->escape($path);
        $blog_id = intval($blog_id);
        # resolve for $path -- one of:
        #      /path/to/file.html
        #      /path/to/index.html
        #      /path/to/default.asp
        #      /path/to/
        #      /path/to
        $indexes = array('index', 'default');
        $index_list = '';
        foreach ($indexes as $index) {
            if ($index_list) $index_list .= ' or ';
            $index_list .= "fileinfo_url like '$path/$index%'";
        }
        $sql = "
            select *
              from mt_blog, mt_fileinfo, mt_template
              left outer join mt_templatemap on templatemap_id = fileinfo_templatemap_id
             where fileinfo_blog_id = $blog_id
               and ((fileinfo_url = '$path' or fileinfo_url = '$path/') or ($index_list))
               and blog_id = fileinfo_blog_id
               and template_id = fileinfo_template_id
             order by length(fileinfo_url) asc
        ";
        $rows = $this->get_results($sql, ARRAY_A);
        if (!$rows) return null;
        $found = false;
        foreach ($rows as $row) {
            $fiurl = $row['fileinfo_url'];
            if ($fiurl == $path) {
                $found = true;
                break;
            }
            if ($fiurl == "$path/") {
                $found = true;
                break;
            }
            $ext = $row['blog_file_extension'];
            if (!empty($ext)) $ext = '.' . $ext;
            foreach ($indexes as $index) {
                if ($fiurl == ($path.'/'.$index.$ext))
                    $found = true;
                if ($fiurl == ($path.'/$index.html'))
                    $found = true;
                if ($fiurl == ($path.'/$index.htm'))
                    $found = true;
                if ($fiurl == ($path.'/$index.php'))
                    $found = true;
                if ($found) break;
            }
            if ($found) break;
        }
        if (!$found) return null;
        $data = array();
        foreach ($row as $key => $value) {
            if (preg_match('/^([a-z]+)/', $key, $matches)) {
                $data[$matches[1]][$key] = $value;
            }
        }
        $this->_blog_id_cache[$data['blog']['blog_id']] =& $data['blog'];
        return $data;
    }

    function load_index_template(&$ctx, $tmpl) {
        return $this->load_special_template($ctx, $tmpl, 'index');
    }

    function load_special_template(&$ctx, $tmpl, $type) {
        $blog_id = $ctx->stash('blog_id');
        $sql = "select * from mt_template where template_blog_id=$blog_id ".($tmpl ? "and template_name='".$this->escape($tmpl)."' " : "")."and template_type='".$this->escape($type)."'";
        list($row) = $this->get_results($sql, ARRAY_A);
        if (!$row) return null;
        return $row;
    }

    function category_link($cid, $args) {
        if (isset($this->_cat_link_cache[$cid])) {
            $url = $this->_cat_link_cache[$cid];
        } else {
            $sql = "select fileinfo_url, fileinfo_blog_id
                      from mt_fileinfo, mt_templatemap
                     where fileinfo_category_id = $cid
                       and fileinfo_archive_type = 'Category'
                       and templatemap_id = fileinfo_templatemap_id
                       and templatemap_is_preferred = 1";
            $rows = $this->get_results($sql, ARRAY_A);
            if (count($rows)) {
                $link =& $rows[0];
            } else {
                return null;
            }
            $blog =& $this->fetch_blog($link['fileinfo_blog_id']);
            $blog_url = $blog['blog_site_url'];
            $blog_url = preg_replace('!(https?://(?:[^/]+))/.*!', '$1', $blog_url);
            $url = $blog_url . $link['fileinfo_url'];
            $this->_cat_link_cache[$cid] = $url;
        }
        return $url;
    }

    function archive_link($ts, $at, $args) {
        if (isset($this->_archive_link_cache[$ts.';'.$at])) {
            $url = $this->_archive_link_cache[$ts.';'.$at];
        } else {
            $blog_id = $args['blog_id'];
            $sql = "select fileinfo_url
                      from mt_fileinfo, mt_templatemap
                     where fileinfo_startdate = '$ts'
                       and fileinfo_blog_id = $blog_id
                       and fileinfo_archive_type = '".$this->escape($at)."'
                       and templatemap_id = fileinfo_templatemap_id
                       and templatemap_is_preferred = 1";
            $rows = $this->get_results($sql, ARRAY_A);
            if (count($rows)) {
                $link =& $rows[0];
            } else {
                return null;
            }
            $blog =& $this->fetch_blog($blog_id);
            $blog_url = $blog['blog_site_url'];
            $blog_url = preg_replace('!(https?://(?:[^/]+))/.*!', '$1', $blog_url);
            $url = $blog_url . $link['fileinfo_url'];
            $this->_archive_link_cache[$ts.';'.$at] = $url;
        }
        return $url;
    }

    function entry_link($eid, $at, $args) {
        if (isset($this->_entry_link_cache[$eid.';'.$at])) {
            $url = $this->_entry_link_cache[$eid.';'.$at];
        } else {
            if ($at == 'Individual') {
                $sql = "select fileinfo_url, fileinfo_blog_id
                          from mt_fileinfo, mt_templatemap
                         where fileinfo_entry_id=$eid
                           and templatemap_id = fileinfo_templatemap_id
                           and templatemap_archive_type='Individual'
                           and templatemap_is_preferred = 1";
            } elseif ($at == 'Category') {
                $sql = "select fileinfo_url, fileinfo_blog_id
                          from mt_fileinfo, mt_templatemap, mt_placement
                         where placement_entry_id = $eid
                           and fileinfo_category_id = placement_category_id
                           and placement_is_primary = 1
                           and fileinfo_templatemap_id = templatemap_id
                           and templatemap_archive_type='Category'
                           and templatemap_is_preferred = 1";
            } else {
                $entry = $this->fetch_entry($eid);
                $ts = $entry['entry_created_on'];
                if ($at == 'Monthly') {
                    $ts = substr($ts, 0, 6) . '01000000';
                } elseif ($at == 'Daily') {
                    $ts = substr($ts, 0, 8) . '000000';
                } elseif ($at == 'Weekly') {
                    require_once("MTUtil.php");
                    list($ws, $we) = start_end_week($ts);
                    $ts = $ws;
                } elseif ($at == 'Yearly') {
                    $ts = substr($ts, 0, 4) . '0101000000';
                }
                $sql = "select fileinfo_url, fileinfo_blog_id
                          from mt_fileinfo, mt_templatemap
                         where fileinfo_templatemap_id = templatemap_id
                           and fileinfo_startdate = '$ts'
                           and templatemap_archive_type='".$this->escape($at)."'
                           and templatemap_is_preferred = 1";
            }
            $rows = $this->get_results($sql, ARRAY_A);
            if (count($rows)) {
                $link =& $rows[0];
            } else {
                return null;
            }
            $blog =& $this->fetch_blog($link['fileinfo_blog_id']);
            $blog_url = $blog['blog_site_url'];
            $blog_url = preg_replace('!(https?://(?:[^/]+))/.*!', '$1', $blog_url);

            $url = $blog_url . $link['fileinfo_url'];
            $this->_entry_link_cache[$eid.';'.$at] = $url;
        }
        if ($at != 'Individual') {
            if (!isset($args['no_anchor'])) {
                $url .= '#' . (isset($args['valid_html']) ? 'a' : '') .
                        sprintf("%06d", $eid);
            }
        }
        return $url;
    }

    /* recreation of generic load method functionality from MT::Object */
    function &load($class, $terms = null, $args = null) {
        $sql = "select * from mt_$class";
        $where = '';
        if ($terms) {
          if (is_array($terms)) {
            foreach ($terms as $col => $val) {
              $col = $class.'_'.$col;
              $where .= " and ($col='".mysql_escape_string($val)."')";
            }
            $where = preg_replace('/^ and/', '', $where);
          } else {
            $where = " ($class"."_id='".intval($terms)."')";
          }
          $where = 'where'.$where;
        }
      /*
        if ($args) {
          if (
        }
      */
        return $this->get_results($sql.' '.$where, ARRAY_A);
    }

    function get_template_text($ctx, $module) {
        return $this->get_var("
            select template_text
              from mt_template
             where template_blog_id=".$ctx->stash('blog_id')."
               and template_name='".$this->escape($module)."'
            ");
    }

    function &fetch_entries($args) {
        if (isset($args['blog_id'])) {
            $blog_filter = 'and entry_blog_id = '.$args['blog_id'];
            $blog =& $this->fetch_blog($args['blog_id']);
        } else {
            $blog_filter = '';
        }
        if (isset($args['lastn'])) {
            $limit = intval($args['lastn']);
        }
        if (isset($args['days'])) {
            $day_limit = 'and date_add(entry_created_on, interval '.intval($args['days']).' day) >= now()';
        } else {
            if ((!isset($args['current_timestamp']) && !isset($args['current_timestamp_end'])) && ($limit <= 0) && (!isset($args['category'])) && (isset($blog))) {
                $days = $blog['blog_days_on_index'];
                $days or $days = 10;
                $day_limit = 'and date_add(entry_created_on, interval '.$days.' day) >= now()';
            }
        }
        if (isset($args['recently_commented_on']) && ($rco = $args['recently_commented_on'])) {
            $comment_join = 'inner join mt_comment on comment_entry_id = entry_id and comment_visible = 1';
            if ($blog) {
                $comment_join .= ' and comment_blog_id = '.$blog['blog_id'];
            }
            $sort_field = 'comment_created_on';
            $order = 'desc';
            $limit = $rco;
            $day_limit = '';
            $distinct = 'distinct';
        }
        if (isset($args['offset'])) {
            $offset = 'offset '.intval($args['offset']);
        }
        if (!isset($rco)) {
             $order = 'desc';
            if (isset($args['sort_order'])) {
                if ($args['sort_order'] == 'ascend') {
                    $order = 'asc';
                }
            } elseif (isset($blog) && isset($blog['blog_sort_order_posts'])) {
                if ($blog['blog_sort_order_posts'] == 'ascend') {
                    $order = 'asc';
                }
            }
        }
        $sort_field or $sort_field = 'entry_created_on';
        if (isset($args['sort_by'])) {
            if ($args['sort_by'] == 'title') {
                $sort_field = 'entry_title';
            } elseif ($args['sort_by'] == 'status') {
                $sort_field = 'entry_status';
            } elseif ($args['sort_by'] == 'modified_on') {
                $sort_field = 'entry_modified_on';
            } elseif ($args['sort_by'] == 'author_id') {
                $sort_field = 'entry_author_id';
            } elseif ($args['sort_by'] == 'excerpt') {
                $sort_field = 'entry_excerpt';
            }
        }
        if (isset($args['author'])) {
            $author_filter = 'and author_name = ' . "'" . $this->escape($args['author']) . "'";
        } else {
            $author_filter = '';
        }
        $start = isset($args['current_timestamp']) ? $args['current_timestamp'] : null;
        $end = isset($args['current_timestamp_end']) ? $args['current_timestamp_end'] : null;
        if (isset($args['entry_id'])) {
            $entry_filter = 'and entry_id = '.$args['entry_id'];
            $start = ''; $end = ''; $limit = 1; $blog_filter = ''; $day_limit = '';
        } else {
            $entry_filter = '';
        }
        if (isset($args['not_entry_id'])) {
            $entry_filter .= 'and entry_id != '.$args['not_entry_id'];
        }
        if ($start and $end) {
            $daterange = "and entry_created_on between '$start' and '$end'";
        } elseif ($start) {
            $daterange = "and entry_created_on >= '$start'";
        } elseif ($end) {
            $daterange = "and entry_created_on <= '$end'";
        } else {
            $daterange = '';
        }
        if ($limit > 0) {
            $limit = "limit $limit";
        } else {
            $limit = '';
        }
        if ($cat_name = isset($args['category']) ? $args['category'] : null) {
            $cats = preg_split('/\s+(AND|OR)\s+/', $cat_name);
            $is_and = preg_match('/\sAND\s/', $args['category']);
            $name_list = '';
            foreach ($cats as $cat) {
                if ($name_list != '') $name_list .= ',';
                $name_list .= "'".$this->escape($cat)."'";
            }
            $sql = "
                select $distinct mt_entry.*, mt_category.*, mt_placement.*, mt_trackback.*, mt_author.*
                  from mt_placement, mt_category, mt_entry
            left outer join mt_trackback on trackback_entry_id = entry_id,
                       mt_author
            $comment_join
                 where category_id = placement_category_id
                   $blog_filter
                   $entry_filter
                   and entry_id = placement_entry_id
                   and entry_status = 2
                   and entry_author_id = author_id
                   $author_filter
                   and category_label in ($name_list)
                   $daterange
                   $day_limit
                 order by $sort_field $order
                 $limit $offset
            ";
        } else {
            $sql = "
                select $distinct mt_entry.*, mt_placement.*, mt_trackback.*, mt_author.*
                  from mt_entry
            left outer join mt_placement on placement_entry_id = entry_id and placement_is_primary = 1
            left outer join mt_trackback on trackback_entry_id = entry_id,
                       mt_author
            $comment_join
                 where entry_status = 2
                   $blog_filter
                   $entry_filter
                   and entry_author_id = author_id
                   $author_filter
                   $daterange
                   $day_limit
                 order by $sort_field $order
                 $limit $offset
            ";
        }
        $entries = $this->get_results($sql, ARRAY_A);

        $id_list = array();
        $last_date = '';
        $seen = array();
        if (is_array($entries)) {
            foreach ($entries as $key => $entry) {
                if (isset($seen[$entry['entry_id']]))
                    continue;
                $id_list[] = $entry['entry_id'];
                $entries[$key]['entry_created_on'] = preg_replace('/[^0-9]/', '', $entries[$key]['entry_created_on']);
                $entries[$key]['EntriesHeader'] = $key == 0;
                $entries[$key]['EntriesFooter'] = $key == count($entries)-1;
                $entry_date = substr($entry['entry_created_on'],0,10);
                $entries[$key]['DateHeader'] = 0;
                $entries[$key]['DateFooter'] = 0;
                $entries[$key]['EntryBreak'] = 0;
                if ($last_date != $entry_date) {
                    $entries[$key]['DateHeader'] = 1;
                    $entries[$key]['DateFooter'] = $key > 0;
                    $last_date = $entry_date;
                }
                if ($key == count($entries)-1) {
                    $entries[$key]['DateFooter'] = 1;
                } else {
                    $entries[$key]['DateFooter'] = $last_date != substr($entries[$key+1]['entry_created_on'],0,10);
                }
                if (!$entries[$key]['DateFooter']) {
                    if (!$entries[$key]['EntriesFooter']) {
                        $entries[$key]['EntryBreak'] = 1;
                    }
                }
                $seen[$entries[$key]['entry_id']] = 1;
            }
        }

        # pre-cache comment counts and categories for these entries
        $this->cache_comment_counts($id_list);
        $this->cache_ping_counts($id_list);
        $this->cache_categories($id_list);
        $this->cache_permalinks($id_list);

        return $entries;
    }

/*
    function now_ts($blog) {
        $tsa = offset_time_list(time(), $blog);
        $now = sprintf("%04d%02d%02d%02d%02d%02d", $tsa[5] + 1900, $tsa[4] + 1, $tsa[3], $tsa[2], $tsa[1], $tsa[0]);
        return $now;
    }
*/

    function &fetch_categories($args) {
        # load categories
        if (isset($args['blog_id'])) {
            $blog_filter = 'and category_blog_id = '.intval($args['blog_id']);
        }
        if (isset($args['category_id'])) {
            if (isset($args['children'])) {
                if (isset($this->_cat_id_cache['c'.$args['category_id']])) {
                    $cat = $this->_cat_id_cache['c'.$args['category_id']];
                    if (isset($cat['_children'])) {
                        $children = &$cat['_children'];
                        if ($children === false) {
                            return null;
                        } else {
                            return $children;
                        }
                    }
                }

                $cat_filter = 'and category_parent = '.intval($args['category_id']);
            } else {
                $cat_filter = 'and category_id = '.intval($args['category_id']);
                $limit = 1;
            }
        } elseif (isset($args['label'])) {
            $cat_filter = 'and category_label = \''.$this->escape($args['label']).'\'';
            $limit = 1;
        } else {
            $limit = $args['lastn'];
            if (isset($args['sort_order'])) {
                if ($args['sort_order'] == 'ascend') {
                    $sort_order = 'asc';
                } elseif ($args['sort_order'] == 'descend') {
                    $sort_order = 'desc';
                }
            } else {
                $sort_order = '';
            }
        }
        if (isset($args['entry_id'])) {
            $entry_filter = 'and placement_entry_id = '.intval($args['entry_id']);
        }
        if ($args['show_empty']) {
            $join_clause = 'left outer join mt_placement on placement_category_id = category_id';
        } else {
            $join_clause = ', mt_placement';
            $cat_filter .= ' and placement_category_id = category_id';
        }
        if ($limit > 0) {
            $limit = "limit $limit";
        } else {
            $limit = '';
        }
        $sql = "
            select mt_category.*, mt_trackback.*, count(mt_placement.placement_id) as category_count
              from mt_category $join_clause
                   left outer join mt_trackback on trackback_category_id = category_id
             where 1 = 1
                   $cat_filter
                   $entry_filter
                   $blog_filter
             group by category_id
             order by category_label $sort_order
             $limit
        ";
        if (empty($cat_filter) && empty($entry_filter)) {
            $args['top_level_categories'] = 1;
        }
        $categories = $this->get_results($sql, ARRAY_A);
        if (!$categories) {
            return null;
        }
        if (isset($args['children']) && isset($parent_cat)) {
            $parent_cat['_children'] =& $categories;
        } else {
            $id_list = array();
            foreach ($categories as $cid => $cat) {
                $cat_id = $cat['category_id'];
                if (isset($args['top_level_categories']) || !isset($this->_cat_id_cache['c'.$cat_id])) {
                    $id_list[] = $cat_id;
                    $this->_cat_id_cache['c'.$cat_id] = &$categories[$cid];
                }
                if (isset($args['top_level_categories'])) {
                    $this->_cat_id_cache['c'.$cid]['_children'] = false;
                }
            }

            $top_cats = array();
            foreach ($categories as $cid => $cat) {
                if ($cat['category_parent'] > 0) {
                    if (!isset($categories[$cid]['category_parent'])) {
                        $parent_id = $cat['category_parent'];
                        if (isset($this->_cat_id_cache['c'.$parent_id])) {
                            if (isset($args['top_level_categories'])) {
                                $parent =& $this->fetch_category($categories[$cid]['category_parent']);
                                if (!isset($parent['_children']) || ($parent['_children'] === false)) {
                                    $parent['_children'] = array(&$categories[$cid]);
                                } else {
                                    $parent['_children'][] = &$categories[$cid];
                                }
                            }
                        }
                    } else {
                        if (isset($args['top_level_categories'])) {
                            $parent = &$this->fetch_category($categories[$cid]['category_parent']);
                            $parent['_children'][] = &$categories[$cid];
                        }
                    }
                }
                if ((!$cat['category_parent']) && (isset($args['top_level_categories']))) {
                    $top_cats[] = &$categories[$cid];
                }
            }
            $this->cache_category_links($id_list);
            if (isset($args['top_level_categories'])) {
                return $top_cats;
            }
        }
        return $categories;
    }

    function &fetch_entry($entry_id) {
        if (isset($this->_entry_id_cache['entry_id'])) {
            return $this->_entry_id_cache[$entry_id];
        }
        list($entry) = $this->fetch_entries(array('entry_id' => $entry_id));
        $this->_entry_id_cache[$entry_id] = &$entry;
        return $entry;
    }

    function &fetch_author($author_id) {
        if (isset($this->_author_id_cache[$author_id])) {
            return $this->_author_id_cache[$author_id];
        }
        $author = $this->get_row("
            select *
              from mt_author
             where author_id=$author_id
        ", ARRAY_A);
        $this->_author_id_cache[$author_id] = &$author;
        return $author;
    }

    function cache_permalinks(&$entry_list) {
        $id_list = '';
        foreach ($entry_list as $entry_id) {
            if (!isset($this->_entry_link_cache[$entry_id.';Individual'])) {
                $id_list .= ','.$entry_id;
                $this->_entry_link_cache[$entry_id.';Individual'] = ''; 
            }
        }
        if (empty($id_list))
            return;
        $id_list = substr($id_list, 1);
        $query = "
            select fileinfo_entry_id, fileinfo_url, blog_site_url
              from mt_fileinfo, mt_templatemap, mt_blog
             where fileinfo_entry_id in ($id_list)
               and fileinfo_archive_type = 'Individual'
               and blog_id = fileinfo_blog_id
               and templatemap_id = fileinfo_templatemap_id
               and templatemap_is_preferred = 1
        ";
        $results = $this->get_results($query, ARRAY_N);
        if ($results) {

            foreach ($results as $row) {
                $blog_url = $row[2];
                $blog_url = preg_replace('!(https?://(?:[^/]+))/.*!', '$1', $blog_url);
                $url = $blog_url . $row[1];
                $this->_entry_link_cache[$row[0].';Individual'] = $url;
            }
        }
    }

    function cache_category_links(&$cat_list) {
        $id_list = '';
        foreach ($cat_list as $cat_id) {
            if (!isset($this->_cat_link_cache[$cat_id])) {
                $id_list .= ','.$cat_id;
                $this->_cat_link_cache[$cat_id] = '';
            }
        }
        if (empty($id_list))
            return;
        $id_list = substr($id_list, 1);
        $query = "
            select fileinfo_category_id, fileinfo_url, blog_site_url
              from mt_fileinfo, mt_templatemap, mt_blog
             where fileinfo_category_id in ($id_list)
               and fileinfo_archive_type = 'Category'
               and blog_id = fileinfo_blog_id
               and templatemap_id = fileinfo_templatemap_id
               and templatemap_is_preferred = 1
        ";
        $results = $this->get_results($query, ARRAY_N);
        if ($results) {

            foreach ($results as $row) {
                $blog_url = $row[2];
                $blog_url = preg_replace('!(https?://(?:[^/]+))/.*!', '$1', $blog_url);
                $url = $blog_url . $row[1];
                $this->_cat_link_cache[$row[0]] = $url;
            }
        }
    }

    function cache_comment_counts(&$entry_list) {
        $id_list = '';
        foreach ($entry_list as $entry_id) {
            if (!isset($this->_comment_count_cache[$entry_id])) {
                $id_list .= ','.$entry_id;
            }
        }
        if (empty($id_list))
            return;
        $id_list = substr($id_list, 1);
        $query = "
            select comment_entry_id, count(*)
              from mt_comment
             where comment_entry_id in ($id_list)
               and comment_visible = 1
             group by comment_entry_id
        ";
        $results = $this->get_results($query, ARRAY_N);
        foreach ($entry_list as $entry_id) {
            $this->_comment_count_cache[$entry_id] = 0;
        }
        if ($results) {
            foreach ($results as $row) {
                $this->_comment_count_cache[$row[0]] = $row[1];
            }
        }
    }

    function blog_entry_count($blog_id) {
        $count = $this->get_var("
          select count(*)
            from mt_entry
           where entry_blog_id = $blog_id
             and entry_status = 2");
        return $count;
    }

    function blog_comment_count($blog_id) {
        $count = $this->get_var("
            select count(*)
              from mt_entry, mt_comment
             where entry_blog_id = $blog_id
               and entry_status = 2
               and comment_visible = 1
               and comment_entry_id = entry_id");
        return $count;
    }

    function entry_comment_count($entry_id) {
        if (isset($this->_comment_count_cache[$entry_id])) {
            return $this->_comment_count_cache[$entry_id];
        }
        $count = $this->get_var("
            select count(*)
              from mt_comment 
               and comment_visible = 1
             where comment_entry_id = $entry_id
        ");
        $this->_comment_count_cache[$entry_id] = $count;
        return $count;
    }

    function &fetch_comments($args) {
        $entry_id = $args['entry_id'];
        # load comments
        $limit = isset($args['lastn']) ? $args['lastn'] : null;
        if ($limit > 0) {
            $limit = "limit $limit";
        } else {
            $limit = '';
        }
        $order = 'desc';
        if (isset($args['sort_order'])) {
            if ($args['sort_order'] == 'ascend') {
                $order = 'asc';
            }
        } elseif (isset($args['blog_id'])) {
            $blog =& $this->fetch_blog($args['blog_id']);
            if ($blog['blog_sort_order_comments'] == 'ascend') {
                $order = 'asc';
            }
        }
        $comments = $this->get_results("
            select *
              from mt_comment
             where comment_entry_id = $entry_id
               and comment_visible = 1
             order by comment_created_on $order
             $limit", ARRAY_A);
  
        if (!is_array($comments))
            return array();
  
        return $comments;
    }
    
    function cache_ping_counts(&$entry_list) {
        $id_list = '';
        foreach ($entry_list as $entry_id) {
            if (!isset($this->_ping_count_cache[$entry_id])) {
                $id_list .= ','.$entry_id;
            }
        }
        $id_list = substr($id_list, 1);
        if (empty($id_list))
            return;
        $query = "
            select trackback_entry_id, count(*)
              from mt_trackback, mt_tbping
             where trackback_entry_id in ($id_list)
               and tbping_tb_id = trackback_id
             group by trackback_entry_id
        ";
        $results = $this->get_results($query, ARRAY_N);
        foreach ($entry_list as $entry_id) {
            $this->_ping_count_cache[$entry_id] = 0;
        }
        if ($results) {
            foreach ($results as $row) {
                $this->_ping_count_cache[$row[0]] = $row[1];
            }
        }
    }

    function entry_ping_count($entry_id) {
       if (isset($this->_ping_count_cache[$entry_id])) {
            return $this->_ping_count_cache[$entry_id];
        }
        $count = $this->get_var("
            select count(*)
              from mt_trackback, mt_tbping
             where trackback_entry_id = $entry_id
               and tbping_tb_id = trackback_id 
        ");
        $_ping_count_cache[$entry_id] = $count;
        return $count;
    }

    function &fetch_pings($args) {
        $entry_id = $args['entry_id'];
        # load pings  
        $limit = $args['lastn'];
        if ($limit > 0) {
            $limit = "limit $limit";
        } else {
            $limit = '';
        }
        $order = 'asc';
        if (isset($args['sort_order'])) {
            if ($args['sort_order'] == 'descend') {
                $order = 'desc';
            }
        }
        $pings = $this->get_results("
            select *  
              from mt_trackback, mt_tbping
             where trackback_entry_id = '$entry_id'
               and tbping_tb_id = trackback_id
             order by tbping_created_on $order
             $limit", ARRAY_A);
        return $pings;
    }

    function cache_categories(&$entry_list) {
        $id_list = '';
        foreach ($entry_list as $entry_id) {
            if (!isset($this->_cat_id_cache['e'.$entry_id])) {
                $id_list .= ','.$entry_id;
            }
        }
        $id_list = substr($id_list, 1);
        if (!$id_list)
            return;
        $query = "
            select *
              from mt_category, mt_placement
             where placement_entry_id in ($id_list)
               and placement_category_id = category_id
               and placement_is_primary = 1
        ";
        $results = $this->get_results($query, ARRAY_A);
        foreach ($entry_list as $entry_id) {
            $this->_cat_id_cache['e'.$entry_id] = null;
        }
        if (is_array($results)) {
            foreach ($results as $row) {
                $entry_id = $row['placement_entry_id'];
                $this->_cat_id_cache['e'.$entry_id] = $row;
                $cat_id = $row['category_id'];
                $this->_cat_id_cache['c'.$cat_id] = $row;
            }
        }
    }
    
    function &fetch_category($cat_id) {
        if (isset($this->_cat_id_cache['c'.$cat_id])) {
            return $this->_cat_id_cache['c'.$cat_id];
        }
        $cats =& $this->fetch_categories(array('category_id' => $cat_id));
        if ($cats && (count($cats) > 0)) {
            $this->_cat_id_cache['c'.$cat_id] = &$cats[0];
            return $cats[0];
        } else {
            return null;
        }
    }
    
    function &fetch_blog($blog_id) {
        if (isset($this->_blog_id_cache[$blog_id])) {
            return $this->_blog_id_cache[$blog_id];
        }
        list($blog) = $this->load('blog', $blog_id);
        $this->_blog_id_cache[$blog_id] = &$blog;
        return $blog;
    }

    function &get_archive_list($args) {
        $blog_id = $args['blog_id'];
        if (($n = $args['lastn']) && ($n > 0)) {
            $limit = "limit $n";
        } else {
            $limit = '';
        }
        $at = $args['archive_type'];
        if ($at == 'Daily') {
            $group_sql = "
                select count(*),
                       extract(year from entry_created_on),
                       extract(month from entry_created_on),
                       extract(day from entry_created_on)
                  from mt_entry
                 where entry_blog_id = $blog_id
                   and entry_status = 2
                 group by
                       extract(year from entry_created_on),
                       extract(month from entry_created_on),
                       extract(day from entry_created_on)
                 order by
                       extract(year from entry_created_on) desc,
                       extract(month from entry_created_on) desc,
                       extract(day from entry_created_on) desc
                 $limit";
        } elseif ($at == 'Weekly') {
            $group_sql = "
                select count(*),
                       extract(year from entry_created_on),
                       date_format(entry_created_on,'%U')+1
                  from mt_entry
                 where entry_blog_id = $blog_id
                   and entry_status = 2
                 group by
                       extract(year from entry_created_on),
                       date_format(entry_created_on,'%U')
                 order by
                       extract(year from entry_created_on)+1 desc,
                       date_format(entry_created_on,'%U')+1 desc
                 $limit";
        } elseif ($at == 'Monthly') {
            $group_sql = "
                select count(*),
                       extract(year from entry_created_on),
                       extract(month from entry_created_on)
                  from mt_entry
                 where entry_blog_id = $blog_id
                   and entry_status = 2
                 group by
                       extract(year from entry_created_on),
                       extract(month from entry_created_on)
                 order by
                       extract(year from entry_created_on) desc,
                       extract(month from entry_created_on) desc
                 $limit";
        } elseif ($at == 'Yearly') {
            $group_sql = "
                select count(*),
                       extract(year from entry_created_on)
                  from mt_entry
                 where entry_blog_id = $blog_id
                   and entry_status = 2
                 group by
                       extract(year from entry_created_on)
                 order by
                       extract(year from entry_created_on) desc
                 $limit";
        } elseif ($at == 'Individual') {
            $group_sql = "
                select entry_id,
                       entry_created_on
                  from mt_entry
                 where entry_blog_id = $blog_id
                   and entry_status = 2
                 order by
                       entry_created_on desc
                 $limit";
        }
        $results = $this->get_results($group_sql, ARRAY_N);
        if (is_array($results)) {
            if ($at == 'Daily') {
                $hi = sprintf("%04d%02d%02d", $results[0][1], $results[0][2], $results[0][3]);
                $low = sprintf("%04d%02d%02d", $results[count($results)-1][1], $results[count($results)-1][2], $results[count($results)-1][3]);
            } elseif ($at == 'Weekly') {
                require_once("MTUtil.php");
                list($y,$m,$d) = week2ymd($results[0][1], $results[0][2]);
                $hi = sprintf("%04d%02d%02d", $y, $m, $d);
                list($y,$m,$d) = week2ymd($results[count($results)-1][1], $results[count($results)-1][2]);
                $low = sprintf("%04d%02d%02d", $y, $m, $d);
            } elseif ($at == 'Monthly') {
                $hi = sprintf("%04d%02d00", $results[0][1], $results[0][2]);
                $low = sprintf("%04d%02d00", $results[count($results)-1][1], $results[count($results)-1][2]);
            } elseif ($at == 'Yearly') {
                $hi = sprintf("%04d0000", $results[0][1]);
                $low = sprintf("%04d0000", $results[count($results)-1][1]);
            } elseif ($at == 'Individual') {
                $hi = $results[0][1];
                $low = $results[count($results)-1][1];
            }
            $range = "'$low' and '$hi'";
            $link_cache_sql = "
                select fileinfo_startdate, fileinfo_url, blog_site_url
                  from mt_fileinfo, mt_templatemap, mt_blog
                 where fileinfo_startdate between $range
                   and fileinfo_archive_type = '$at'
                   and blog_id = $blog_id
                   and fileinfo_blog_id = blog_id
                   and templatemap_id = fileinfo_templatemap_id
                   and templatemap_is_preferred = 1
            ";
            $cache_results = $this->get_results($link_cache_sql, ARRAY_N);
            if (is_array($cache_results)) {
                foreach ($cache_results as $row) {
                    $date = $row[0];
                    $blog_url = $row[2];
                    $blog_url = preg_replace('!(https?://(?:[^/]+))/.*!', '$1', $blog_url);
                    $url = $blog_url . $row[1];
                    $this->_archive_link_cache[$date.';'.$at] = $url;
                }
            }
        }
        return $results;
    }

    function get_author_token($blog_id) {
        $auth_token = $this->get_var("
            select author_remote_auth_token
              from mt_author, mt_permission
             where permission_blog_id = $blog_id
               and author_remote_auth_token is not null
             limit 1");
        return $auth_token;
    }
}
?>
