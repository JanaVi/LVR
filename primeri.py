from izrazi_cnf import *
from povezanost import *
from barvanje import *

######################## Primeri za cnf, SAT ##########################################################################

p = Spr('p')
r = Spr('r')
q = Spr('q')
a = Spr('a')
b = Spr('b')
c = Spr('c')
d = Spr('d')
e = Spr('e')
f = Spr('f')

primer1 = Ali(p,In(q,p))
primer2 = In(p,Ali(q,Neg(p)))
primer3 = In(Ali(p,q),Ali(p,r))
primer4 = In(In(p,q),In(q,r),In(r,p))
primer5 = In(Ali(p,q),Ali(q,r),Ali(r,p),Neg(In(p,q)),Neg(In(q,r)),Neg(In(r,p)))
primer6 = Ali(In(Spr(p),Spr(r),Spr(q)),In(Spr(a),Spr(b),Spr(c)))
primer7 = In(Ali(In(Spr(p),Spr(r),Spr(q)),In(Spr(a),Spr(b),Spr(c))),Spr(f))
primer8 = In(Ali(Neg(a),b,Neg(c),e,Neg(f)),Ali(Neg(a),e,d),Ali(e,f,c,Neg(p),Neg(r)),Ali(q,b,f))
primer9 = In(Ali(a,b,c),Ali(Neg(a),Neg(b)),c)


p1=In(T(),F(),Ali(p,Neg(p)))
p2=Ali(Neg(In(p,r,q,)))
p3=In(T(),In(p,Neg(p)))


a1 = Spr('a1')
a2 = Spr('a2')
a3 = Spr('a3')
a4 = Spr('a4')
a5 = Spr('a5')
a6 = Spr('a6')

#### Testi
enostavenIn = In(*tuple('a'+str(i) for i in range(15)))
enostavenALI = Ali(*tuple('a'+str(i) for i in range(15)))


povezanostJA1 = povezanost({'a': {'b'},'b':{'a','c'},'c':{'b','d'},'d':{'c','e'},'e':{'d'}})
povezanostJA2 = povezanost({'a':{'b','c'},'b':{'a','e','f'},'c':{'a','d'},'d':{'c'},'e':{'b'},'f':{'b'}})


povezanostNE1 = povezanost({'a':{'c'},'b':{'e','f'},'c':{'a','d'},'d':{'c'},'e':{'b'},'f':{'b'}})
povezanostNE2 = povezanost({'a':{'b'},'b':{'a'},'c':{'d'},'d':{'c'}})

#Testi dolžine 9
enostavenJA = Ali(In(a1,(Ali(Ali(a2,a4),In(a5,a6)))),(In(a3,Ali(a4,a1))),a5)
enostavenNE = Ali(In(a1,(Ali(Ali(a2,a4),In(a5,a6)))),(In(a3,Ali(a4,a6))),a5)
