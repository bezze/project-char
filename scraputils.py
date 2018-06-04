#!/usr/bin/env python3

from bs4 import element
import urllib.request

#-------------------------------------------------------------------------------
def download_html(link, filename=False):
    UserAgent="Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"
    request =urllib.request.Request(link)
    request.add_header('User-Agent',UserAgent)
    linktext = urllib.request.urlopen(request)
    return linktext

#-------------------------------------------------------------------------------
is_linebreak = lambda x: True if (isinstance(x, element.NavigableString) and x == '\n') else False
is_navstring = lambda x: True if (isinstance(x, element.NavigableString)) else False
has_subelements = lambda x: True if (not is_navstring(x) and len(x.contents) > 1) else False #
get_header_number = lambda h: int(h.name[1]) if len(h.name) == 2 else 0
get_text = lambda h: ' '.join(h.text.replace('\n',' ').strip().split())
is_key = lambda k,d : True if k in d.keys() else False
not_empty = lambda d: True if len( d ) != 0 else False

def header_indent_lvl (t,l):
    if l==1: # h2
        return ' ■ '+get_text(t)+'\n\n'
    elif l==2: # h2 sub
        return '\n\n • '+get_text(t)+'\n\n'

def has_name ( tag ):
    try:
        tag.name
        return True
    except AttributeError:
        return False

def return_nstring_text ( tag ):
    if is_navstring(tag):
        return tag.string.strip()
    elif tag.name == 'strong':
        return header_indent_lvl(tag,2)
    else:
        return ' '+tag.text.strip()+' '

def get_header_n_t (h):
    return get_header_number(h), get_text(h)

def ask_parent(parent_dic, sprev, s):

    if sprev == None:
        return None

    sprev_n, sprev_t = get_header_n_t(sprev)
    s_n, s_t = get_header_n_t(s)

    if  sprev_n == s_n:
        return parent_dic[sprev]
    elif sprev_n > s_n:
        ask_parent( parent_dic, parent_dic[sprev], s )

def has_attr ( x,a ):
    # x: tag, a:regex string
    r=re.compile(a)
    matches = []
    if type(x) == element.Tag and x.attr != None:
        for w in x.attr:
            matches.append( re.match(r,w) != None )
        return any( matches )
    else:
        return False

def parse_table_tag (tds):
    row = []
    for td in tds:
        if has_subelements(td):
            row.append( get_text(td) )
        else:
            if td.string != '\n':
                row.append(get_text(td) )
    return row

parse_table_row = lambda tag, subtagname: parse_table_tag( tag.find_all(subtagname) )

def meta_return_table_n_stuff (attribute, value):
    def return_table_n_stuff  (tag):
        try:
            if tag.attrs[attribute] == value:
                return True
            else: False
        except KeyError:
            return False
    return return_table_n_stuff
