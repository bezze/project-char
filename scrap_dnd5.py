#!/usr/bin/python

from bs4 import BeautifulSoup as bs
from bs4 import element
import bs4
import re,sys
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
get_text = lambda h: h.text.strip()
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
    r=re.compile(a)
    matches = []
    if type(x) == element.Tag and x.attr != None:
        for w in x.attr:
            matches.append( re.match(r,w) != None )
        return any( matches )
    else:
        return False

def parse_td (tds):
    row = []
    for td in tds:
        if has_subelements(td):
            row.append( td.text.replace('\n',' ').strip() )
        else:
            if td.string != '\n':
                row.append(td.string)
    return row

parse_row = lambda tag, subtagname: parse_td( tag.find_all(subtagname) )

def meta_return_table_n_stuff (attribute, value):

    def return_table_n_stuff  (tag):
        try:
            if tag.attrs[attribute] == value:
                return True
            else: False
        except KeyError:
            return False

    return return_table_n_stuff
#-------------------------------------------------------------------------------

def get_fields (tag):
    fields = []
    for el in tag.thead.find_all('tr'):
        fields.append( parse_row( el, 'th' ) )
    return fields

def get_table ( tag ):
    table = []
    for tr in tag.tbody.find_all('tr'):
        table.append( parse_row( tr, 'td' ) )
    return table

def get_fields_table(soup):
    tag = soup.find_all( meta_return_table_n_stuff("id", "pagecontent") )[0]
    fields = get_fields( tag )
    table = get_table( tag )
    return fields, table

def get_nth_level (n, table):
    return table[n-1]

# raw_page = download_html(sys.argv[1]) # Real download
raw_page = open('Warlock', 'r').read() # Testing
soup = bs(raw_page, 'html.parser')
fields, table = get_fields_table( soup )

"""
h1
  h2
  h2
    h3
    h3
  h2
  h2
  h2
    h3
      h4
"""

def create_header_parents (soup):
    headers = soup.find_all( re.compile('h[0-9]+') )

    h_prev = None
    parents = { }
    for h in headers:
        # print( h.name, get_header_number(h), len(h.contents), h.text.strip() )
        h_n, h_t = get_header_n_t(h)
        if h_prev == None:
            h_prev_n, h_prev_t = -1, 'root'
        else:
            h_prev_n, h_prev_t = get_header_n_t(h_prev)

        if h_n > h_prev_n:
            parents[ h ] = h_prev
        elif h_n == h_prev_n:
            parents[ h ] = parents[h_prev]
        else:
            parents[ h ] = ask_parent(parents, h_prev, h)
        h_prev = h

    parents_dic = {}
    for key in parents:
        if parents[key] == None:
            parents_dic[ get_text(key) ] = None
        else:
            parents_dic[ get_text(key) ] = get_text(parents[key])

    return parents_dic, parents

header_parents_dic, header_parents_tag = create_header_parents(soup)
print( header_parents_dic )

# print( fields )
# print( table )
# print( get_nth_level( 5, table ))

