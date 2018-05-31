import random
import numpy as np
from matplotlib import pyplot as plt

def ed2cen(ed):
    cen = .5*(ed[1:]+ed[:-1])
    return cen

def roll_w_dis():
    a=random.randint(1,20)
    b=random.randint(1,20)
    return min(a,b)

def roll_w_adv():
    a=random.randint(1,20)
    b=random.randint(1,20)
    return max(a,b)

def roll(n,dice):
    a = []
    for i in range(n):
        a.append(random.randint(1,dice))
    return a

def keep(m,seq):
    for i in range(len(seq)-m):
        seq.pop(seq.index(min(seq)))
    return seq
