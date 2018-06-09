#!/usr/bin/python

import pandas, re

# from pandas.core.frame import DataFrame
# class newDataFrame (DataFrame):
#     def __init__(self):
#         super(newDataFrame, self).__init__()

class Spellbook():

    def __init__ (self, CharClass):
        spellbook_csv_file = 'SpellbookList/'+CharClass+'.csv'
        self.colnames = ('Level', 'Spell', 'School', 'Casting_time', 'Range', 'Components', 'Duration', 'Effect', 'Spellbook')
        spellbook_df = pandas.read_csv( spellbook_csv_file, delimiter = ';', header=None, names=self.colnames )
        self.sb = spellbook_df

    def search_spell_by_name(self, spell, regex=True):
        mask = self.sb[['Spell']].apply(lambda x: x.str.contains(spell, regex=regex )).any(axis=1)
        return self.sb[mask] #.iloc[0] #query.iloc[0]

    def get_spell (self, spell):
        if type(spell) == str:
            return self.sb[self.sb['Spell'] == spell]
        elif type(spell) == int:
            return self.sb.iloc[spell]
        else:
            raise KeyError

    def get_spell_name_mask (self, spell):
        mask = self.sb['Spell'].apply(lambda x: x==spell)
        return mask

    def get_spell_id_mask (self, spell_id):
        s = self.sb; spell = s.iloc[spell_id]
        mask = s.apply( lambda x: x.Spell==spell.Spell, axis=1 )
        return mask

    def print_spell(self, spell):
        result = self.get_spell_by_name(spell).iloc[0]
        for i in result.keys():
            print( "{0} := {1}".format(i, result[i]))

    def get_spell_id_list (self):
        get_id = lambda series, value: series[series == value].index.tolist()
        id_list=[]
        for entry in self.sb.Spell:
            id_list.append( get_id(self.sb.Spell, entry)[0] )
        return id_list

    def get_player_spellbook(self,spell_list):
        for spell in spell_list:
            if type(spell) == str: # if spell == string
                newmask = self.get_spell_name_mask( spell )
            elif type(spell) == int: # if spell == id
                newmask = self.get_spell_id_mask(spell)
            try:
                mask = mask.combine(newmask, lambda x1,x2: x1 | x2)
            except NameError:
                mask = newmask
        return self.sb[mask]

    def __repr__ (self ): # pretty df print
        return repr( self.sb )

class CharacterSpellbook(Spellbook):

    def __init__ (self, spell_list, *CharClass):
        super(CharacterSpellbook, self).__init__(*CharClass)
        # self.csb = self.sb
        self.sb = self.get_player_spellbook(spell_list)

    def add (self, spell_df):
        self.sb = self.sb.append(spell_df).sort_index()
