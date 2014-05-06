# **Projekt: SAT solver**
###Ekipa: -- .- ..-. .. .--- .- 

###### Članici: *Barbara Bajcer* in *Jana Vidrih*  :two_women_holding_hands:


Projekt je sestavljen iz dveh delov:
* SAT solverja, ki uporablja DPLL algoritem (*sat_solver.py*)
* prevedb problemov na reševanje logičnih izrazov (*sudoku.py*, *hadamard.py*, *barvanje.py*)


##Datoteke

* **izrazi_cnf.py**: V tej datoteki se nahajajo tako definicije razredov spremenljivk in logičnih operacij, kot tudi prevedba logičnega izraza na [CNF obliko](http://en.wikipedia.org/wiki/Conjunctive_normal_form).

* **sudoku.py**: Prevedba problema za dani sudoku v boolovo formulo. 

* **barvanje.py**: Prevedba problema za dani graf v boolovo formulo.

* **hadamard.py**: Prevedba problema za hadamardovo matriko neke dimenzije v boolovo formulo.

* **sat_solver.py**: Vsebuje [dpll](http://www.dis.uniroma1.it/~liberato/ar/dpll/dpll.html) algoritem. Algoritem sva izboljšali s sortiranjem literalov po frekvenci pojavitve (vzame najpogostejšega) in nato (če jih je več z maksimalno frekvenco) po dolzini najkrajšega stavka, v katerem se določeni literal nahaja.

* **primeri.py**: Vsebuje primere za SAT solver in metodo cnf, sudoku in barvanje grafa.

* **demo.py**: Demonstracija pisanja logičnih izrazov, uporabe SAT solverja in prevedb.

* **generator.py**: ...

* **testiranje.py**: ...


## Uporaba

* Za zagon demonstracije poženi datoteko demo.py.
* Za zagon testnih primerov odpri datoteko testiranje.py. ...
* Za generiranje naključnega izraza kliči funkcijo generiraj(max število spremenljivk, dolžina formule). ...
* Za zagon drugih primerov poženi datoteko *sat_solver.py* in v IDLE kliči sat(moj_primer). ...
