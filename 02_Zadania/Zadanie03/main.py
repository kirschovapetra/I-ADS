"""
Zadanie 3: Program s polynomiálnou zložitosťou zistí, či je vstupná formula splniteľná alebo nie je splniteľná
    * vypíše na obrazovku SPLNITEĽNÁ/NESPLNITEĽNÁ
    * Splniteľná => vypíše pre jednotlivé booleovské premenné pravdivostné hodnoty (PRAVDA/NEPRAVDA)

Vstup:
2 3             <- nbvar (Počet booleovských premenných=2) nbclauses (klauzuly=3)
1 2 0           <- klauzula (x1 OR x2)
-1 -2 0         <- klauzula (x1' OR x2')
1 0             <- klauzula (x1)

Vystup:
SPLNITEĽNÁ
PRAVDA
NEPRAVDA

* Literály v nich sa zapisujú číslom booleovskej premennej (od 1 po nbvar)
* negovaná booleovská premenná má pred svojím poradovým číslom znak -.
* Klauzula je ukončená znakom 0.

Zdroje:
https://cp-algorithms.com/graph/2SAT.html
https://www.programiz.com/dsa/strongly-connected-components
https://www.geeksforgeeks.org/2-satisfiability-2-sat-problem/
"""

import pandas as pd
from termcolor import colored
from graph import Graph


def load(filename):
    """
    Nacitanie vstupneho suboru
    :param filename: nazov suboru
    :return: nb_var (pocet premennych), nb_clauses (pocet klauzul),
             litA[] (literaly #1 v klauzulach), litB[] (literaly #2 v klauzulach)
    """

    print(colored("\n-- " + filename + " --", color="cyan"))

    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")

    # konvert na int
    file_content = [x.strip() for x in lines]
    file_content = pd.Series(file_content).str.split()
    file_content = [list(map(int, x)) for x in file_content]

    if len(file_content[0]) < 2:
        raise ValueError("Nespravny format vstupneho suboru")

    # pocet premennych a klauzul
    nb_var = file_content[0][0]
    nb_clauses = file_content[0][1]
    print("- nbvar:", nb_var)
    print("- nbclauses:", nb_clauses)

    # klauzuly (A v B)
    litA = []
    litB = []
    for i, row in enumerate(file_content[1:]):
        if row[-1] != 0 or len(row) > 3:
            raise ValueError("Nespravny format vstupneho suboru")
        # (A v B) alebo (A v A)
        litA.append(row[0])
        litB.append(row[0] if len(row) == 2 else row[1])

    return nb_var, nb_clauses, litA, litB


def print_formula(formula):
    """
    Vypis formuly
    :param formula: zoznam tuples (A,B)
    """

    print("- formula: ", end="")
    for i, clause in enumerate(formula):
        if i != 0:
            print(" & ", end="")
        literalA = "x"+str(clause[0]) if clause[0] > 0 else "-x"+str(-clause[0])
        literalB = "x"+str(clause[1]) if clause[1] > 0 else "-x"+str(-clause[1])
        print("(" + literalA + " v " + literalB + ")", end="")
    print()


def print_results(result, assignment):
    """
    Vypis vysledku SAT
    :param result: splnitelost true/false
    :param assignment: priradenie bool hodnot premennym
    """
    if result:
        print(colored("SPLNITEĽNÁ", color="green"))
    else:
        print(colored("NESPLNITEĽNÁ", color="red"))

    for i, value in enumerate(assignment):
        print(("PRAVDA     <-- x" + str(i+1)) if value else "NEPRAVDA   <-- x" + str(i+1))


def main(filename):
    try:
        # nacitanie suboru, graf
        nb_var, nb_clauses, litA, litB = load(filename)
        graph = Graph(nb_var, nb_clauses, litA, litB)
        # vysledky
        result, assignment = graph.is_2SAT()
        print_formula([(litA[i], litB[i]) for i in range(nb_clauses)])
        print_results(result, assignment)
    except ValueError as err:
        print(colored(err, color="red"))


if __name__ == '__main__':
    main("priklad3.txt")
