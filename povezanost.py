from izrazi_cnf import *

def povezanost(g):
    '''Funkcija sprejme slovar g, ki podaja graf in vrne boolov izraz, s pomočjo katerega ugotovimo ali je dani graf povezan.'''

    def sprem(u,v,n):
        return Spr("C{0}{1}{2}".format(u,v,n))

    n = len(g)

    #sosedi so povezani
    f1 = In(*tuple(sprem(u,v,1) if v in g[u] else Neg(sprem(u,v,1)) for u in g for v in g.keys()))

    #povezanost
    f3 = In(*tuple(Ali(*tuple(sprem(u,v,i) for i in range(1,n))) for u in g for v in g.keys()-{u}))

    # če u in v povezana in iz v do k v n korakih, potem iz u do k v n+1 korakih
    f2 = In(*tuple(Ali(Neg(sprem(v,k,i)),sprem(u,k,i+1)) for u in g for v in g[u] for k in g.keys()-{u,v} for i in range(1,n)))

    # če iz u do v v n korakih, potem iz nekega soseda od u do v v n-1 korakih
    f4 = In(*tuple(Ali(*tuple(Ali(Neg(sprem(u,v,i)),sprem(k,v,i-1)) for k in g[u] for i in range(2,n))) for u in g for v in g.keys()-{u}))
    

    return In(f1,f2,f3,f4)


g = {"a":{"d"},"b":{"d"},"c":{"d"},"d":{"a","b","c"}}
