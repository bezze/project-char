#!/usr/bin/python

from bs4 import BeautifulSoup as bs

from scraputils import *
from tree import SectionTree

#-------------------------------------------------------------------------------
class TableInfo ():

    def get_fields(tag, ttype):
        fields = []
        for el in tag.find_all('tr'):
            fields.append( parse_table_row( el, ttype ) )
        return fields

    def get_fields_table( soup ):
        tag = soup.find_all( meta_return_table_n_stuff("id", "pagecontent") )[0]
        fields = TableInfo.get_fields( tag.thead, 'th')
        table = TableInfo.get_fields( tag.tbody, 'td' )
        return fields, table

    def __init__ (self, soup):
        self.fields, self.table = TableInfo.get_fields_table(soup)

    def get_nth_level (self, n):
        return self.table[n-1]

    def __repr__ (self):
        return repr(self.fields)+"\n"+repr(self.table)

class ClassInfo ():

    def __init__ (self, class_file = None):
        if class_file == None:
            raw_page = download_html(sys.argv[1]) # Real download
            classname = class_file.split('#')[-1]
        else:
            raw_page = open(class_file, 'r').read() # Testing
            classname = class_file.split('/')[-1]

        self.classname = classname
        self.soup = bs(raw_page, 'html.parser');  #print(soup.prettify())
        self.table = TableInfo(self.soup)
        self.section = SectionTree(self.soup)

    def get_section(self):
        all_sections = self.section.parse_all_sections()
        all_sections.pop('D&D; 5th Edition')
        all_sections.pop('Compendium')
        all_sections.pop(self.classname)
        return all_sections


info = ClassInfo('CharacterClasses/'+'Wizard')

# print( info.section.search_tree("Pact Boon") )
# print( info.table )
for l in info.get_section() :
    print(l, info.get_section()[l])

# header_parents_dic, header_parents_tag = create_header_parents(soup)
# # print( header_parents_dic )

# st = SectionTree( header_parents_dic )
# # print(st.search_tree("Spellcasting"))
# print(st.parents)
# print(st)
# # print( fields )
# # print( table )
# # print( get_nth_level( 5, table ))

