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

    def cnf(self):
        return self

###################################################
class Spr():
    def __init__(self,ime):
        self.ime = ime

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

    def cnf(self):
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
            return Ali(*tuple(Neg(i) for i in a.sez)).cnf()
        elif tip == Ali:
            return In(*tuple(Neg(i) for i in a.sez)).cnf()

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

    def bistvo(self): #In(Spr(p)) spremeni v Spr(p)
        if len(self.sez) == 1: return self.sez.pop()
        else: return self

    def cnf(self):
        if len(self.sez)==0: return T()
        elif len(self.sez)==1: return self.sez.pop().cnf()

        #law of union, law of intersection, complementary law:
        smiselni = set()
        for i in self.sez:
            i = i.cnf()
            if type(i) == F: return F()
            elif type(i) == T: pass
            elif (type(i) == Spr and Neg(i) in smiselni) or (type(i) == Neg and i.izr in smiselni): return F()
            elif type(i) == Spr or type(i) == Neg: smiselni.add(i)
            elif type(i) == In: #če imaš In v In, ju združi
                for j in i.sez:
                    if (type(j) == Spr and Neg(j) in smiselni) or (type(j) == Neg and j.izr in smiselni): return F()
                    else: smiselni.add(j)                
            else: smiselni.add(i) #vsi ostali kompleksni izrazi
        a = In(*tuple(i for i in smiselni))
        if len(a.sez) !=0: return a
        else: return T()

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

    def bistvo(self):
        if len(self.sez) == 1: return self.sez.pop()
        else: return self

    def cnf(self):
        if len(self.sez)==0: return F()
        elif len(self.sez)==1: return self.sez.pop().cnf()

        #law of union, law of intersection, complementary law:
        smiselni = set()
        for i in self.sez:
            i = i.cnf()
            if type(i) == F: pass
            elif type(i) == T: return T()
            elif type(i) == Spr and Neg(i) in smiselni: smiselni.remove(Neg(i))
            elif type(i) == Neg and i.izr in smiselni: smiselni.remove(i.izr)
            elif type(i) == Spr or type(i) == Neg: smiselni.add(i)
            elif type(i) == Ali: #če imaš Ali v Ali, ju združi
                for j in i.sez:
                    if type(j) == Spr and Neg(j) in smiselni: smiselni.remove(Neg(j))
                    elif type(j) == Neg and j.izr in smiselni: smiselni.remove(j.izr)
                    else: smiselni.add(j)                
            else: smiselni.add(i) #vsi ostali kompleksni izrazi
        a = Ali(*tuple(i for i in smiselni))
        
        if len(a.sez) == 0: return F()

        seznam = [i for i in a.sez]
        n = len(seznam)
        nova = seznam[0] #do sedaj že narejen izraz, postopoma distributiramo





        
        #distributivnost:############################################
        for i in range(1,n):
            if (type(nova) == Spr or type(nova) == Neg) and (type(seznam[i]) == Spr or type(seznam[i]) == Neg):
                nova = Ali(nova,seznam[i]).bistvo()

            elif (type(nova) == Ali and (type(seznam[i]) == Spr or type(seznam[i]) == Neg):
                nova.sez.add(seznam[i])
                
            elif type(nova) == Spr or type(nova) == Neg:
                nova = In(*tuple(Ali(nova,j).bistvo() for j in seznam[i].sez))

            elif type(seznam[i]) == Spr or type(seznam[i]) == Neg:
                nova = In(*tuple(Ali(k,seznam[i]).bistvo() for k in nova.sez))
                
            else: nova = In(*tuple(Ali(k,j).bistvo() for j in seznam[i].sez for k in nova.sez))
        return nova.bistvo()







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

primer7 = In(Ali(In(Spr('p'),Spr('r'),Spr('q')),In(Spr('a'),Spr('b'),Spr('c'))),F())

primer8 = In(Ali(In(Spr('p'),Spr('r'),Spr('q')),In(Spr('a'),Spr('b'),Spr('c'))),Spr('K'))


p1=In(T(),F(),Ali(p,Neg(p)))
p2=Ali(Neg(In(p,r,q,)))
p3=In(T(),In(p,Neg(p)))

##################################### Primeri za SAT ############################################################
a1=Spr('a1')
a2=Spr('a2')
a3=Spr('a3')
a4=Spr('a4')
a5=Spr('a5')
a6=Spr('a6')



def SATprimer(niz,n):
    '''Funkcija sprejme niz:
    enostavenIN
    enostavenALI
    povezanostJA1
    povezanostJA2
    enostavenJA
    enostavenNE
    in dolžino formule za enostavne primere.'''
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
    elif niz == 'enostavenJA':
        return Ali(In(a1,(Ali(Ali(a2,a4),In(a5,a6)))),(In(a3,Ali(a4,a1))),a5)
    elif niz == 'enostavenNE':
        return Ali(In(a1,(Ali(Ali(a2,a4),In(a5,a6)))),(In(a3,Ali(a4,a6))),a5)    


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

            
############ SAT #############################

def sat(izraz):
    izraz = izraz.cnf() #sedaj je izraz v konjuktivni obliki
    
    if izraz == T(): return True
    elif izraz == F(): return False
    
##    elif len(izraz.sez) == 0 and type(izraz) == In: return True #če ni stavkov
##    elif len(izraz.sez) == 0 and type(izraz) == Ali: return False

    print('cnf oblika=',izraz)
    literal = dict() #slovar vseh spremenljivk, skupaj z očitnimi znanimi vrednostmi
    stavki = [i for i in izraz.sez] #stavki, ki jih je še potrebno predelati
    print('začetni stavki=',stavki)


    #######tega se želimo znebiti že v cnf!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! zaenkrat notri zaradi pravilnosti
    for i in izraz.sez: #če je kakšen stavek F()
        if type(i) == F: return False

        
    for i in izraz.sez: 
        if type(i) == Spr: #samostojna spremenljivka
            stavki.remove(i)
            print('preostali stavki=',stavki)
            literal[i.ime] = True
            stavki2=stavki #nadomestna kopija preostalih stavkov
            
            for stavek in stavki2:
                if type(stavek) == Spr and stavek==i: stavki.remove(stavek)
                elif type(stavek) == Neg and stavek.izr==i: return False
                elif type(stavek) == Ali and len(stavek.sez)>1:
                    for lit in stavek.sez:
                        if type(lit) == Spr and lit == i:
                            stavki.remove(stavek)
                        if type(lit) == Neg and lit.izr == i:
                            stavki.remove(stavek)
                            stavki.append(Ali(*tuple(a for a in stavek if a!=Neg(i)))) #odstrani stari stavek in ga nadomesti z novim, ki nima negacij naše spremenljivke  
                else: print('Napaka pri vstavljanju znanih spr. v preostale stavke 1.')
                
            
        elif type(i) == Neg: #samostojna negirana spremenljivka
            stavki.remove(i)
            print('preostali stavki=',stavki)
            literal[i.izr.ime] = False
            stavki2=stavki #nadomestna kopija preostalih stavkov
            
            for stavek in stavki2:
                if type(stavek) == Spr and stavek==i.izr: return False                
                elif type(stavek) == Neg and stavek.izr==i.izr: stavki.remove(stavek)

                
                elif type(stavek) == Ali and len(stavek.sez)>1:
                    for lit in stavek.sez:
                        if type(lit) == Spr and lit == i.izr:
                            stavki.remove(stavek)
                            stavki.append(Ali(*tuple(a for a in stavek if a!=i.izr))) #odstrani stari stavek in ga nadomesti z novim, ki nima negacij naše spremenljivke  
                        if type(lit) == Neg and lit.izr == i.izr:
                            stavki.remove(stavek)
                else: print('Napaka pri vstavljanju znanih spr. v preostale stavke 2.')
            

        else:
            for j in i.sez:
                if type(j) == Spr: literal[j.ime] = ''
                elif type(j) == Neg: literal[j.izr.ime] = ''                
                else: print('NAPAKA!')
                
    
    znane = {i: literal[i] for i in literal if literal[i]!=''}
    neznane = {i: literal[i] for i in literal if literal[i]==''}
    
    return literal


def element(s): #vrne edini element v množici in ga pusti notri
    return list(s)[0]
    


































    
            



