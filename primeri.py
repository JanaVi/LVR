######################## Primeri za cnf ##########################################################################
p = Spr("p")
q = Spr("q")
r = Spr("r")

primer1 = Ali(p,In(q,p))

primer2 = In(p,Ali(q,Neg(p)))

primer3 = In(Ali(p,q),Ali(p,r))

primer4 = In(In(p,q),In(q,r),In(r,p))

primer5 = In(Ali(p,q),Ali(q,r),Ali(r,p),Neg(In(p,q)),Neg(In(q,r)),Neg(In(r,p)))

primer6 = Ali(In(Spr('p'),Spr('r'),Spr('q')),In(Spr('a'),Spr('b'),Spr('c')))

primer7 = In(Ali(In(Spr('p'),Spr('r'),Spr('q')),In(Spr('a'),Spr('b'),Spr('c'))),Spr('K'))

##################################### Primeri za SAT ############################################################
a1=Spr('a1')
a2=Spr('a2')
a3=Spr('a3')
a4=Spr('a4')
a5=Spr('a5')
a6=Spr('a6')



#### Testi
enostavenIn = (*tuple('a'+str(i) for i in range(15)))
enostavenALI = Ali(*tuple('a'+str(i) for i in range(15)))


povezanostJA1 = povezanost({'a': {'b'},'b':{'a','c'},'c':{'b','d'},'d':{'c','e'},'e':{'d'}})
povezanostJA2 = povezanost({'a':{'b','c'},'b':{'a','e','f'},'c':{'a','d'},'d':{'c'},'e':{'b'},'f':{'b'}})


povezanostNE1 = povezanost({'a':{'c'},'b':{'e','f'},'c':{'a','d'},'d':{'c'},'e':{'b'},'f':{'b'}})
povezanostNE2 = povezanost({'a':{'b'},'b':{'a'},'c':{'d'},'d':{'c'}})

#Testi dolžine 9
enostavenJA = Ali(In(a1,(Ali(Ali(a2,a4),In(a5,a6)))),(In(a3,Ali(a4,a1))),a5)
enostavenNE = Ali(In(a1,(Ali(Ali(a2,a4),In(a5,a6)))),(In(a3,Ali(a4,a6))),a5)
