#!/usr/bin/python

import pandas, re

colnames = ('Level', 'Spell', 'School', 'Casting_time', 'Range', 'Components', 'Duration', 'Effect', 'Spellbook')

spellbook_csv_file = 'SpellbookList/'+'wizard'+'.csv'

spellbook_df = pandas.read_csv( spellbook_csv_file, delimiter = ';', header=None, names=colnames )

class Spellbook():

    def __init__ (self, spell_df):
        self.sb = spell_df

    def get_spell_by_name(self, spell):
        mask = self.sb[['Spell']].apply(lambda x: x.str.contains(spell, regex=True)).any(axis=1)
        # query = self.sb[self.sb.Spell == spell ]
        return self.sb[mask] #.iloc[0] #query.iloc[0]

    def print_spell(self, spell):
        result = self.get_spell_by_name(spell).iloc[0]
        for i in result.keys():
            print( "{0} := {1}".format(i, result[i]))

    def get_player_spellbook(self,spell_list):
        if type(spell_list[0]) == str:
            query = self.get_spell_by_name( "|".join(spell_list) )
        elif type(spell_list[0]) == int:
            query = self.get_spell_by_id( "|".join(spell_list) )
        return query

sb = Spellbook( spellbook_df )
player_sb = sb.get_player_spellbook(["Shocking Grasp"])
print( player_sb.values )



