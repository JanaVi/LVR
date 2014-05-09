from izrazi_cnf import *
from sat import *
from primeri import *

def hadamard_pretvori(n):
    '''Funkcija sprejme število n, vrne pa boolov izraz, s pomočjo katerega ugotovimo,
    ali obstaja Hadamardova matrika dimenzije n x n.'''

    def sprem(u,v,n):
        return Spr('{0}{1}_{2}'.format(u,v,n))

    def polovica(sez,m):
        '''Sprejme seznam izjav sez in število m. Funkcija vrne izjavo, ki je ekvivalentna temu,
        da je v seznamu resničnih natanko m izjav.'''
        
        if m == 0: return In(*tuple(Neg(i) for i in sez)) #nobena izjava ne sme veljati
        elif len(sez) == m: return In(*tuple(i for i in sez)).bistvo() #vse izjave morajo veljati
        else: return Ali(
            In(sez[0],polovica(sez[1:],m-1)), #prva izjava velja
            In(Neg(sez[0]),polovica(sez[1:],m)) #prva izjava ne velja
            )

    if n%2 == 1: return F()
    if n == 0: return F()
    
    prva_vrstica = In(*tuple(sprem(1,j,1) for j in range(1,n+1)))
    prvi_stolpec = In(*tuple(sprem(i,1,1) for i in range(1,n+1)))

    #Na vsakem mestu v matriki je ali 1 ali -1:
    f1 = In(*tuple(Ali(sprem(i,j,1),sprem(i,j,-1)) for i in range(1,n+1) for j in range(1,n+1)))

    #Dve vrstici imata natanko n/2 mest enakih:
    vrstice = set()
    for i in range(1,n):
        for j in range(i+1,n+1):
            sez = list()
            for k in range(1,n+1):
                sez.append(Ali(In(sprem(k,i,1),sprem(k,j,1)),In(sprem(k,i,-1),sprem(k,j,-1))))
            vrstice.add(polovica(sez,n/2))
    f2 = In(*tuple(i for i in vrstice))
 
    #Dva stolpca imata natanko n/2 mest enakih:
    stolpci = set()
    for i in range(1,n):
        for j in range(i+1,n+1):
            sez = list()
            for k in range(1,n+1):
                sez.append(Ali(In(sprem(i,k,1),sprem(j,k,1)),In(sprem(i,k,-1),sprem(j,k,-1))))
            stolpci.add(polovica(sez,n/2))
    f3 = In(*tuple(i for i in stolpci))

    return In(prva_vrstica,prvi_stolpec,f1,f2,f3)

def hadamard_sat_to_matrika(slovar):
    '''Sprejme slovar s ključi (ij_k) in vrednostmi ⊤ in ⊥. Ključ (ij_k) z vrednostjo ⊤ pove,
    da se v kvadratku (i,j) nahaja število k. Funkcija vrne hadamardovo matriko v obliki matrike.'''
    
    if slovar == 'Izraz ni rešljiv.': return 'Ne obstaja Hadamardova matrika te dimezije.'
    
    pom = dict()
    for k in slovar.keys():
        if slovar[k] == T(): pom[k.ime] = slovar[k] #vzamemo samo tiste, ki imajo vrednost ⊤
    n = int(len(pom)**(1/2))
    matrika = [[0 for i in range(n)] for j in range(n)]
    for k in pom.keys():
        k = k.split('_')
        matrika[int(k[0][0])-1][int(k[0][1])-1] = int(k[1])

    s = ''
    for i in range(n):
        for j in range(n):
            if matrika[i][j] == -1: s = s + str(matrika[i][j]) + ' '
            else: s = s + ' ' + str(matrika[i][j]) + ' '
        s = s + '\n'
        
    print(s)

def hadamard(n):
    '''Funkcija sprejme število n in vrne Madamardovo matriko dimenzije n x n (če ta obstaja).'''
    
    return hadamard_sat_to_matrika(sat(hadamard_pretvori(n)))
