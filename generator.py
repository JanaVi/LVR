import random
from izrazi_cnf import *

def generiraj(n = 10, k = 20):
    '''Funkcija nam vrne izraz v cnf obliki, ki vsebuje največ n različnih
    spremenljivk in ima dolžino k.'''
    
    if n == 0 or k == 0: return T()
    
    izraz = In()
    sez = []
    for i in range(k):
        lit = random.randint(1,n)
        sez.append(Spr('{0}'.format(lit)) if random.randint(0,1) == 1 else Neg(Spr('{0}'.format(lit))))
    st = random.randint(1,k) #število stavkov
    pozicija = random.sample(range(k-1),st-1) #pozicija In-ov med stavki
    pozicija.sort()

    start = 0
    stavki = []
    for i in pozicija:
        stavki.append(Ali(*tuple(s for s in sez[start:i+1])).bistvo())
        start = i + 1

    stavki.append(Ali(*tuple(s for s in sez[start:])).bistvo())
    izraz = In(*tuple(i for i in stavki)).bistvo()
    return izraz
    
