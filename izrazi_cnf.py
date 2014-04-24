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
        if len(a.sez) !=0: return a.bistvo()
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

        #distributivnost:############################################katastrofa!!!!!!!!!!!!!!!!!!!!ampak deluje
        for i in range(1,n):
            if (type(nova) == Spr or type(nova) == Neg) and (type(seznam[i]) == Spr or type(seznam[i]) == Neg):
                nova = Ali(nova,seznam[i]).bistvo()
            elif (type(nova) == Spr or type(nova) == Neg) and type(seznam[i]) == In:
                sez=set()
                mn={m for m in seznam[i].sez}
                for m in mn:
                    if type(m) == Spr or type(m) == Neg:
                        sez.add(Ali(nova,m).bistvo())
                    elif type(m) == Ali:
                        for s in m:
                            sez.add(Ali(nova,s).bistvo())
                    else: print('napaka pri distr.!')
                nova = In(*tuple(k for k in sez))
            elif type(seznam[i]) == Ali and (type(nova) == Spr or type(nova) == Neg):
                nova.sez.add(k for k in seznam[i].sez)


            elif type(nova) == Ali and (type(seznam[i]) == Spr or type(seznam[i]) == Neg):
                nova.sez.add(seznam[i])
            elif type(nova) == Ali and type(seznam[i]) == Ali:
                nova.sez.add(k for k in seznam[i].sez)
            elif type(nova) == Ali: #seznam[i] je tipa In
                nova_sez = [k for k in nova.sez]
                sez=set()
                mn={m for m in seznam[i].sez}
                for m in mn:
                    zacasen_seznam = nova_sez
                    if type(m) == Spr or type(m) == Neg:
                          zacasen_seznam.append(m)
                          sez.add(Ali(*tuple(k for k in zacasen_seznam)).bistvo())
                    elif type(m) == Ali:
                        for s in m:
                              zacasen_seznam.append(s)
                        sez.add(Ali(*tuple(k for k in zacasen_seznam)).bistvo())
                    else: print('napaka pri distr.!')
                nova = In(*tuple(k for k in sez))

                
            elif (type(seznam[i]) == Spr or type(seznam[i]) == Neg) and type(nova) == In:
                sez=set()
                mn={m for m in nova.sez}
                for m in mn:
                    if type(m) == Spr or type(m) == Neg:
                        sez.add(Ali(seznam[i],m).bistvo())
                    elif type(m) == Ali:
                        for s in m:
                            sez.add(Ali(seznam[i],s).bistvo())
                    else: print('napaka pri distr.! 2')
                nova = In(*tuple(k for k in sez))              
            elif type(nova) == In and type(seznam[i]) == Ali:
                nova_sez = [k for k in seznam[i].sez]
                sez=set()
                mn={m for m in nova.sez}
                for m in mn:
                    zacasen_seznam = nova_sez
                    if type(m) == Spr or type(m) == Neg:
                          zacasen_seznam.append(m)
                          sez.add(Ali(*tuple(k for k in zacasen_seznam)).bistvo())
                    elif type(m) == Ali:
                        for s in m:
                              zacasen_seznam.append(s)
                        sez.add(Ali(*tuple(k for k in zacasen_seznam)).bistvo())
                    else: print('napaka pri distr.!')
                nova = In(*tuple(k for k in sez))               
            else: #In ali In
                sez = set()
                for m in nova.sez:
                   for n in seznam[i].sez:
                      zacasen = []
                      zacasen.append(k for k in m.sez) if type(m) == Ali else zacasen.append(m)
                      zacasen.append(k for k in n.sez) if type(n) == Ali else zacasen.append(n)
                      sez.add(Ali(*tuple(k for k in zacasen))) 
                nova = In(*tuple(k for k in sez))
                
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
