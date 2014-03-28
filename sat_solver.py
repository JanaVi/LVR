from izrazi_cnf import *

############ SAT #############################


def sat(izraz):
    izraz = izraz.cnf() #sedaj je izraz v konjuktivni obliki
    print('cnf oblika=',izraz)
    
    if izraz == T(): return True
    elif izraz == F(): return False

    literal = dict() #slovar vseh spremenljivk, skupaj z očitnimi znanimi vrednostmi
    stavki = [i for i in izraz.sez] #stavki, ki jih je še potrebno predelati
    print('začetni stavki=',stavki)



    while stavki: #dokler še imamo kakšen stavek

        for i in izraz.sez: 
            if type(i) == Spr: #samostojna spremenljivka
                stavki.remove(i)
                print('preostali stavki=',stavki)
                literal[i.ime] = T()
                stavki2=stavki #nadomestna kopija preostalih stavkov
                
                for stavek in stavki2:
                    if type(stavek) == Neg and stavek.izr==i: return F()
                    elif type(stavek) == Spr and stavek == i: stavki.remove(stavek)
                    elif type(stavek) == Ali :
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
                literal[i.izr.ime] = F()
                stavki2=stavki #nadomestna kopija preostalih stavkov
                
                for stavek in stavki2:
                    if type(stavek) == Spr and stavek==i.izr: return F()                
                    elif type(stavek) == Neg and stavek.izr==i.izr: stavki.remove(stavek)
                    elif type(stavek) == Ali:
                        for lit in stavek.sez:
                            if type(lit) == Spr and lit == i.izr:
                                stavki.remove(stavek)
                                stavki.append(Ali(*tuple(a for a in stavek if a!=i.izr))) #odstrani stari stavek in ga nadomesti z novim, ki nima negacij naše spremenljivke  
                            if type(lit) == Neg and lit.izr == i.izr:
                                stavki.remove(stavek)
                    else: print('Napaka pri vstavljanju znanih spr. v preostale stavke 2.')      

            else: #stavek
                for j in i.sez:
                    if type(j) == Spr: literal[j.ime] = ''
                    elif type(j) == Neg: literal[j.izr.ime] = ''                
                    else: print('NAPAKA!')
                
    
            znane = {i: literal[i] for i in literal if literal[i]!=''}
            neznane = {i: literal[i] for i in literal if literal[i]==''}

            for i in [F(),T()]:
                trenutna = list(neznane.keys())[0]
                znane[trenutna] = i
                del neznane[trenutna]
                
                #gremo po vseh stavkih in vstavljamo vrednost za našo trenutno spr.
                for stavek in stavki:
                    if trenutna in stavek.sez:
                        if trenutna == T():
                            stavki.remove(stavek)
                        else:
                            stavki.remove(stavek)
                            stavki.append(Ali(*tuple(a for a in stavek if a!=trenutna)).bistvo())
                    elif Neg(trenutna) in stavek.sez:
                        if trenutna == F():
                            stavki.remove(stavek)
                        else:
                            stavki.remove(stavek)
                            stavki.append(Ali(*tuple(a for a in stavek if a!=Neg(trenutna))).bistvo())
                    else: continue
                    
                #########sat(In(*tuple(i for i in stavki)).bistvo())
            
            
    
    return literal


def element(s): #vrne edini element v množici in ga pusti notri
    return list(s)[0]
