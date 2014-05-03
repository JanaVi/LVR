from izrazi_cnf import *
from sat import *
from generator import *
import time

def majhen_test(izraz, literal):
    '''Funkcija sprejme logični izraz in slovar vrednosti spremenljivk in
    preveri ali te vrednosti res nastavijo izraz na T(). če je literal slovar,
    vrne True ali False, sicer vrne niz (iz sat solverja lahko dobimo niz).'''

    if literal == 'Izraz ni rešljiv.': return literal
    elif type(literal) == str: return literal

    a = T()==izraz.vrednost(literal)
    if not a:
        print('OJOJOJOJOJOJOJOJOJOJOJOJOJOJOJOJOJOJOJOJ')
        return a
    return a


def test(n,k,s, izpisuj = False, cas = True):
    '''Funkcija testira pravilnost SAT solverja s pomočjo generatorja primerov.
    n in k označujeta maksimalno število različnih spr. v izrazu in dolžino
    izraza (t.j. število spr. v izrazu). s označuje, koliko primerov želimo
    generirati. Če ne želimo izpisovati časa, ki ga SAT solver porabi za
    reševanje nastavimo cas na False.
    Funkcija nam izpiše pravilnost in čas delovanja(če želimo).'''

    a = time.clock()
    for i in range(s):
        izraz = generiraj(n,k)
        test = majhen_test(izraz, sat(izraz, cas))
        if test == False: print('Napaka')
        if izpisuj: print(test,'\n')
    print('Porabljen čas za {} primerov: {} s.'.format(s,time.clock()-a))

    
