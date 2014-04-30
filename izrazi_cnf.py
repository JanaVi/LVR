import copy

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

    def bistvo(self):
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

    def bistvo(self):
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

    def bistvo(self):
        return self

    
###################################################
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

    def bistvo(self):
        return self


###################################################
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
            a = a and i.vrednost(slo)
            if a==False:
                return a
        return a

    def bistvo(self): #In(Spr(p)) spremeni v Spr(p); In(a,..,Neg(a)) spremeni v F(); 
        if len(self.sez)==0: return T()
        vsebina = set()
        for i in self.sez:
            if type(i) == F: return F()
            elif type(i) == T: pass
            elif (type(i) == Spr and Neg(i) in vsebina) or (type(i) == Neg and i.izr in vsebina): return F()
            else: vsebina.add(i)
        if len(vsebina) == 1: return vsebina.pop()
        else: return In(*tuple(i for i in vsebina))

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
        return a.bistvo()

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
    
        
###################################################
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
        if len(self.sez)==0: return F()
        vsebina = set()
        for i in self.sez:
            if type(i) == F: pass
            elif type(i) == T: return T()
            elif type(i) == Spr and Neg(i) in vsebina: return T()
            elif type(i) == Neg and i.izr in vsebina: return T()
            elif type(i) == Spr or type(i) == Neg: vsebina.add(i)
        if len(vsebina) == 1: return vsebina.pop()
        else: return Ali(*tuple(i for i in vsebina))

    def cnf(self):
        if len(self.sez)==0: return F()
        elif len(self.sez)==1: return self.sez.pop().cnf()

        #law of union, law of intersection, complementary law:
        smiselni = set()
        for i in self.sez:
            i = i.cnf()
            if type(i) == F: pass
            elif type(i) == T: return T()
            elif type(i) == Spr and Neg(i) in smiselni: return T()
            elif type(i) == Neg and i.izr in smiselni: return T()
            elif type(i) == Spr or type(i) == Neg: smiselni.add(i)
            elif type(i) == Ali: #če imaš Ali v Ali, ju združi
                for j in i.sez:
                    if type(j) == Spr and Neg(j) in smiselni: return T()
                    elif type(j) == Neg and j.izr in smiselni: return T()
                    else: smiselni.add(j)                
            else: smiselni.add(i) #vsi ostali kompleksni izrazi

        if len(smiselni) == 0: return F()
        elif len(smiselni) == 1: return smiselni.pop()
       
        seznam = list(smiselni)
        n = len(seznam)
        nova = seznam[0] #do sedaj že narejen izraz, postopoma distributiramo
        #distributivnost:      (katastrofalno napisano, ampak pravilno deluje; bom popravila, če utegnem)
        for i in range(1,n):
            naslednja = seznam[i]

            if type(nova) == T: return T()

            elif (type(nova) == Spr or type(nova) == Neg) and (type(naslednja) == Spr or type(naslednja) == Neg):
                nova = Ali(nova,naslednja).bistvo()
            elif (type(nova) == Spr or type(nova) == Neg) and type(naslednja) == In:
                sez = set()
                for m in naslednja.sez:
                    if type(m) == Spr or type(m) == Neg:
                        stavek = Ali(nova,m).bistvo()
                        if not type(stavek) == T: sez.add(stavek)
                    elif type(m) == Ali:
                        m.sez.add(nova)
                        m = m.bistvo()
                        if not type(m) == T: sez.add(m)
                    else: print('napaka pri distr.!')
                nova = In(*tuple(k for k in sez)).bistvo()
            elif type(naslednja) == Ali and (type(nova) == Spr or type(nova) == Neg):
                naslednja.sez.add(nova)
                naslednja = naslednja.bistvo()
                nova = naslednja
                

            elif type(nova) == Ali and (type(naslednja) == Spr or type(naslednja) == Neg):
                nova.sez.add(naslednja)
                nova = nova.bistvo()
            elif type(nova) == Ali and type(naslednja) == Ali:
                nova.sez.add(k for k in naslednja.sez)
                nova = nova.bistvo()
            elif type(nova) == Ali: #naslednja je tipa In                
                sez = set()
                for m in naslednja.sez:
                    if type(m) == Spr or type(m) == Neg:
                        mn = nova.sez.union({m})
                        izraz = Ali(*tuple(i for i in mn)).bistvo()
                        if not type(izraz) == T: sez.add(izraz)
                    elif type(m) == Ali:
                        mn = nova.sez.union(m.sez)
                        izraz = Ali(*tuple(i for i in mn)).bistvo()
                        if not type(izraz) == T: sez.add(izraz)
                    else: print('napaka pri distr.!')
                nova = In(*tuple(k for k in sez)).bistvo()

                
            elif (type(naslednja) == Spr or type(naslednja) == Neg) and type(nova) == In:
                sez = set()
                for m in nova.sez:
                    if type(m) == Spr or type(m) == Neg:
                        stavek = Ali(naslednja,m).bistvo()
                        if not type(stavek) == T: sez.add(stavek)
                    elif type(m) == Ali:
                        m.sez.add(naslednja)
                        m = m.bistvo()
                        if not type(m) == T: sez.add(m)
                    else: print('napaka pri distr.! 2')
                nova = In(*tuple(k for k in sez)).bistvo()             
            elif type(nova) == In and type(naslednja) == Ali:
                sez = set()
                for m in nova.sez:
                    if type(m) == Spr or type(m) == Neg:
                        mn = naslednja.sez.union({m})
                        izraz = Ali(*tuple(i for i in mn)).bistvo()
                        if not type(izraz) == T: sez.add(izraz)
                    elif type(m) == Ali:
                        mn = naslednja.sez.union(m.sez)
                        izraz = Ali(*tuple(i for i in mn)).bistvo()
                        if not type(izraz) == T: sez.add(izraz)
                    else: print('napaka pri distr.!')
                nova = In(*tuple(k for k in sez)).bistvo()             
            else: #In ali In
                sez = set()
                for m in nova.sez:
                    for n in naslednja.sez:
                        zacasen = set()
                        if type(m) == Ali: zacasen = zacasen.union(m.sez)
                        else: zacasen.add(m)
                        if type(n) == Ali: zacasen = zacasen.union(n.sez)
                        else: zacasen.add(n)
                        stavek = Ali(*tuple(k for k in zacasen)).bistvo()
                        if not type(stavek) == T: sez.add(stavek)
                nova = In(*tuple(k for k in sez)).bistvo()
                
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
