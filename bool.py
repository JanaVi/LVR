class T():
    def __init__(self):
        pass

    def __repr__(self):
        return "⊤"

    def __eq__(self,other):
        return type(other)==T

    def __hash__(self):
        return hash(repr(self))

    def vrednost(self,slo):
        return True

    def poenostavi(self):
        return self

    def nnf(self):
        return self

    def cnf(self):
        return self

###################################################
class F():
    def __init__(self):
        pass

    def __repr__(self):
        return "⊥"
    
    def __eq__(self,other):
        return type(other)==F

    def __hash__(self):
        return hash(repr(self))

    def vrednost(self,slo):
        return False

    def poenostavi(self):
        return self

    def nnf(self):
        return self

    def cnf(self):
        return self

###################################################
class Spr():
    def __init__(self,ime):
        self.ime=ime

    def __repr__(self):
        return str(self.ime)

    def __eq__(self,other):
        if type(other)==Spr:
            return self.ime==other.ime
        else:
            return False

    def __hash__(self):
        return hash(repr(self))

    def vrednost(self,slo):
        return slo[self.ime]

    def poenostavi(self):
        return self

    def nnf(self):
        return self

    def cnf(self):
        return self
    
######################################################
class Neg():
    def __init__(self,izr):
        self.izr = izr

    def __repr__(self):
        if type(self.izr)!=Ali and type(self.izr)!=In:
            return "¬"+repr(self.izr)
        else:
            return "¬("+repr(self.izr)+")"

    def __eq__(self,other):
        if type(other) == Neg:
            return self.izr==other.izr
        else:
            return False
    
    def __hash__(self):
        return hash(repr(self))

    def vrednost(self,slo):
        return not self.izr.vrednost(slo)

    def poenostavi(self):
        a = self.izr.poenostavi()
        tip = type(a)
        if tip == T:
            return F()
        elif tip == F:
            return T()
        elif tip == Spr:
            return Neg(a)
        elif tip == Neg:
            return a.izr
        elif tip == In:
            return Ali(*tuple(Neg(i) for i in a.sez)).poenostavi()
        elif tip == Ali:
            return In(*tuple(Neg(i) for i in a.sez)).poenostavi()

    def nnf(self): #negacije spravi notri do konca
        a = self.izr
        tip = type(a)
        if tip == T:
            return F()
        elif tip == F:
            return T()
        elif tip == Spr:
            return Neg(a)
        elif tip == Neg:
            return a.izr
        elif tip == In:
            return Ali(*tuple(Neg(i).nnf() for i in a.sez))
        elif tip == Ali:
            return In(*tuple(Neg(i).nnf() for i in a.sez))

    def cnf(self): #že imamo nnf, torej je negacija lahko samo pri spremenljivki
        return Neg(self.izr)

#####################################################
class In():
    def __init__(self,*args):
        self.sez=set(args)

    def __repr__(self):
        niz=""
        for i in self.sez:
            if type(i)!=In and type(i)!=Ali:
                niz+=" ∧ "+repr(i)
            else:
                niz+=" ∧ ("+repr(i)+")"

        return niz[3:]

    def __eq__(self,other):
        if type(other)==In:
            return self.sez==other.sez
        else:
            return False
    
    def __hash__(self):
        return hash(repr(self))

    def vrednost(self,slo):
        a=True
        for i in self.sez:
            a= a and i.vrednost(slo)
            if a==False:
                return a
        return a

    def nnf(self):
        if len(self.sez)==0: return T()
        elif len(self.sez)==1: return self.sez.pop().nnf()
        return In(*tuple(i.nnf() for i in self.sez))

    def cnf(self):
        return In(*tuple(i.cnf() for i in self.sez))
        
    def poenostavi(self):
        if len(self.sez)==0: return T()
        elif len(self.sez)==1: return self.sez.pop().poenostavi()
        slo = {}
        for i in self.sez:
            i=i.poenostavi()
            if type(i)==F: return F()
            elif type(i)==T: pass
            elif type(i) in slo:
                slo[type(i)].add(i)
            else:
                slo[type(i)]={i}

        #complementary law
        if Neg in slo.keys():
            for i in slo[Neg]:
                for j in slo.values():
                    if i.izr in j:
                        return F()

        #absorpcija in common identities
        if Ali in slo.keys():
            menjave={}
            for i in slo[Ali]:
                for j in slo.values():
                    for k in j:
                        if k in i.sez:
                            menjave[i]=0
                        elif Neg(k) in i.sez:
                            menjave[i]=i.sez-{Neg(k)}
            slo[Ali]={(Ali(*tuple(menjave[i])) if menjave[i]!=0 else None ).poenostavi() if i in menjave else i for i in slo[Ali]} - {None}

        #distributivnost
            if len(slo[Ali])>1:
                presek = 42
                for i in slo[Ali]:
                    if presek==42:
                        presek={j for j in i.sez}
                    else:
                        presek&=i.sez
                if presek:
                    slo[Ali]={Ali(
                        In(*tuple(set().union(*tuple(i.sez-presek for i in slo[Ali])))),
                        *tuple(presek)
                        )}
                
                
                
        

        #če imaš In znotraj In, ju lahko združiš
        if In in slo.keys():
            for j in slo[In]:
                for i in j.sez:
                    if type(i) in slo: slo[type(i)].add(i)
                    else: slo[type(i)]={i}
      
            del slo[In]

        #sestavi poenostavljen izraz
        mn=set()
        for i in slo.values():
            mn|=i
        return In(*tuple(mn))
    
        
