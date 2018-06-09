import random
import rolls
import races as races
import classes as classes
import spellbook as spellbook

def CharGen(name, Race_, Class_, **kwargs):

    """ Returns a  Character instace which inherits from Race_ and Class_.
    Depending on the Race_ and Class_ chosen, additional parameters are needed
    which are passed directly as keyword arguments to their __init__'s
    """

    class Character(Race_, Class_):

        def __init__(self, name, age=30, raw_attr_values = 6*(10,)):
            super(Character, self).__init__(**kwargs)
            self.name = name
            self.race = Race_.__name__
            self.age = age
            self.attr = races.AttrSet( raw_attr_values )
            for dummy_attr in self.mod:
                self.attr[dummy_attr] += self.mod[dummy_attr]
            try:
                casterType = kwargs["MAGIC"][0]
                spellList = kwargs["MAGIC"][1]
                self.spellbook = spellbook.CharacterSpellbook(casterType, spellList)
            except KeyError:
                print("Not caster")

        def roll_npc(self):
            for attr in self.attr:
                self.attr[attr]=sum(rolls.roll(3,6))

        def roll_pc(self):
            for attr in self.attr:
                self.attr[attr]=sum(rolls.keep(3,rolls.roll(4,6)))

        def lvl(self):
            lvl=0
            for clase in self.Class_:
                lvl+=self.Class_[clase]
            return lvl

        def stats(self):
            print( self.attr )

    return Character(name)



ski=["Athletics","Acrobatics"]
lang=["Gnomish"]
attr=["STR", "CON"]
spelllist_id = [7, 13, 15, 18, 37, 38, 45, 52, 53, 56, 57, 58, 93, 94]
Player_1 = CharGen("Alejandro", races.WoodElf, classes.Fighter, SKILL=ski, ATTR=attr, LANG=lang)
Player_2 = CharGen("Jeronimo", races.Tiefling, classes.Fighter, SKILL=ski, ATTR=attr, LANG=lang, MAGIC=(spelllist_id,'wizard'))
for Player in [ Player_1, Player_2]:
    for el in Player.__dict__:
        print( el,"=", Player.__dict__[el] )
    print("----")
# print(Player_1.name)
# print(Player_1.age)
# Player_1.stats()
# print(Player_1.traits)

# print( Player_1.attr.STR )
