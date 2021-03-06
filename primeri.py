from izrazi_cnf import *

#################### primeri za cnf, SAT ####################

p = Spr('p')
r = Spr('r')
q = Spr('q')
a = Spr('a')
b = Spr('b')
c = Spr('c')
d = Spr('d')
e = Spr('e')
f = Spr('f')

p1, p1_cnf = Ali(a), a
p2, p2_cnf = In(a,Neg(a)), F()
p3, p3_cnf = Ali(a,Neg(a)), T()
p4, p4_cnf = In(T(),F(),Ali(p,Neg(p))), F()
p5, p5_cnf = Ali(Neg(In(p,r,q))), Ali(Neg(r),Neg(p),Neg(q))
p6, p6_cnf = In(T(),In(p,Neg(p))), F()
p7, p7_cnf = In(a), a
p8, p8_cnf = Ali(p,In(q,p)), In(p,Ali(p,q))
p9, p9_cnf = In(p,Ali(q,Neg(p))), In(p,Ali(q,Neg(p)))
p10, p10_cnf = Ali(Ali(a)), a
p11, p11_cnf = Ali(Ali(a,b),In(Neg(a),b)), Ali(a,b) 
p12, p12_cnf = In(Ali(p,q),Ali(p,r)), In(Ali(p,q),Ali(p,r))
p13, p13_cnf = In(In(p,q),In(q,r),In(r,p)), In(p,q,r)
p14, p14_cnf = Ali(In(p,q),In(a,b,Neg(p))), In(Ali(a,p),Ali(a,q),Ali(b,p),Ali(b,q),Ali(Neg(p),q))
p15, p15_cnf = In(Ali(In(p,r),In(a,b)),f), In(f, Ali(a,p),Ali(a,r),Ali(b,p),Ali(b,r))

p16 = Ali(In(a,Ali(Ali(b,d),In(e,f))),In(c,Ali(d,a)),e)
p17 = Ali(F(),Ali(a,b,c),In(Neg(a),e,f,Ali(c,d),T()),Neg(Ali(Neg(e),d)),In(b,f))


#################### primeri za sudoku ####################
## Neresljiv sudoku
sud1 = [(1,2,8),(1,4,3),(1,5,1),
        (2,3,3),(2,6,5),(2,7,4),(2,9,1),
        (3,4,7),(3,7,8),(3,8,5),
        (4,1,9),(4,2,7),(4,6,2),(4,9,6),
        (5,1,4),(5,2,6),(5,3,1),(5,7,7),(5,8,9),(5,9,4),
        (6,1,2),(6,4,6),(6,8,8),(6,9,4),
        (7,2,4),(7,3,7),(7,6,1),
        (8,1,8),(8,3,9),(8,4,2),(8,7,3),
        (9,5,7),(9,6,3),(9,8,1)]
## Sudokuji z resitvijo
sud2 = [(1,1,8),(1,5,9),(1,6,3),(1,7,7),(1,9,1),
       (2,5,5),(2,7,3),(2,8,6),(2,9,9),
       (3,3,5),(3,4,6),(3,5,7),
       (4,6,8),(4,9,6),
       (5,1,6),(5,2,7),(5,3,4),(5,4,9),(5,6,5),(5,7,2),(5,8,3),(5,9,8),
       (6,1,1),(6,4,7),
       (7,5,8),(7,6,9),(7,7,5),
       (8,1,9),(8,2,1),(8,3,2),(8,5,3),
       (9,1,5),(9,3,8),(9,4,4),(9,5,2),(9,9,7)]

sud3 = [(1,2,1),(1,5,6),(1,7,4),(1,8,3),(1,9,9),
       (2,5,4),(2,6,3),(2,7,5),
       (3,1,4),(3,4,9),(3,5,5),(3,6,1),(3,7,2),(3,8,8),
       (4,5,2),(4,7,9),(4,8,5),(4,9,4),
       (5,1,6),(5,2,9),(5,5,7),(5,6,4),(5,7,8),(5,8,1),(5,9,3),
       (6,1,5),(6,3,3),(6,5,8),
       (7,3,8),(7,6,5),
       (8,3,1),(8,4,2),
       (9,1,9),(9,3,4),(9,5,1),(9,8,7)]

