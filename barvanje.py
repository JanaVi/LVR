from izrazi_cnf import *
from sat import *
from primeri import *

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

