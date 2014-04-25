from izrazi_cnf import *
from sat_solver import *
    
def sudoku(zacetni):
    '''Dani sudoku prevede v boolov izraz. Začetne pogoje podamo s seznamom
    trojic [(i1,j1,k1),(i2,j2,k2),...], ki predstavljajo polje sudokuja (i,j)
    ter vrednost na tem mestu k.'''

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

    return In(f1, f2, f3, f4, f5, f6, f7, f8, danipogoji)

def sudoku_matrika(slovar):
    '''Sprejme slovar s ključi (i,j,k) in vrednostmi ⊤ in ⊥. Ključ (i,j,k) z vrednostjo ⊤ pove,
    da se v kvadratku (i,j) nahaja število k. Funkcija vrne rešitev sudokuja v obliki matrike.'''

    if type(slovar) == str: return 'Sudoku s tako podanimi začetnimi vrednostmi ni rešljiv.'
    
    pom = dict()
    for k in slovar.keys():
        if slovar[k] == T(): pom[k] = slovar[k] #vzamemo samo tiste, ki imajo vrednost ⊤
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



#nekaj primerov:
    
NPS = [(1,1,8),(3,3,5),(1,5,9),(1,6,3),(1,7,7),(1,9,1),(2,5,5),(2,7,3),(2,8,6),(2,9,9),(3,4,6),(3,5,7),(4,6,8),(4,9,6),(5,1,6),(5,2,7),(5,3,4),(5,4,9),(5,6,5),(5,7,2),(5,8,3),(5,9,8),(6,1,1),(6,4,7),(7,5,8),(7,6,9),(7,7,5),(8,1,9),(8,2,1),(8,3,2),(8,5,3),(9,1,5),(9,3,8),(9,4,4),(9,5,2),(9,9,7)]

NDS = [(1,2,1),(1,5,6),(1,7,4),(1,9,9),(2,6,3),(2,7,5),(3,4,9),(3,7,2),(4,5,2),(4,9,4),(5,1,6),(5,2,9),(5,8,1),(5,9,3),(6,1,5),(6,5,8),(7,3,8),(7,6,5),(8,3,1),(8,4,2),(9,1,9),(9,3,4),(9,5,1),(9,8,7),(3,1,4),(3,6,1),(6,3,3),(1,8,3),(2,5,4),(3,5,5),(3,8,8),(4,7,9),(4,8,5),(5,5,7),(5,6,4),(5,7,8)]

NTS = [(1,3,6),(1,5,7),(1,6,4),(1,8,8),(1,9,2),
         (2,3,9),(2,6,5),(2,9,3),
         (3,2,2),(3,4,3),(3,5,6),(3,7,9),(3,9,5),
         (4,2,6),(4,4,5),(4,5,3),(4,6,2),
         (5,4,1),(5,6,9),
         (6,4,7),(6,5,8),(6,6,6),(6,8,2),
         (7,1,7),(7,3,5),(7,5,9),(7,6,3),(7,8,6),
         (8,1,6),(8,4,8),(8,7,3),
         (9,1,1),(9,2,9),(9,4,6),(9,5,2),(9,7,8)]

NCS = [(1,1,9),(1,2,2),(1,5,1),(1,6,5),
       (2,3,5),(2,8,6),
       (3,1,6),(3,2,1),(3,4,3),(3,9,4),
       (4,1,2),(4,2,8),(4,5,4),
       (5,1,1),(5,5,3),(5,9,6),
       (6,5,8),(6,8,9),(6,9,5),
       (7,1,4),(7,6,9),(7,8,5),(7,9,3),
       (8,2,9),(8,7,6),
       (9,4,8),(9,5,6),(9,8,4),(9,9,1)]

