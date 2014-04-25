# **Projekt: SAT solver**
###Ekipa: -- .- ..-. .. .--- .- 

###### Članici: *Barbara Bajcer* in *Jana Vidrih*  :two_women_holding_hands:


Projekt je sestavljen iz:
* SAT solverja, ki uporablja DPLL algoritem (*sat_solver.py*)
* testnih primerov (*primeri.py*, *generator_primerov.py*)
* primerov uporabe (*sudoku.py*, *povezanost.py*, *barvanje.py*)


##Datoteke

* *izrazi_cnf.py*: V tej datoteki se nahajajo tako definicije razredov logičnih operacij, kot tudi prevedba boolovega izraza na [cnf obliko](http://en.wikipedia.org/wiki/Conjunctive_normal_form).

Primer uporabe:
Boolovo formulo    **(x ∧ y) ∨ ~x ∨ ⊥**   zapišemo kot:  Ali ( In ( Spr('x'), Spr('y') ), Neg(Spr('x') ), F() ).

* *sudoku.py*: Prevedba problema za dani sudoku v boolovo formulo.
* *povezanost.py* in *barvanje.py*: Prevedba problema za dani graf v boolovo formulo. Graf naj bo predstavljen s slovarjem {vozlišče: {sosedi}, vozlišče: {sosedi}, ...}.
* *sat_solver.py*: Vsebuje [dpll](http://www.dis.uniroma1.it/~liberato/ar/dpll/dpll.html) algoritem. Algoritem sva izboljšali s sortiranjem literalov po frekvenci pojavitve.

## Uporaba

* Za zagon testnih primerov, poženi datoteko ..... !!!!
* Za generiranje naključnega primera kliči funkcijo generator_primerov(max število spremenljivk, dolžina formule).
* Za zagon drugih primerov poženi datoteko *sat_solver.py* in v IDLE kliči sat(moj_primer).
