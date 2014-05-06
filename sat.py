from izrazi_cnf import *
import time

def sat(izraz, cas = False):
    '''Funkcija sprejme logični izraz in če je rešljiv, vrne slovar možnih vrednosti.'''

    if type(izraz) == str: return izraz #za potrebe prevedb
    
    b = time.clock()
    izraz = izraz.cnf() #sedaj je izraz v konjuktivni obliki
    
    if izraz == T():
        if cas: print('sat time=', time.clock()-b)
        return 'Izraz je rešljiv za kakršnekoli vrednosti spremenljivk.'
    elif izraz == F():
        if cas: print('sat time=', time.clock()-b)
        return 'Izraz ni rešljiv.'

    literal = dict() #slovar spremenljivk z določenimi vrednostmi
    if type(izraz) == In: stavki = [i for i in izraz.sez] #stavki, ki jih je še potrebno predelati
    else: stavki = [izraz]

    rezultat = pomo(stavki, literal)

    if cas: print('sat time=', time.clock()-b)
    if type(rezultat) == F: return 'Izraz ni rešljiv.'
    elif type(rezultat) == T: return 'Izraz je rešljiv za kakršnekoli vrednosti spremenljivk.'
    else: return rezultat
   

def pomo(stavki, literal):
    '''Dobi stavke v cnf obliki in slovar že znanih spremenljivk.
       Vrne ali slovar možnih vrednosti spremenljivk ali F() ali T().'''
    
    if len(stavki) == 0: return T()

    rezultat = samostojne(stavki, literal) #rešimo se samostojnih literalov
    if type(rezultat) == F: return F()
    stavki, literal = rezultat
    if not stavki: return literal #če ni več stavkov, imamo vse potrebne vrednosti za naše spremenljivke
    
    stavki, literal = ciste_pojavitve(stavki, literal) #rešimo se čistih pojavitev
    if not stavki: return literal
    neznane = uredi_po_frekvenci(stavki)

    trenutna = max(neznane, key = neznane.get)
    for i in [F(),T()]:
        stavki_prej = list(stavki)
        literal_prej = dict(literal)
        neznane_prej = dict(neznane)
        
        literal[trenutna] = i
        
        #gremo po vseh stavkih in vstavljamo vrednost za našo trenutno spr.
        stavki2 = list(stavki)

        for stavek in stavki2:
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

        vmes = pomo(stavki, literal)
        
        if type(vmes) == F:
            if i == F():
                stavki = list(stavki_prej)
                literal = dict(literal_prej)
                neznane = dict(neznane_prej)
            else: return F()
        elif type(vmes) == T: return literal
        else: return vmes


def uredi_po_frekvenci(stavki):
    '''Sprejme stavke in vrne spremenljivke v slovarju, skupaj z njihovimi frekvencami in dolžinami
    najkrajših stavkov, v katerih nastopajo.'''
    
    slovar = dict()
    for stavek in stavki:
        for i in stavek.sez:
            n = len(stavek.sez)
            if type(i) == Spr:
                if i in slovar:
                    slovar[i][0]+=1
                    slovar[i][1] = max(-n,slovar[i][1]) #vzamemo dolžino najkrajšega stavka
                else: slovar[i] = [1, -n]
            elif type(i) == Neg:
                if i.izr in slovar:
                    slovar[i.izr][0]+=1
                    slovar[i.izr][1] = max(-n,slovar[i.izr][1])
                else: slovar[i.izr] = [1, -n]
    return slovar         


def uredi_po_dolzini(stavki):
    '''Sprejme stavke in vrne slovar, ki ima za ključe dolžine, za vrednosti pa stavke te dolžine'''
    
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
    if 1 not in slovar: slovar[1] = set()
    return slovar


