import math

class Skill (dict):
    def __init__ (self, skill, ability, proficient=False, expert=False):
        self[skill] = [ability, proficient, expert]

class SkillSet (dict):

    skill_list = [ [ "Athletics", "STR" ],
                  ["Acrobatics","DEX"],
                  ["Sleight of Hand","DEX"],
                  ["Stealth","DEX"],
                  ["Arcana","INT"],
                  ["History","INT"],
                  ["Investigation","INT"],
                  ["Nature","INT"],
                  ["Religion","INT"],
                  ["Animal Handling","WIS"],
                  ["Insight","WIS"],
                  ["Medicine","WIS"],
                  ["Perception","WIS"],
                  ["Survival","WIS"],
                  ["Deception","CHA"],
                  ["Intimidation","CHA"],
                  ["Performance","CHA"],
                  ["Persuasion","CHA"] ]

    def __init__(self):
        for skill in SkillSet.skill_list:
            self[ skill[0] ] = Skill(skill[0], skill[1])[skill[0]]

    def set_skill(self, skill, prof, exp = False):
        try:
            self[skill][1] = prof
            self[skill][2] = exp
        except KeyError:
            pass

    def add(self, skill):
        self[skill][1] = True

    def remove(self, skill):
        self[skill][1] = False

    def add_exp(self, skill):
        self[skill][2] = True

    def remove_exp(self, skill):
        self[skill][2] = False

class Attribute (int):
    def __init__(self, integer):
        self = integer

    def modifier(self):
        return math.floor((self-10)/2)

class AttrSet (dict):

    attr_list = ["STR", "DEX", "CON", "INT", "WIS", "CHA" ]

    def __init__(self, tAtt = (0,0,0,0,0,0)):
        for i, attr in enumerate( AttrSet.attr_list ):
            self[ attr ] = Attribute(tAtt[i])

    def add(self, attr=None, n=0):
        try:
            self[attr] += n
        except KeyError:
            print( "Wrong keyword argument" )

    @property
    def STR(self):
        return self["STR"]
    @STR.setter
    def STR(self, value):
        self["STR"] = value

    @property
    def DEX(self):
        return self["DEX"]
    @DEX.setter
    def DEX(self, value):
        self["DEX"] = value

    @property
    def CON(self):
        return self["CON"]
    @CON.setter
    def CON(self, value):
        self["CON"] = value

    @property
    def INT(self):
        return self["INT"]
    @INT.setter
    def INT(self, value):
        self["INT"] = value

    @property
    def WIS(self):
        return self["WIS"]
    @WIS.setter
    def WIS(self, value):
        self["WIS"] = value

    @property
    def CHA(self):
        return self["CHA"]
    @CHA.setter
    def CHA(self, value):
        self["CHA"] = value

# ------------- Race  ---------------

class Race():
    def __init__(self, **kwargs):
        super(Race, self).__init__()
        self.mod = AttrSet()
        self.skills = SkillSet()
        self.size = "Medium"
        self.speed = 30
        self.age = 20
        self.align = "NN"
        self.language = ["Common"]
        self.traits = []

    def __iter__ (self):
        return self.__dict__.__iter__()

    def set_input(self,input_list, nlimit, call, **kws):
        """ Sets input like choosing languages or skills """
        if len( input_list ) == nlimit:
            for k in input_list: call(k, **kws)
        else:
            print("Wrong number of options")

# ------------- Human  ---------------

class Human(Race):
    def __init__(self, **kwargs): #, LANG=""):
        super(Human, self).__init__(**kwargs)
        for el in self.mod: self.mod[el] += 1
        self.set_input(kwargs["LANG"] , 1, self.language.append)

# ------------- Dwarf  ---------------

class Dwarf(Race):
    def __init__(self, **kwargs):
        super(Dwarf, self).__init__(**kwargs)
        self.mod.CON += 2
        self.speed = 25
        self.age = 50
        self.align = "LN"
        self.language.append("Dwarvish")
        self.traits.append("Darkvision")
        self.traits.append("Dwarven Resilience")
        self.traits.append("Dwarven Combat Trainig")
        self.traits.append("Tool Proficiency")
        self.traits.append("Stonecunning")

class HillDwarf(Dwarf):
    def __init__(self, **kwargs):
        super(HillDwarf, self).__init__(**kwargs)
        self.mod.WIS += 1
        self.traits.append("Dwarven Toughness")

class MountainDwarf(Dwarf):
    def __init__(self, **kwargs):
        super(MountainDwarf, self).__init__(**kwargs)
        self.mod.STR += 2
        self.traits.append("Dwarven Armor Trainig")

# ------------- Elf  ---------------

