#!/usr/bin/env python3

from scraputils import *
import re

class Tree(dict):
    """ Tree will be a dict of dicts """

    def __build_tree (self,parents):
        """ parents is a parent dictionary, where every element stores its own
        parent i.e. parents[child] := parent """

        tree = {None:{}}
        A = parents.copy()

        def level_candidates(A, parent_lvl):
            """ returns childs of items found in the parent_lvl list """
            level = []
            for child, parent in A.items():
                if parent in parent_lvl:
                    level.append(child)
            return level

        def add_branch(tree, e):
            pe = parents[e]
            if pe in tree:
                tree[pe][e] = {}
            else:
                for parent in tree:
                    add_branch(tree[parent], e)
            return tree

        root = [None]
        level =  level_candidates(A, root)
        while not_empty(A):
            for branch in level:
                tree = add_branch( tree, branch)
                A.pop(branch)
            # Update level
            root = level
            level =  level_candidates(A, root)
        # Let's take out the root (maybe this will change)
        return tree[None]

    def __init__(self, parents=None, *arg,**kw):
        super(Tree, self).__init__(*arg, **kw)
        self.parents = parents
        self.tree = self.__build_tree(parents) if parents is not None else {}

    def search_tree(self, branch ):
        """ Returns a list with matched branches (Note that it is possible
        to have different branches with the same name)"""

        def search(k, d, l):
            if k in d:
                l.append( d[k] )
            else:
                for ks in d:
                    l.append(search(k, d[ks], l))
        l = []
        result = False
        search(branch, self.tree, l)
        result = [ i for i in l if i!=None ]
        return result

    def __repr__(self):
        return repr(self.tree)

class SectionTree (Tree):

    def create_header_parents (soup):
        headers = soup.find_all( re.compile('h[0-9]+') )
        h_prev = None
        parents_tag = { }
        for h in headers:
            # print( h.name, get_header_number(h), len(h.contents), h.text.strip() )
            h_n, h_t = get_header_n_t(h)
            if h_prev == None:
                h_prev_n, h_prev_t = -1, 'root'
            else:
                h_prev_n, h_prev_t = get_header_n_t(h_prev)

            if h_n > h_prev_n:
                parents_tag[ h ] = h_prev
            elif h_n == h_prev_n:
                parents_tag[ h ] = parents_tag[h_prev]
            else:
                parents_tag[ h ] = ask_parent(parents_tag, h_prev, h)
            h_prev = h

        parents_name = {}
        for key in parents_tag:
            if parents_tag[key] == None:
                parents_name[ get_text(key) ] = None
            else:
                parents_name[ get_text(key) ] = get_text(parents_tag[key])
        return parents_name, parents_tag

    def __init__(self, soup, *arg,**kw):
        self.__header_parents_dic, self.__header_parents_tag = SectionTree.create_header_parents(soup)
        super(SectionTree, self).__init__(parents = self.__header_parents_dic, *arg, **kw)

    def parse_all_sections(self):

        def parse_text_up_to_next_htag ( htag ):
            text = header_indent_lvl( htag,1 )
            for s in htag.next_siblings:
                # if isinstance(s, element.Tag) and s.name == 'h2':
                if isinstance(s, element.Tag) and re.match(re.compile('h[0-9]+'),s.name) != None:
                    break
                elif isinstance(s, element.Tag) and re.match(re.compile('script'),s.name) != None:
                    continue
                elif isinstance(s, element.Tag) and re.match(re.compile('Attributes'),s.name) != None:
                    text += return_nstring_text_attribute(s)
                else:
                    text += return_nstring_text(s)
            return text

        sections = {}
        for  hname, htag in zip(self.__header_parents_dic, self.__header_parents_tag):
            # if (hname == 'D&D; 5th Edition') or (hname == ):
            #     continue
            sections[hname] = parse_text_up_to_next_htag(htag)
        return sections