########################################################
class Ali():
    def __init__(self,*args):
        self.sez=set(args)

    def __repr__(self):
        niz=""
        for i in self.sez:
            if type(i)!=Ali and type(i)!=In:
                niz+=" ∨ "+repr(i)
            else:
                niz+=" ∨ ("+repr(i)+")"

        return niz[3:]

    def __eq__(self,other):
        if type(other)==Ali:
            return self.sez==other.sez
        else:
            return None

    def __hash__(self):
        return hash(repr(self))

    def vrednost(self,slo):
        a=False
        for i in self.sez:
            a= a or i.vrednost(slo)
            if a==True:
                return a
        return a

    def nnf(self):
        if len(self.sez)==0: return F()
        elif len(self.sez)==1: return self.sez.pop().nnf()
        return Ali(*tuple(i.nnf() for i in self.sez))

    def cnf(self):
        seznam = [i.cnf() for i in self.sez]
        n = len(seznam)
        nova = seznam[0]
        #distribucija:
        for i in range(1,n):
            if (type(nova) == Spr or type(nova) == Neg) and (type(seznam[i]) == Spr or type(seznam[i]) == Neg):
                nova = Ali(nova,seznam[i])
            elif type(nova) == Spr or type(nova) == Neg:
                nova = In(*tuple(Ali(nova,j) for j in seznam[i].sez))
            elif type(seznam[i]) == Spr or type(seznam[i]) == Neg:
                nova = In(*tuple(Ali(k,seznam[i]) for k in nova.sez))
            else: nova = In(*tuple(Ali(k,j) for j in seznam[i].sez for k in nova.sez))
        return nova

    def poenostavi(self):
        if len(self.sez)==0: return F()
        elif len(self.sez)==1: return self.sez.pop().poenostavi()
        slo = {}
        for i in self.sez:
            i=i.poenostavi()
            if type(i)==T: return T()
            elif type(i)==F: pass
            elif type(i) in slo:
                slo[type(i)].add(i)
            else:
                slo[type(i)]={i}
        
        #complementary law
        if Neg in slo.keys():
            for i in slo[Neg]:
                for j in slo.values():
                    if i.izr in j:
                        return T()

        #absorpcija in common identities in distributivnost
        if In in slo.keys():
            menjave={}
            for i in slo[In]:
                for j in slo.values():
                    for k in j:
                        if k in i.sez: #absorpcija
                            menjave[i]=0
                        elif Neg(k) in i.sez: #common id
                            menjave[i]=i.sez-{Neg(k)}
            slo[In]={(In(*tuple(menjave[i])) if menjave[i]!=0 else None ).poenostavi() if i in menjave else i for i in slo[In]} - {None}
        
            #distributivnost
            if len(slo[In])>1:
                presek = 42
                for i in slo[In]:
                    if presek==42:
                        presek={j for j in i.sez}
                    else:
                        presek&=i.sez
                if presek:
                    slo[In]={In(
                        Ali(*tuple(set().union(*tuple(i.sez-presek for i in slo[In])))),
                        *tuple(presek)
                        )}

                
       
        if Ali in slo.keys():
            for j in slo[Ali]:
                for i in j.sez:
                    if type(i) in slo: slo[type(i)].add(i)
                    else: slo[type(i)]={i}
      
            del slo[Ali]

        mn=set()
        for i in slo.values():
            mn|=i
        return Ali(*tuple(mn))



