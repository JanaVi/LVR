from izrazi_cnf import *

def barvanje(g,k):
    '''Funkcija sprejme slovar g, ki podaja graf in število barv k, s katerimi želimo pobarvati naš graf.
    Vrne boolov izraz, s pomočjo katerega ugotovimo ali je takšno barvanje mogoče.'''
    
    def sprem(v,b):
        return Spr(str(v)+","+str(b))
    
    #vsako vozlišče je vsaj ene barve
    f1 = In(*tuple(Ali(*tuple(sprem(v,b) for b in range(k))) for v in g))

    #vsako vozlišče ima kvečjemu eno barvo
    f2 = In(*tuple(In(*tuple(Neg(In(sprem(v,b1),sprem(v,b2))) for b1 in range(k-1) for b2 in range(b1+1,k))) for v in g))
    
    #povezani vozlišči različnih barv
    f3 = In(*tuple(In(*tuple(Neg(In(sprem(v1,b),sprem(v2,b))) for b in range(k))) for v1 in g for v2 in g[v1]))

    formula = In(f1,f2,f3)

    return formula.poenostavi()
