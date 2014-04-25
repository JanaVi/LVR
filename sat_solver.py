from izrazi_cnf import *
from primeri import *
from generator_primerov import *
from sudoku import *


def sat(izraz):
    izraz = izraz.cnf() #sedaj je izraz v konjuktivni obliki
##    print('začetna cnf oblika=',izraz)
    
    if izraz == T():
        print('???')
        return T()
    elif izraz == F(): return F()

    literal = dict() #slovar vseh spremenljivk, skupaj z očitnimi znanimi vrednostmi
    stavki = [i for i in izraz.sez] #stavki, ki jih je še potrebno predelati

    rezultat = pomo(stavki, literal)
    if type(rezultat) == F: return 'Dani izraz ni rešljiv.'
    elif type(rezultat) == T: return 'Dani izraz je rešljiv za kakršnekoli vrednosti spremenljivk.'
    else:
        print('Dani izraz je rešljiv za naslednje vrednosti spremenljivk:')
        return rezultat
    

def pomo(stavki, literal):
    '''dobi stavke iz cnf oblike in slovar že znanih spr.
       vrne ali seznam možnih vrednosti spremenljivk ali F() ali T()'''
    
    if len(stavki) == 0: return T()
    
    izraz = In(*tuple(i for i in stavki)).cnf() ####nepotrebno
    
    if izraz == T(): return T() ####nepotrebno
    elif izraz == F(): return F() ####nepotrebno
    
##    print('literal=', literal)
##    print('začetni stavki=',stavki)
##    print('\n')
    
    while stavki:
        stavki = list(uredi_po_dolzini(stavki))
        i = stavki[0]
##        print('while zanka',i)
        if not (type(i) == Spr or type(i) == Neg):
##            print('sami sestavljeni stavki')
            break #če več nimamo samostojnih spr. med stavki
        
        if type(i) == Spr: #samostojna spremenljivka
            stavki.remove(i)
            literal[i.ime] = T()
            
            stavki2=list(stavki) #nadomestna kopija preostalih stavkov
            for stavek in stavki2:
                if type(stavek) == Neg and stavek.izr==i: return F()
                elif type(stavek) == Spr and stavek == i: stavki.remove(stavek)
                elif type(stavek) == Ali :
                    for lit in stavek.sez:
                        if type(lit) == Spr and lit == i:
                            stavki.remove(stavek)
                        if type(lit) == Neg and lit.izr == i:
                            stavki.remove(stavek) 
                            stavki.append(Ali(*tuple(a for a in stavek.sez if a!=Neg(i))).bistvo()) #odstrani stari stavek in ga nadomesti z novim, ki nima negacij naše spremenljivke  
                else: pass  #sem pride, če ne obstaja stavek, ki vsebuje i. 
                
            
        elif type(i) == Neg: #samostojna negirana spremenljivka
            stavki.remove(i)
            literal[i.izr.ime] = F()
            
            stavki2=list(stavki) #nadomestna kopija preostalih stavkov
            for stavek in stavki2:
                if type(stavek) == Spr and stavek==i.izr: return F()           
                elif type(stavek) == Neg and stavek.izr==i.izr: stavki.remove(stavek)
                elif type(stavek) == Ali:
                    for lit in stavek.sez:
                        if type(lit) == Spr and lit == i.izr:
                            stavki.remove(stavek)
                            stavki.append(Ali(*tuple(a for a in stavek.sez if a!=i.izr)).bistvo()) #odstrani stari stavek in ga nadomesti z novim, ki nima negacij naše spremenljivke  
                        if type(lit) == Neg and lit.izr == i.izr:
                            stavki.remove(stavek)
                else: pass    

        else: #############sestavljen stavek, do tega nikoli ne pride!!!!
            for j in i.sez:
                if type(j) == Spr and j.ime not in literal:
                    literal[j.ime] = ''
                elif type(j) == Neg and j.izr.ime not in literal:
                    literal[j.izr.ime] = ''
##                    
##        print('stavki na koncu zanke=',stavki)
##
##    print('\n')
##    print('stavki, ki so ostali',stavki)
    neznane = uredi_po_frekvenci(stavki) 
    
    # imamo stavke (ki so vsi sestavljeni!), literale in neznane (ki so še v stavkih), skupaj z njihovimi frekvencami