def ciste_pojavitve(stavki, literal):
    '''Sprejme stavke v izrazu in slovar že določenih vrednosti. Vrne dopolnjen slovar z vrednostmi
    literalov, ki nastopajo samo nenegirani ali samo negirani in prečiščene stavke.'''

    slovar = dict()
    for stavek in stavki:
        if type(stavek) == Spr:
            if stavek in slovar: slovar[stavek].add(1)
            else: slovar[stavek] = set().union({1})
        elif type(stavek) == Neg:
            if stavek.izr in slovar: slovar[stavek.izr].add(-1)
            else: slovar[stavek.izr] = set().union({-1})
        elif type(stavek) == Ali:
            for i in stavek.sez:
                if type(i) == Spr:
                    if i in slovar: slovar[i].add(1)
                    else: slovar[i] = set().union({1})
                elif type(i) == Neg:
                    if i.izr in slovar: slovar[i.izr].add(-1)
                    else: slovar[i.izr] = set().union({-1})
    for spr in slovar:
        if slovar[spr] == {1}: #v izrazu se pojavlja samo spremenljivka
            literal[spr] = T()
            stavki2 = list(stavki)
            for stavek in stavki2: #gremo po vseh stavkih in brišemo tiste, ki vsebujejo to spr.
                if spr in stavek.sez: stavki.remove(stavek)
        elif slovar[spr] == {-1}: #v izrazu se pojavlja samo negirana spr.
            literal[spr] = F()
            stavki2 = list(stavki)
            for stavek in stavki2:
                if Neg(spr) in stavek.sez: stavki.remove(stavek)
    return stavki, literal
        

def samostojne(stavki, literal):
    '''Sprejme stavke v izrazu in slovar že določenih vrednosti spremenljivk. Najde spremenljivke,
    ki same nastopajo v stavkih, vrne dopolnjen slovar in prečiščene stavke, ki so vsi sestavljeni.'''

    stavki_dolzina = uredi_po_dolzini(stavki)
    while stavki_dolzina[1]: #dokler imamo stavek z dolžino 1
        i = stavki_dolzina[1].pop()
        if type(i) == Spr: #samostojna spremenljivka
            literal[i] = T()
            stavki2 = [st for k in stavki_dolzina.keys() for st in stavki_dolzina[k]]
            for stavek in stavki2: #gremo po vseh stavkih in vstavljamo T() namesto naše spr.
                if type(stavek) == Neg and stavek.izr==i: return F()
                elif type(stavek) == Ali :
                    n = len(stavek.sez)
                    for lit in stavek.sez:
                        if type(lit) == Spr and lit == i:
                            stavki_dolzina[n].remove(stavek)
                            break
                        elif type(lit) == Neg and lit.izr == i:
                            stavki_dolzina[n].remove(stavek)
                            if n-1 in stavki_dolzina: stavki_dolzina[n-1].add(Ali(*tuple(a for a in stavek.sez if a!=Neg(i))).bistvo())
                            else: stavki_dolzina[n-1] = set().union({Ali(*tuple(a for a in stavek.sez if a!=Neg(i))).bistvo()})

        elif type(i) == Neg: #samostojna negirana spremenljivka
            literal[i.izr] = F()
            stavki2 = [st for k in stavki_dolzina.keys() for st in stavki_dolzina[k]]
            for stavek in stavki2: #gremo po vseh stavkih in vstavljamo F() namesto naše spr.
                if type(stavek) == Spr and stavek==i.izr: return F()           
                elif type(stavek) == Ali:
                    n = len(stavek.sez)
                    for lit in stavek.sez:
                        if type(lit) == Spr and lit == i.izr:
                            stavki_dolzina[n].remove(stavek)
                            if n-1 in stavki_dolzina: stavki_dolzina[n-1].add(Ali(*tuple(a for a in stavek.sez if a!=i.izr)).bistvo())
                            else: stavki_dolzina[n-1] = set().union({Ali(*tuple(a for a in stavek.sez if a!=i.izr)).bistvo()})
                        elif type(lit) == Neg and lit.izr == i.izr:
                            stavki_dolzina[n].remove(stavek)
                            break
    return [st for k in stavki_dolzina.keys() for st in stavki_dolzina[k]], literal