sud4 = [(1,3,6),(1,5,7),(1,6,4),(1,8,8),(1,9,2),
       (2,3,9),(2,6,5),(2,9,3),
       (4,2,6),(4,4,5),(4,5,3),(4,6,2),
       (5,4,1),(5,6,9),
       (6,4,7),(6,5,8),(6,6,6),(6,8,2),
       (7,1,7),(7,3,5),(7,5,9),(7,6,3),(7,8,6),
       (8,1,6),(8,4,8),(8,7,3),
       (9,1,1),(9,2,9),(9,4,6),(9,5,2),(9,7,8)]

sud5 = [(1,1,9),(1,2,2),(1,5,1),(1,6,5),
       (2,3,5),(2,8,6),
       (3,1,6),(3,2,1),(3,4,3),(3,9,4),
       (4,1,2),(4,2,8),(4,5,4),
       (5,1,1),(5,5,3),(5,9,6),
       (6,5,8),(6,8,9),(6,9,5),
       (7,1,4),(7,6,9),(7,8,5),(7,9,3),
       (8,2,9),(8,7,6),
       (9,4,8),(9,5,6),(9,8,4),(9,9,1)]

##Poln sudoku
sud6 = [(1,1,5),(1,2,3),(1,3,6),(1,4,9),(1,5,7),(1,6,4),(1,7,1),(1,8,8),(1,9,2),
       (2,1,8),(2,2,7),(2,3,9),(2,4,2),(2,5,1),(2,6,5),(2,7,6),(2,8,4),(2,9,3),
       (3,1,4),(3,2,2),(3,3,1),(3,4,3),(3,5,6),(3,6,8),(3,7,9),(3,8,7),(3,9,5),
       (4,1,9),(4,2,6),(4,3,7),(4,4,5),(4,5,3),(4,6,2),(4,7,4),(4,8,1),(4,9,8),
       (5,1,2),(5,2,5),(5,3,8),(5,4,1),(5,5,4),(5,6,9),(5,7,7),(5,8,3),(5,9,6),
       (6,1,3),(6,2,1),(6,3,4),(6,4,7),(6,5,8),(6,6,6),(6,7,5),(6,8,2),(6,9,9),
       (7,1,7),(7,2,8),(7,3,5),(7,4,4),(7,5,9),(7,6,3),(7,7,2),(7,8,6),(7,9,1),
       (8,1,6),(8,2,4),(8,3,2),(8,4,8),(8,5,5),(8,6,1),(8,7,3),(8,8,9),(8,9,7),
       (9,1,1),(9,2,9),(9,3,3),(9,4,6),(9,5,2),(9,6,7),(9,7,8),(9,8,5),(9,9,4)]


#################### primeri za barvanje grafa ####################

g1 = {'a':{'b'},'b':{'a','c'},'c':{'b','d'},'d':{'c','e'},'e':{'d'}}
g2 = {'a':{'b','f'},'b':{'a','c','f'},'c':{'b','d','f'},'d':{'c','e','f'},'e':{'d','f'},'f':{'a','b','c','d','e'}}
g3 = {'a':{'b','f','g'},'b':{'a','c'},'c':{'b','d','g'},'d':{'c','e'},'e':{'d','f','g'},'f':{'a','e','g'},'g':{'a','c','e','f'}}
g4 = {'a':{'b','c'},'b':{'a','e','f'},'c':{'a','d'},'d':{'c'},'e':{'b'},'f':{'b'}}
g5 = {1:{2,6,7},2:{1,7,5,3},3:{2,4},4:{3,5,6},5:{2,4,6},6:{1,5,4},7:{1,2}}
g6 = {1:{2,3,4,5,6},2:{1,3,4,5,6},3:{1,2,4,5,6},4:{1,2,3,5,6},5:{1,2,3,4,6},6:{1,2,3,4,5}} #poln graf na 6 vozliscih
g7 = {1:{2,5,6},2:{1,3,7},3:{2,4,8},4:{3,5,9},5:{4,1,10},6:{1,8,9},7:{2,9,10},8:{3,10,6},9:{4,6,7},10:{5,7,8}} #petersenov graf
g8 = {1:{2,4,5},2:{1,3,5,6},3:{2,5,6},4:{1,5},5:{1,2,3,4,6},6:{2,3,5}}
