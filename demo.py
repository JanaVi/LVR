from sat import *
from barvanje import *
from hadamard import *
from izrazi_cnf import *
from sudoku import *
from tkinter import *

class Demo():
    def __init__(self, glavnoOkno):
        self.glavnoOkno = glavnoOkno

        self.canvas = Canvas(glavnoOkno, height = 440, width = 200, bd = -2, bg = "LightSkyBlue3")
        self.canvas.grid(row = 0, column=0)
        self.canvas2 = Canvas(glavnoOkno, height = 440, width = 600, bd = -2, bg = 'azure2')
        self.canvas2.grid(row = 0, column = 1)
        
        self.frame = Frame(self.glavnoOkno, height = 300, width = 580, bd = 3, relief = SUNKEN)
        self.frame.place(x = 210, y = 10)
        
        self.obvestilo = StringVar() #obvestila v osrednjem okvirju
        self.obvestilo.set('''Avtorici: Barbara Bajcer in Jana Vidrih''')
        self.obvestila = Label(self.frame, height = 25, width = 71, textvariable = self.obvestilo,
                               font=("Helvetica", 10), background="white", anchor = NW, justify = LEFT)
        self.obvestila.pack()
        
        self.pes = PhotoImage(file = 'pingvin.gif')
        self.lab = Label(self.frame, image = self.pes)
        self.lab.photo = self.pes
        self.lab.place(x = 10, y = 30)
        
        self.izrazi = Button(self.glavnoOkno, text = 'Podajanje logičnih izrazov', command = self.podajanje, bg="LightSkyBlue3", relief = SUNKEN, bd = 1)
        self.izrazi.place(x = 10, y = 10)
        self.primeri = Button(self.glavnoOkno, text = 'Primeri uporabe', command = self.uporaba, bg = "LightSkyBlue3", relief = SUNKEN, bd = 1)
        self.primeri.place(x = 10, y = 40)
        self.prevedbe = Menubutton(self.glavnoOkno, text = 'Prevedbe nekaterih problemov', bg = "LightSkyBlue3", relief = SUNKEN, bd = 1)
        self.prevedbe.place(x = 10, y = 70)
        self.prevedbe.menu = Menu(self.prevedbe, tearoff=0, bg = "LightSkyBlue3")
        self.prevedbe.menu.add_command(label = 'Sudoku', command = self.sudoku)
        self.prevedbe.menu.add_command(label = 'Barvanje grafa', command = self.barvanje)
        self.prevedbe.menu.add_command(label = 'Hadamard', command = self.hadamard)
        self.prevedbe.config(menu = self.prevedbe.menu)

    def podajanje(self):
        self.lab.destroy()
        self.obvestilo.set('''Podajanje logičnih izrazov:

- Spremenljivke podamo kot: Spr(ime), kjer je ime niz.
- Negacijo izraza podamo kot: Neg(a), kjer je a nek logični izraz.
- Logični operator IN podamo kot: In(a_1, ... , a_n), kjer so a_1, ... , a_n logični izrazi.
- Logični operator ALI podamo kot: Ali(a_1, ... , a_n), kjer so a_1, ... , a_n logični izrazi.
- Vrednost TRUE podamo kot: T().
- Vrednost FALSE podamo kot: F().

Primer:  ( ¬a ∧ b ) ∨ b ∨ ⊥  zapišemo kot:  Ali ( In ( Neg(Spr('a')), Spr('b') ), Spr('b'), F() )''')

    def uporaba(self):
        self.lab.destroy()
        primer_1 = Ali(a,b)
        primer_2 = Ali(In(a,Neg(b),c),a)
        primer_3 = Ali(e,In(a,Ali(a,Neg(b),d),c))
        primer_4 = In(F(),a)
        
        self.obvestilo.set('''- Klic sat(izraz)  nam vrne slovar spremenljivk in njihovih boolovih vrednosti, ki zadostijo temu,
da je izraz rešljiv.
- izraz.cnf()  nam vrne izraz v CNF obliki. \n

primer_1 = {0}
primer_1.cnf() = {1}
sat(primer_1) = {2}

primer_2 = {3}
primer_2.cnf() = {4}
sat(primer_2) = {5}

primer_3 = {6}
primer_3.cnf() = {7}
sat(primer_3) = {8}


Če spremenljivkam v izrazu ne moremo določiti takšne vrednosti, da bi bil izraz resničen, nam
funkcija vrne niz 'Izraz ni rešljiv.'

primer_4 = {9}
primer_4.cnf() = {10}
sat(primer_4) = {11}'''.format(primer_1, primer_1.cnf(), sat(primer_1), primer_2, primer_2.cnf(), sat(primer_2), primer_3, primer_3.cnf(),
                               sat(primer_3), primer_4, primer_4.cnf(), sat(primer_4)))

    def sudoku(self):
        self.lab.destroy()
        self.obvestilo.set('''Naj bo zacetne = [(i_1,j_1,k_1), (i_2,j_2,k_2), ... , (i_n,j_n,k_n)] seznam začetnih vrednosti. Prva
koordinata označuje vrstico, druga stolpec, tretja pa vrednost na tem polju.

- sudoku_pretvori(zacetne)  nam vrne logični izraz, ki ga lahko podamo SAT solverju.

- sudoku(zacetne)  nam vrne izpisan rešen sudoku (če je ta rešljiv, sicer vrne niz 'Sudoku s tako
  podanimi začetnimi vrednostmi ni rešljiv.').

primer = [(1,1,9),(1,2,2),(1,5,1),(1,6,5),(2,3,5),(2,8,6),
              (3,1,6),(3,2,1),(3,4,3),(3,9,4),(4,1,2),(4,2,8),(4,5,4),
              (5,1,1),(5,5,3),(5,9,6),(6,5,8),(6,8,9),(6,9,5),
              (7,1,4),(7,6,9),(7,8,5),(7,9,3),(8,2,9),(8,7,6),
              (9,4,8),(9,5,6),(9,8,4),(9,9,1)]

sudoku(primer) = 9 2 4 | 6 1 5 | 7 3 8 
                          7 3 5 | 4 2 8 | 1 6 9 
                          6 1 8 | 3 9 7 | 5 2 4 
                         -- -- -- -- -- -- -- -- -- --
                          2 8 9 | 5 4 6 | 3 1 7 
                          1 5 7 | 9 3 2 | 4 8 6 
                          3 4 6 | 7 8 1 | 2 9 5 
                         -- -- -- -- -- -- -- -- -- --
                          4 6 1 | 2 7 9 | 8 5 3 
                          8 9 3 | 1 5 4 | 6 7 2 
                          5 7 2 | 8 6 3 | 9 4 1 ''')

    def barvanje(self):
        self.lab.destroy()
        g1 = {'a':{'b'},'b':{'a','c'},'c':{'b','d'},'d':{'c','e'},'e':{'d'}}
        g2 = {1:{2,3,4,5},2:{1,3,4,5},3:{1,2,4,5},4:{1,2,3,5},5:{1,2,3,4}} #poln graf

        self.obvestilo.set('''Graf predstavimo s slovarjem g = {vozlišče: {sosedi}, vozlišče: {sosedi}, ...}. Naj bo k število barv,
s katerimi želimo pobarvati naš graf.

- barvanje_pretvori(g,k)  nam vrne logični izraz, s pomočjo katerega ugotovimo, ali je takšno
  barvanje mogoče.

- barvanje(g,k)  nam vrne slovar vozlišč z njihovimi barvami (če k-barvanje za naš graf obstaja,
  sicer vrne niz 'Takšno barvanje grafa ni mogoče.').'''+'''


g1 = {0}
barvanje(g1,2) = {1}


g2 = {2}   #poln graf na petih vozliščih
barvanje(g2,4) = {3}
'''.format(g1,barvanje(g1,2),g2,barvanje(g2,4)))

    def hadamard(self):
        self.lab.destroy()
        self.obvestilo.set('''Naj bo n naravno število.

- hadamard_pretvori(n)  nam vrne logični izraz, s pomočjo katerega lahko ugotovimo, ali
  obstaja Hadamardova matrika dimenzije n x n.

- hadamard(n)  nam takšno matriko izpiše (če obstaja, sicer vrne niz 'Ne obstaja Hadamardova
  matrika te dimezije.').


hadamard(3) = {0}


hadamard(4) =  1  1  1  1 
                       1 -1 -1  1 
                       1  1 -1 -1 
                       1 -1  1 -1 '''.format(hadamard(3)))


koren = Tk()
koren.title('')
koren.minsize(800,435)
koren.maxsize(800,435)
demo = Demo(koren)
koren.mainloop()
