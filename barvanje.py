from izrazi_cnf import *
from sat import *

def barvanje_pretvori(g,k):
    '''Funkcija sprejme slovar g, ki podaja graf in število barv k, s katerimi želimo pobarvati naš graf.
    g = {v1:{v3,v5},v2:{v3,v6},v3:{v1,v2,...},...}, za vsako vozlišče je njegova vrednost v slovarju množica vozlišč,
    s katerimi je povezan. Vrne boolov izraz, s pomočjo katerega ugotovimo ali je takšno barvanje mogoče.'''

    def sprem(v,b):
        return Spr(str(v)+","+str(b))
    
    #vsako vozlišče je vsaj ene barve
    f1 = In(*tuple(Ali(*tuple(sprem(v,b) for b in range(k))) for v in g))

    #vsako vozlišče ima kvečjemu eno barvo
    f2 = In(*tuple(In(*tuple(Neg(In(sprem(v,b1),sprem(v,b2))) for b1 in range(k-1) for b2 in range(b1+1,k))) for v in g))
    
    #povezani vozlišči različnih barv
    f3 = In(*tuple(In(*tuple(Neg(In(sprem(v1,b),sprem(v2,b))) for b in range(k))) for v1 in g for v2 in g[v1]))

    formula = In(f1,f2,f3)
    return formula

def barvanje_sat_to_barve(slovar):
    '''Sprejme slovar s ključi (i,j) in vrednostmi ⊤ in ⊥. Ključ (i,j) z vrednostjo ⊤ pove,
    da je vozlišče i pobarvano z barvo j. Funkcija vrne slovar vozlišč z njihovimi barvami.'''

    if slovar == 'Izraz ni rešljiv.': return 'Takšno barvanje grafa ni mogoče.'

    pom = dict()
    for k in slovar.keys():
        if slovar[k] == T():
            s = k.ime.split(',')
            pom[s[0]] = s[1]
    return pom

def barvanje(g,k):
    '''Sprejme slovar g, ki podaja graf in število barv, s katerimi želimo pobarvati naš graf.
    Funkcija vrne slovar vozlišč z njihovimi barvami.'''

    return barvanje_sat_to_barve(sat(barvanje_pretvori(g,k)))


#Nekaj primerov:
g1 = {'a':{'b'},'b':{'a','c'},'c':{'b','d'},'d':{'c','e'},'e':{'d'}}
g2 = {'a':{'b','f'},'b':{'a','c','f'},'c':{'b','d','f'},'d':{'c','e','f'},'e':{'d','f'},'f':{'a','b','c','d','e'}}
g3 = {'a':{'b','f','g'},'b':{'a','c'},'c':{'b','d','g'},'d':{'c','e'},'e':{'d','f','g'},'f':{'a','e','g'},'g':{'a','c','e','f'}}
g4 = {'a':{'b','c'},'b':{'a','e','f'},'c':{'a','d'},'d':{'c'},'e':{'b'},'f':{'b'}}
g5 = {1:{2,6,7},2:{1,7,5,3},3:{2,4},4:{3,5,6},5:{2,4,6},6:{1,5,4},7:{1,2}}
g6 = {1:{2,3,4,5,6},2:{1,3,4,5,6},3:{1,2,4,5,6},4:{1,2,3,5,6},5:{1,2,3,4,6},6:{1,2,3,4,5}} #poln graf

petersen = {1:{2,5,6},2:{1,3,7},3:{2,4,8},4:{3,5,9},5:{4,1,10},6:{1,8,9},7:{2,9,10},8:{3,10,1},9:{4,1,2},10:{5,2,3}}
