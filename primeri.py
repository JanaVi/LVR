from izrazi_cnf import *
from sat import *

#################### Testi za cnf, SAT ####################

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

primer16 = Ali(In(a,Ali(Ali(b,d),In(e,f))),In(c,Ali(d,a)),e)

