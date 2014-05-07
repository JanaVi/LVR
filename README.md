# **Projekt: SAT solver**
###Ekipa: -- .- ..-. .. .--- .- 

###### Članici: *Barbara Bajcer* in *Jana Vidrih*  :two_women_holding_hands:


Projekt je sestavljen iz dveh delov:
* SAT solverja, ki uporablja DPLL algoritem (*sat.py*, *izrazi_cnf.py*)
* prevedb problemov na reševanje logičnih izrazov (*sudoku.py*, *hadamard.py*, *barvanje.py*)


##Datoteke

* **izrazi_cnf.py**: V tej datoteki se nahajajo tako definicije razredov spremenljivk in logičnih operacij, kot tudi prevedba logičnega izraza na [CNF obliko](http://en.wikipedia.org/wiki/Conjunctive_normal_form).

* **sudoku.py**: Prevedba problema za dani sudoku v boolov izraz. 

* **barvanje.py**: Prevedba problema za dani graf v boolov izraz.

* **hadamard.py**: Prevedba problema za hadamardovo matriko poljubne dimenzije v boolov izraz.

* **sat.py**: Vsebuje [dpll](http://www.dis.uniroma1.it/~liberato/ar/dpll/dpll.html) algoritem. Algoritem sva izboljšali s sortiranjem literalov po frekvenci pojavitve (vzame najpogostejšega) in nato (če jih je več z maksimalno frekvenco) po dolžini najkrajšega stavka, v katerem se določeni literal nahaja.

* **primeri.py**: Vsebuje primere za SAT solver in metodo cnf, sudoku in barvanje grafa.

* **demo.py**: Demonstracija pisanja logičnih izrazov, uporabe SAT solverja in prevedb.

* **generator.py**: Vsebuje funkcijo generiraj, ki nam generira boolovo formulo v cnf obliki.

* **testiranje.py**: Vsebuje dve funkciji. Prvo, ki za dani logični izraz in slovar literalov s pripadajočimi vrednostmi preveri, če tako nastavljeni literali izpolnjujejo dani izraz. In drugo, ki testira večjo količino naključno generiranih primerov (glej spodaj v Uporabi).


## Uporaba

* Za zagon demonstracije poženi datoteko *demo.py*.
* Za generiranje naključnega izraza kliči funkcijo generiraj(max število spremenljivk, dolžina izraza) (v *sat.py* ali *generator.py*). Funkcija vrne izraz v cnf obliki.
* Za zagon testnih primerov odpri datoteko *testiranje.py*. Kliči funkcijo test(n,k,s,izpisuj=False,cas=True). Funkcija testira pravilnost SAT solverja s pomočjo generatorja primerov. Števili n in k označujeta maksimalno število različnih literalov v izrazu in dolžino izraza, s pa označuje, koliko primerov želimo generirati. Za dodatne možnosti izpisovanja pravilnosti in porabljenega časa glej opis funkcije.
* Za ogled že napisanih primerov odpri *primeri.py* in nato v primerni datoteki (za sudoku odpri *sudoku.py*, za reševanje splošnega logičnega izraza *sat.py*, ...) preizkusi te primere.
* Za reševanje poljubnih logičnih izrazov odpri datoteko *sat.py* in kliči sat(moj_primer).


## Opombe

* Za reševanje lažjega sudokuja najin algoritem porabi prb. 20 sekund, ne priporočava reševanje praznega sudokuja ali ekstremno težkih primerov.