##    print('konec poma, tik pred zanko = ', stavki, literal, neznane)
##    print('\n')
    
    if not stavki:
##        print(literal)
##        print('1?','\n')
        return literal #ni več stavkov, imamo vse potrebne vrednosti za naše spremenljivke

    
    for i in [F(),T()]:
        stavki_prej = list(stavki)
        literal_prej = dict(literal)
        neznane_prej = dict(neznane)
        
##        print('.')
##        print('.')
##        print('.')
##        print('neznane=',neznane)
##        print('literal=',literal)
        trenutna = max(neznane, key=neznane.get)
##        print('trenutna=', trenutna, i)
        literal[trenutna] = i
        
        #gremo po vseh stavkih in vstavljamo vrednost za našo trenutno spr.
        stavki2 = list(stavki)
##        print('stavek2=', stavki2)
##        print('\n')
        for stavek in stavki2:
##            print('stavek=', stavek)
            if trenutna in stavek.sez:
                if literal[trenutna] == T():
                    stavki.remove(stavek)
                else:
                    stavki.remove(stavek)
                    stavki.append(Ali(*tuple(a for a in stavek.sez if a!=trenutna)).bistvo())
            elif Neg(trenutna) in stavek.sez:
                if literal[trenutna] == F():
                    stavki.remove(stavek)
                else:
                    stavki.remove(stavek)
                    stavki.append(Ali(*tuple(a for a in stavek.sez if a!=Neg(trenutna))).bistvo())
            else: continue

##        print('\n')
##        print('pred rekurzijo:', stavki, literal)
##        print('.')
##        print('.')
##        print('.')
##        print('\n')
        vmes = pomo(stavki, literal)
        
        if type(vmes) == F:
            if i == F():
                stavki = list(stavki_prej)
                literal = dict(literal_prej)
                neznane = dict(neznane_prej)
            else:
##                print('Primer ni rešljiv pri tako nastavljenih spremenljivkah.')
                return F()
        elif type(vmes) == T:
##            print(literal)
##            print('2?','\n')
            return literal
        else:
##            print(literal)
##            print('3?','\n')
            return literal


def uredi_po_frekvenci(stavki):
    '''sprejme stavke in vrne spremenljivke v slovarju, urejene po frekvenci'''
    
    slovar = dict()
    for stavek in stavki:
        for i in stavek.sez:
            if type(i) == Spr:
                if i not in slovar: slovar[i] = 1
                else: slovar[i]+=1
            elif type(i) == Neg:
                if i.izr not in slovar: slovar[i.izr] = 1
                else: slovar[i.izr]+=1
            else: print('Napaka pri uredi_po_frekvenci')
    return slovar         


def uredi_po_dolzini(stavki):
    '''sprejme stavke in vrne seznam stavkov, urejenih po dolžini (torej številu spremenljivk)'''
    
    slovar = dict()
    seznam = []
    for stavek in stavki:
        if type(stavek) == Spr or type(stavek) == Neg:
            if 1 in slovar: slovar[1].add(stavek)
            else:
                slovar[1] = set()
                slovar[1].add(stavek)
        else:
            n = len(stavek.sez)
            if n in slovar:
                slovar[n].add(stavek)
            else:
                slovar[n] = set()
                slovar[n].add(stavek)
    for key in sorted(slovar.keys()):
        for i in slovar[key]:
            seznam.append(i)
    return seznam


def neznani_literali(stavki):
    '''sprejme preostale stavke v izrazu in vrne množico literalov iz stavkov'''
    
    if not stavki: return set()
    mn=set()
    for stavek in stavki:
        if type(stavek) == Spr: mn.add(stavek.ime)
        elif type(stavek) == Neg: mn.add(stavek.izr.ime)
        elif type(stavek) == Ali: mn = mn.union(stavek.sez)
        else: print('napaka pri nezanani_literali')
    return mn

            
def element(s):
    '''vrne edini element v množici in ga pusti notri'''
    
    return list(s)[0]