class Elf(Race):
    def __init__(self, **kwargs):
        super(Elf, self).__init__(**kwargs)
        self.mod.DEX += 2
        self.speed = 30
        self.age = 100
        self.align = "CN"
        self.language.append("Elvish")
        self.traits.append("Darkvision")
        self.traits.append("Keen Senses")
        # self.skills.add("Perception")
        self.traits.append("Fey Ancestry")
        self.traits.append("Trance")

class HighElf(Elf):
    def __init__(self, **kwargs):
        super(HighElf, self).__init__(**kwargs)
        self.mod.INT += 1
        self.traits.append("Elf Weapon Training")
        self.traits.append("Cantrip")
        self.traits.append("Extra Language")
        self.set_input(kwargs["LANG"] , 1, self.language.append)

class WoodElf(Elf):
    def __init__(self, **kwargs):
        super(WoodElf, self).__init__(**kwargs)
        self.mod.WIS += 1
        self.traits.append("Elf Weapon Training")
        self.traits.append("Fleet of Foot")
        self.speed = 35
        self.traits.append("Mask of the Wild")

class DarkElf(Elf):
    def __init__(self, **kwargs):
        super(DarkElf, self).__init__(**kwargs)
        self.mod.CHA += 1
        self.traits[0] = "Superior Darkvision"
        self.traits.append("Sunlight Sensitivity")
        self.traits.append("Drow Weapon Training")
        self.traits.append("Drow Magic")

# ------------- Halfling ---------------

class Halfling(Race):
    def __init__(self, **kwargs):
        super(Halfling, self).__init__(**kwargs)
        self.mod.DEX += 2
        self.align = "LG"
        self.size = "Small"
        self.speed = 25
        self.traits.append("Lucky")
        self.traits.append("Brave")
        self.traits.append("Halfling Nimbleness")
        self.language.append("Halfling")

class LightfootHalfling(Halfling):
    def __init__(self, **kwargs):
        super(LightfootHalfling, self).__init__(**kwargs)
        self.mod.CHA += 1
        self.traits.append("Naturally Stealthy")

class StoutHalfling(Halfling):
    def __init__(self, **kwargs):
        super(StoutHalfling, self).__init__(**kwargs)
        self.mod.CON += 1
        self.traits.append("Stout Resilience")

# ------------- Dragonborn ---------------

class Dragonborn(Race):
    def __init__(self, **kwargs):
        super(Dragonborn, self).__init__(**kwargs)
        self.mod.STR += 2
        self.mod.CHA += 1
        self.align = "LG"
        self.traits.append("Draconic Ancestry")
        self.traits.append("Breath Weapon")
        self.traits.append("Damage Resistance")
        self.language.append("Draconic")

# ------------- Gnome ---------------

class Gnome(Race):
    def __init__(self, **kwargs):
        super(Gnome, self).__init__(**kwargs)
        self.mod.INT += 2
        self.align = "NG"
        self.size = "Small"
        self.speed = 25
        self.traits.append("Darkvision")
        self.traits.append("Gnome Cunning")
        self.language.append("Gnomish")

class ForestGnome(Gnome):
    def __init__(self, **kwargs):
        super(ForestGnome, self).__init__(**kwargs)
        self.mod.DEX += 1
        self.traits.append("Natural Illusionist")
        self.traits.append("Speak with Small Beasts")

class RockGnome(Gnome):
    def __init__(self, **kwargs):
        super(RockGnome, self).__init__(**kwargs)
        self.mod.CON += 1
        self.traits.append("Artificer's Lore")
        self.traits.append("Tinker")

# ------------- HalfElf ---------------

class HalfElf(Race):

    def __init__(self, **kwargs):
        super(HalfElf, self).__init__(**kwargs)
        self.mod.CHA += 2
        self.align = "CN"
        self.traits.append("Darkvision")
        self.traits.append("Fey Ancestry")
        self.traits.append("Skill Versatility")
        self.language.append("Elvish")

        self.set_input(kwargs["ATTR"] , 2, self.mod.add, n=1)
        self.set_input(kwargs["LANG"] , 1, self.language.append)
        self.set_input(kwargs["SKILL"], 2, self.skills.add)

# ------------- HalfOrc ---------------

class HalfOrc(Race):

    def __init__(self, **kwargs):
        super(HalfOrc, self).__init__(**kwargs)
        self.mod.STR += 2
        self.mod.CON += 1
        self.align = "CN"
        self.traits.append("Darkvision")
        self.traits.append("Menacing")
        self.skills.add("Intimidation")
        self.traits.append("Relentless Endurance")
        self.traits.append("Savage Attacks")
        self.language.append("Orcish")

# ------------- Tiefling ---------------

class Tiefling(Race):

    def __init__(self, **kwargs):
        super(Tiefling, self).__init__(**kwargs)
        self.mod.CHA += 2
        self.mod.INT += 1
        self.align = "CN"
        self.traits.append("Darkvision")
        self.traits.append("Hellish Resistance")
        self.traits.append("Infernal Legacy")
        self.language.append("Infernal")
