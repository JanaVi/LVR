# **Projekt: SAT solver**
###Ekipa: -- .- ..-. .. .--- .- 

###### Članice: *Barbara Bajcer* in *Jana Vidrih*  :two_women_holding_hands:


Projekt je sestavljen iz:
* SAT solverja, ki uporablja DPLL algoritem (*sat_solver.py*)
* testnih primerov (*primeri.py*, *generator_primerov.py*)
* primerov uporabe (*sudoku.py*, *povezanost_barvanje.py*)



Boolovo formulo    (x ∧ y) ∨ x ∨ False    zapišemo kot:  Ali(In(Spr('x'),Spr('y')),Spr('x'),F()).

* V datoteki *izrazi_cnf.py* se nahajajo definicije teh logičnih objektov, kot tudi prevedba boolovega izraza na [cnf obliko](http://en.wikipedia.org/wiki/Conjunctive_normal_form).
* *sudoku.py* prevede problem za dani sudoku v boolovo formulo.
* *povezanost_barvanje.py* prevede problem za dani graf v boolovo formulo.
* *sat_solver.py* vsebuje kodo dpll

## Uporaba

* Za zagon testnih primerov, poženi datoteko ..... !!!!
* Za generiranje naključnega primera kliči funkcijo generator_primerov
* Za zagon drugih primerov poženi datoteko *sat_solver.py* in v IDLE kliči sat('moj_primer').
Formula mora biti v cnf obliki. Če ni, jo v cnf obliko prevedemo s klicem 'moj_primer'.cnf()
