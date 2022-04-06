import random
from operator import attrgetter
import sys
import numpy as np
import math

#1.creem populatia
class Knote:
    def __init__(self, Wert, x, y):
        self.Wert = Wert
        self.x = x
        self.y = y

    def Entfernung(self, other):
        return math.sqrt(pow(self.x - other.x, 2) + pow(self.y - other.y, 2))


# sir de noduri
class Sequenz:
    def __init__(self, Knoten, Gesamtkosten):
        self.Knoten = Knoten
        self.Gesamtkosten = Gesamtkosten

    def get_Gesamtkosten(self):
        return self.Gesamtkosten

    def get_Knoten(self):
        return self.Knoten


def Knotengenerierung():
    Knoten = []
    for i in range(100):
        x = random.randint(-50, 50)
        y = random.randint(-50, 50)
        p = Knote(x, y, i)
        Knoten.append(p)
    return Knoten

#2.determinarea aptitudini
def Kostenmatrixerzeugung(n):
    Matrix = []
    Knoten = Knotengenerierung()

    for i in range(n):
        Entfernungen = []

        for j in range(n):
            Entfernung = Knoten[i].Entfernung(Knoten[j])
            Entfernungen.append(Entfernung)
        Matrix.append(Entfernungen)

    return Matrix


# secventa se modifica prin inversarea ordinii unei submultimi de noduri
def AnderungSequenz(sequenz):
    sequenzErgebnis = []
    for i in range(len(sequenz)):
        sequenzErgebnis.append(0)
    Knote_1 = random.choice(sequenz)
    Knote_2 = random.choice(sequenz)

    if Knote_1 > Knote_2:
        Knote_1, Knote_2 = Knote_2, Knote_1
    x = 0
    for i in range(len(sequenz)):
        if Knote_1 <= i and i <= Knote_2:
            sequenzErgebnis[i] = sequenz[Knote_2 - x]
            x += 1
        else:
            sequenzErgebnis[i] = sequenz[i]
    return sequenzErgebnis

#3.facem imperecherea, reproducem, mutam si repetam
# Intersecteaza doua secvente de noduri
def Kreuzung(n, s1, s2):
    Ergebnis = []  # secventa rezultat
    Nachbarschaft = []  # matrice de adiacenta

    for i in range(n):
        Nachbarschaft.append([])

    for i in range(n):
        j = i % n - 1
        Nachbarschaft[s1[i]].append(s1[j])

        Nachbarschaft[s1[j]].append(s1[i])

        Nachbarschaft[s2[i]].append(s2[j])

        Nachbarschaft[s2[j]].append(s2[i])

    for i in range(len(Nachbarschaft)):
        Nachbarschaft[i] = list(set(Nachbarschaft[i]))

    Ergebnis.append(random.choice([s1[0], s2[0]]))  # Se alege in mod aleatoriu primul nod

    for i in range(n - 1):
        min = sys.maxsize
        nachsterKnoten = 999
        Knoten = []

        for j in range(len(Nachbarschaft[Ergebnis[i]])):
            knote = Nachbarschaft[Ergebnis[i]][j]  # urmatorul nod este ales dintre vecinii nodului actual
            cardinal = len(set(Nachbarschaft[knote]).difference(set(Ergebnis[:i])))

            if cardinal <= min:
                min = cardinal
                nachsterKnoten = knote
                Knoten.append(knote)

        if len(Knoten) > 1:
            nachsterKnoten = random.choice(Knoten)

        Nachbarschaft[Ergebnis[-1]].clear()

        for a in Nachbarschaft:  # Nodurile vizitate se sterg
            if Ergebnis[-1] in a:
                a.remove(Ergebnis[-1])

        if nachsterKnoten != 999:
            Ergebnis.append(nachsterKnoten)
        else:
            Ergebnis.append(random.choice(list(set(range(n)).difference(set(Ergebnis[:i])))))

    return Ergebnis


def Kostenkalkulation(sequenz, kosten):
    cost = kosten[len(sequenz) - 1][sequenz[0]]
    for i in range(len(sequenz) - 1):
        cost += kosten[sequenz[i]][sequenz[i + 1]]
    return cost


def Problemlosung(n):
    kosten = Kostenmatrixerzeugung(n)
    ind = 0
    s = []
    for i in range(4000):
        s.append([])

    for i in range(10):
        perm = np.random.permutation(n)
        secv = Sequenz(perm, Kostenkalkulation(perm, kosten))
        s[ind].append(secv)

    #repetam
    while ind <= 2000:  # se creaza 2000 de generatii
        s2 = []
        for i in range(10):
            s2.append(Sequenz([], sys.maxsize))

        for i in range(1, 41):
            sequenz = random.choice(s[ind])
            while len(sequenz.get_Knoten()) == 0:
                sequenz = random.choice(s[ind])
            rand = random.randint(1, 10)
            if rand < 3:

                sequenz2 = random.choice(s[ind])

                while len(sequenz2.get_Knoten()) == 0:
                    sequenz2 = random.choice(s[ind])

                inter = Kreuzung(n, sequenz.get_Knoten(), sequenz2.get_Knoten())
                sequenz = Sequenz(inter, Kostenkalkulation(inter, kosten))

            inter = AnderungSequenz(sequenz.get_Knoten())
            sequenz = Sequenz(inter, Kostenkalkulation(inter, kosten))

            s2.append(sequenz)

        ind += 1

        for secv in s[ind - 1]:
            s2.append(secv)

        sortat = sorted(s2, key=attrgetter('Gesamtkosten'))

        if ind == 1 or ind == 100 or ind == 500 or ind == 1000 or ind == 1500 or ind == 2000:  # Generatiile 1, 100, 500, 1000, 1500 si 2000 sunt afisate
            print("Generatia", ind)

        x = 1
        for secv in sortat:
            if x <= 10:
                if len(secv.get_Knoten()) != 0:
                    if ind == 1 or ind == 100 or ind == 500 or ind == 1000 or ind == 1500 or ind == 2000:  # Se afiseaza rezultatul
                        print("Ruta", x, ':', secv.get_Knoten())
                        print("Costuri", secv.get_Gesamtkosten(), "\n")

                    s[ind].append(secv)

            x += 1


def main():
    n = 100
    Problemlosung(n)


main()
