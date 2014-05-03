from izrazi_cnf import *
from sat import *
from primeri import *

def sudoku_pretvori(zacetni):
    '''Sprejme začetne pogoje, podane s seznamom trojic [(i1,j1,k1),(i2,j2,k2),...].
    Trojica (i,j,k) predstavlja polje (i,j), ter vrednost k na tem polju.'''
    
    def sprem(i, j, k):
        return Spr(str(i)+',' + str(j) + ',' + str(k))

    #Vsako polje ima vsaj eno število:
    f1 = In(*tuple(Ali(*tuple(sprem(i,j,k) for k in range(1, 10)))
                    for i in range(1, 10)
                    for j in range(1, 10)))

    #Polje nima hkrati dveh ali več števil:
    f2 = In(*tuple(In(*tuple(Neg(In(sprem(i,j,k), sprem(i,j,l))) for k in range(1,10) for l in range(k+1,10)))
                    for i in range(1,10)
                    for j in range(1,10)))
    
    #Število se pojavi v stolpcu:
    f3 = In(*tuple(Ali(*tuple(sprem(i,j,k) for i in range(1,10)))
                    for j in range(1,10)
                    for k in range(1,10)))

    #Število se ne ponovi v stolpcu:
    f4 = In(*tuple(In(*tuple(Neg(In(sprem(i,j,k),sprem(l,j,k))) for i in range(1,10) for l in range (i+1,10)))
                    for j in range (1,10)
                    for k in range (1,10)))
    
    #Število se pojavi v vrstici:
    f5 = In(*tuple(Ali(*tuple(sprem(i,j,k) for j in range(1,10)))
                    for i in range(1,10)
                    for k in range(1,10)))

    #Število se ne ponovi v vrstici:
    f6 = In(*tuple(In(*tuple(Neg(In(sprem(i,j,k),sprem(i,l,k))) for j in range (1,10) for l in range (j+1,10)))
                    for i in range (1,10)
                    for k in range (1,10)))
    
    #Število se pojavi v 3x3 podkvadratku:
    f7 = In(*tuple(Ali(*tuple(sprem(i+3*s,j+3*v,k) for i in range(1,4) for j in range(1,4)))
                    for v in range(3)
                    for s in range(3)               
                    for k in range(1,10)))

    #Število se ne ponovi v 3x3 podkvadratku:
    f8 = In(*tuple(In(*tuple(Neg(In(sprem(i+3*s,j+3*v,k),sprem(a+3*s,b+3*v,k))) for i in range(1,4)
                                                                                for j in range(1,4)
                                                                                for a in range(i+1,4)
                                                                                for b in range(j+1,4)))
                    for v in range(3)
                    for s in range(3)
                    for k in range(1,10)))
                        
    #Upoštevamo začetne vrednosti:
    danipogoji = In(*tuple(sprem(i[0],i[1],i[2]) for i in zacetni))

    #Olajšamo delo cnf metodi, znebimo se gnezdenih In-ov:
    v2 = {i for stavek in f2.sez for i in stavek.sez}
    v4 = {i for stavek in f4.sez for i in stavek.sez}
    v6 = {i for stavek in f6.sez for i in stavek.sez}
    v8 = {i for stavek in f8.sez for i in stavek.sez}

    return In(*tuple(i for i in f1.sez|v2|f3.sez|v4|f5.sez|v6|f7.sez|v8|danipogoji.sez))

def sudoku_sat_to_matrika(slovar):
    '''Sprejme slovar s ključi (i,j,k) in vrednostmi ⊤ in ⊥. Ključ (i,j,k) z vrednostjo ⊤ pove,
    da se v kvadratku (i,j) nahaja število k. Funkcija vrne rešitev sudokuja v obliki matrike.'''
    
    if slovar == 'Izraz ni rešljiv.': return 'Sudoku s tako podanimi začetnimi vrednostmi ni rešljiv.'
    
    ################popravi za že rešen sudoku
    
    pom = dict()
    for k in slovar.keys():
        if slovar[k] == T(): pom[k.ime] = slovar[k] #vzamemo samo tiste, ki imajo vrednost ⊤
    matrika = [[0 for i in range(9)] for j in range(9)]

    for k in pom.keys():
        matrika[int(k[0])-1][int(k[2])-1] = int(k[4])
        
    s = ''
    for i in range(9):
        for j in range(9):
            s = s + str(matrika[i][j]) + ' '
            if j == 2 or j == 5: s = s + '| '
        s = s + '\n'
        if i == 2 or i == 5: s = s + 21*'-' + '\n'
        
    print(s)

def sudoku(zacetni):
    '''Sprejme začetne pogoje, podane s seznamom trojic [(i1,j1,k1),(i2,j2,k2),...]. Trojica (i,j,k)
    predstavlja polje (i,j), ter vrednost k na tem polju. Funkcija vrne rešitev sudokuja v obliki matrike.'''
    
    return sudoku_sat_to_matrika(sat(sudoku_pretvori(zacetni)))

