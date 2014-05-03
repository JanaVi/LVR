# **Projekt: SAT solver**
###Ekipa: -- .- ..-. .. .--- .- 

###### Članici: *Barbara Bajcer* in *Jana Vidrih*  :two_women_holding_hands:


Projekt je sestavljen iz dveh delov:
* SAT solverja, ki uporablja DPLL algoritem (*sat_solver.py*)
* prevedb problemov na reševanje logičnih izrazov (*sudoku.py*, *hadamard.py*, *barvanje.py*)


##Datoteke

* **izrazi_cnf.py**: V tej datoteki se nahajajo tako definicije razredov spremenljivk in logičnih operacij, kot tudi prevedba logičnega izraza na [CNF obliko](http://en.wikipedia.org/wiki/Conjunctive_normal_form).

Spremenljivke podamo kot: Spr(ime), kjer je ime niz.  
Negacijo izraza podamo kot: Neg(a), kjer je a nek logični izraz.  
Logični operator IN podamo kot: In(a_1, ... , a_n), kjer so a_1, ... , a_n logični izrazi.  
Logični operator ALI podamo kot: Ali(a_1, ... , a_n), kjer so a_1, ... , a_n logični izrazi.  
Vrednost TRUE podamo kot: T().  
Vrednost FALSE podamo kot: F().  

Primer uporabe:  
Boolovo formulo   **(x ∧ y) ∨ ~x ∨ ⊥**   zapišemo kot:  Ali ( In ( Spr('x'), Spr('y') ), Neg(Spr('x') ), F() )..  
Za poljubni izraz nam izraz.cnf() vrne logični izraz v CNF obliki.

* **sudoku.py**: Prevedba problema za dani sudoku v boolovo formulo. Začetne vrednosti naj bodo podane v seznamu:  zacetne = [(i_1,j_1,k_1), (i_2,j_2,k_2), ... , (i_n,j_n,k_n)], kjer prva koordinata označuje vrstico, druga stolpec, tretja pa vrednost na tem polju.

*sudoku_pretvori(zacetne)* nam vrne logični izraz.  
*sudoku(zacetne)* vrne izpisan rešen sudoku (če je ta rešljiv).

* **barvanje.py**: Prevedba problema za dani graf v boolovo formulo. Graf naj bo predstavljen s slovarjem {vozlišče: {sosedi}, vozlišče: {sosedi}, ...}, k naj bo število barv, s katerimi želimo pobarvati naš graf.

*barvanje_pretvori(g,k)* nam vrne logični izraz, s pomočjo katerega ugotovimo, ali je takšno barvanje mogoče.  
*barvanje(g,k)* nam vrne slovar vozlišč z njihovimi barvami (če je takšno barvanje mogoče).

* **hadamard.py**: Prevedba problema za hadamardovo matriko neke dimenzije v boolovo formulo. Naj bo n naravno število.

*hadamard_pretvori(n)* nam vrne logični izraz, s pomočjo katerega lahko ugotovimo, ali obstaja Hadamardova matrika dimenzije n x n.  
*hadamard(n)* nam izpiše takšno matriko (če ta obstaja).

* **sat_solver.py**: Vsebuje [dpll](http://www.dis.uniroma1.it/~liberato/ar/dpll/dpll.html) algoritem. Algoritem sva izboljšali s sortiranjem literalov po frekvenci pojavitve (vzame najpogostejšega) in nato (če jih je več z maksimalno frekvenco) po dolzini najkrajšega stavka, v katerem se določeni literal nahaja.

* **primeri.py**: ...

* **demo.py**: ...

* **generator.py**: ...

* **testiranje.py**: ...


## Uporaba

* Za zagon demonstracije poženi datoteko demo.py. ...
* Za zagon testnih primerov, poženi datoteko tetsiranje. ...
* Za generiranje naključnega izraza kliči funkcijo generiraj(max število spremenljivk, dolžina formule). ...
* Za zagon drugih primerov poženi datoteko *sat_solver.py* in v IDLE kliči sat(moj_primer). ...
