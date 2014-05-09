from izrazi_cnf import *
from sat import *
from generator import *
import time

def majhen_test(izraz, literal):
    '''Funkcija sprejme logični izraz in slovar vrednosti spremenljivk in preveri,
    ali te vrednosti res nastavijo izraz na T(). Če je literal slovar, vrne True
    (pripisane vrednosti res nastavijo izraz na T()) ali False (izraz ni enak T()),
    sicer vrne niz (iz sat solverja lahko namreč dobimo niz namesto slovarja).'''

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
    reševanje, nastavimo cas na False. Če ne želimo izpisovati rezultatov testiranja,
    nastavimo izpisuj na False.'''

    a = time.clock()
    for i in range(s):
        izraz = generiraj(n,k)
        test = majhen_test(izraz, sat(izraz, cas))
        if test == False: print('Napaka: SAT solver ne vrne prave rešitve.')
        if izpisuj: print(test,'\n')
    print('Porabljen čas za {} primerov: {} s.'.format(s,time.clock()-a))

    