######################## Primeri za cnf ##########################################################################
p = Spr("p")
q = Spr("q")
r = Spr("r")

primer1 = Ali(p,In(q,p))

primer2 = In(p,Ali(q,Neg(p)))

primer3 = In(Ali(p,q),Ali(p,r))

primer4 = In(In(p,q),In(q,r),In(r,p))

primer5 = In(Ali(p,q),Ali(q,r),Ali(r,p),Neg(In(p,q)),Neg(In(q,r)),Neg(In(r,p)))

primer6 = Ali(In(Spr('p'),Spr('r'),Spr('q')),In(Spr('a'),Spr('b'),Spr('c')))

primer7 = In(Ali(In(Spr('p'),Spr('r'),Spr('q')),In(Spr('a'),Spr('b'),Spr('c'))),Spr('K'))

##################################### Primeri za SAT ############################################################

def SATprimer(niz,n):
    '''Funkcija sprejme niz:
    enostavenIN
    enostavenALI
    povezanostJA1
    povezanostJA2
    in dolžino formule.'''
    if niz == 'enostavenIN':
        return In(*tuple('a'+str(i) for i in range(n)))
    elif niz == 'enostavenALI':
        return Ali(*tuple('a'+str(i) for i in range(n)))
    elif niz == 'povezanostJA1':
        return povezanost({'a': {'b'},'b':{'a','c'},'c':{'b','d'},'d':{'c','e'},'e':{'d'}})
    elif niz == 'povezanostJA2':
        return povezanost({'a':{'b','c'},'b':{'a','e','f'},'c':{'a','d'},'d':{'c'},'e':{'b'},'f':{'b'}})
    elif niz == 'povezanostNE1':
        return povezanost({'a':{'c'},'b':{'e','f'},'c':{'a','d'},'d':{'c'},'e':{'b'},'f':{'b'}})
    elif niz =='povezanostNE2':
        return povezanost({'a':{'b'},'b':{'a'},'c':{'d'},'d':{'c'}})
    
    
  


    


###################### VAJE ŠTEVILKA 2, 3 ########################################################################


def barvanje(g,k):
    """Ali lahko graf podan s slovarjem g pobarvamo s k barvami? """
    def sprem(v,b):
        return Spr(str(v)+","+str(b))
    
    #vsako vozlišče vsaj ene barve
    f1 = In(*tuple(Ali(*tuple(sprem(v,b) for b in range(k))) for v in g))

    #vsako vozlišče z ne več kot eno barvo
    f2 = In(
        *tuple(
            In(
                *tuple(
                    Neg(In(sprem(v,b1),sprem(v,b2)))
                    for b1 in range(k-1)
                    for b2 in range(b1+1,k))
                )
            for v in g))
    
    #povezani vozlišči različnih barv
    f3 = In(
        *tuple(
            In(
                *tuple(
                    Neg(In(sprem(v1,b),sprem(v2,b)))
                    for b in range(k)
                    )
                )
            for v1 in g for v2 in g[v1]))

    formula = In(f1,f2,f3)

    return formula.poenostavi()

g = {"a":{"d"},"b":{"d"},"c":{"d"},"d":{"a","b","c"}}


def povezanost(g):
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
    f4 = In(
        *tuple(
            Ali(
                *tuple(
                    Ali(Neg(sprem(u,v,i)),sprem(k,v,i-1))
                        for k in g[u] for i in range(2,n)
                    )
                )

                for u in g for v in g.keys()-{u}

            )
        )
    

    return In(f1,f2,f3,f4)

            
        
            



