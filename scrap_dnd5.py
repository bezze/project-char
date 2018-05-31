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

headers = soup.find_all(attrs={ "name" : re.compile('h-')} )
for s in headers[0].next_siblings:
    if (not is_navstring(s)) and (s!=None) and (not has_attr(s,'h-.*')):
        print( s )
    elif is_navstring( s ):
        print( s )
    else:
        print( "Finish" )
        pass
# for h in headers:
    # for sib in  h.next_siblings:
    #     print( sib )
    # if not is_navstring(h.next_sibling):
    #     print('-----------')
    #     print( h.next_sibling.text )
    #     print( h.next_sibling.next_sibling )
    # else:
    #     print('-----------')
    #     print( h.next_sibling.string )

# print( fields )
# print( table )
# print( get_nth_level( 5, table ))

