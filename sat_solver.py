############ SAT #############################

def sat(izraz):
    izraz = izraz.cnf() #sedaj je izraz v konjuktivni obliki
    
    if izraz == T(): return True
    elif izraz == F(): return False
    
##    elif len(izraz.sez) == 0 and type(izraz) == In: return True #če ni stavkov
##    elif len(izraz.sez) == 0 and type(izraz) == Ali: return False

    print('cnf oblika=',izraz)
    literal = dict() #slovar vseh spremenljivk, skupaj z očitnimi znanimi vrednostmi
    stavki = [i for i in izraz.sez] #stavki, ki jih je še potrebno predelati
    print('začetni stavki=',stavki)


    #######tega se želimo znebiti že v cnf!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! zaenkrat notri zaradi pravilnosti
    for i in izraz.sez: #če je kakšen stavek F()
        if type(i) == F: return False

        
    for i in izraz.sez: 
        if type(i) == Spr: #samostojna spremenljivka
            stavki.remove(i)
            print('preostali stavki=',stavki)
            literal[i.ime] = True
            stavki2=stavki #nadomestna kopija preostalih stavkov
            
            for stavek in stavki2:
                if type(stavek) == Spr and stavek==i: stavki.remove(stavek)
                elif type(stavek) == Neg and stavek.izr==i: return False
                elif type(stavek) == Ali and len(stavek.sez)>1:
                    for lit in stavek.sez:
                        if type(lit) == Spr and lit == i:
                            stavki.remove(stavek)
                        if type(lit) == Neg and lit.izr == i:
                            stavki.remove(stavek)
                            stavki.append(Ali(*tuple(a for a in stavek if a!=Neg(i)))) #odstrani stari stavek in ga nadomesti z novim, ki nima negacij naše spremenljivke  
                else: print('Napaka pri vstavljanju znanih spr. v preostale stavke 1.')
                
            
        elif type(i) == Neg: #samostojna negirana spremenljivka
            stavki.remove(i)
            print('preostali stavki=',stavki)
            literal[i.izr.ime] = False
            stavki2=stavki #nadomestna kopija preostalih stavkov
            
            for stavek in stavki2:
                if type(stavek) == Spr and stavek==i.izr: return False                
                elif type(stavek) == Neg and stavek.izr==i.izr: stavki.remove(stavek)

                
                elif type(stavek) == Ali and len(stavek.sez)>1:
                    for lit in stavek.sez:
                        if type(lit) == Spr and lit == i.izr:
                            stavki.remove(stavek)
                            stavki.append(Ali(*tuple(a for a in stavek if a!=i.izr))) #odstrani stari stavek in ga nadomesti z novim, ki nima negacij naše spremenljivke  
                        if type(lit) == Neg and lit.izr == i.izr:
                            stavki.remove(stavek)
                else: print('Napaka pri vstavljanju znanih spr. v preostale stavke 2.')
            

        else:
            for j in i.sez:
                if type(j) == Spr: literal[j.ime] = ''
                elif type(j) == Neg: literal[j.izr.ime] = ''                
                else: print('NAPAKA!')
                
    
    znane = {i: literal[i] for i in literal if literal[i]!=''}
    neznane = {i: literal[i] for i in literal if literal[i]==''}
    
    return literal


def element(s): #vrne edini element v množici in ga pusti notri
    return list(s)[0]
