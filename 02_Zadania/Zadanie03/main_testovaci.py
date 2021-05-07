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
        file_content = [x.strip() for x in f.readlines()]
    file_content = pd.Series(file_content).str.split()

    # pocet premennych a klauzul
    nb_var = int(file_content[0][0])
    nb_clauses = int(file_content[0][1])

    print("- nbvar:", nb_var)
    print("- nbclauses:", nb_clauses)

    # klauzuly (A v B)
    litA = []
    litB = []
    for i, row in enumerate(file_content[1:]):
        # (A v B) alebo (A v A)
        litA.append(int(row[0]))
        litB.append(int(row[0]) if len(row) == 2 else int(row[1]))

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
    :return:
    """
    if result:
        print(colored("SPLNITEĽNÁ", color="green"))
    else:
        print(colored("NESPLNITEĽNÁ", color="red"))

    for i, value in enumerate(assignment):
        print(("PRAVDA     <-- x" + str(i+1)) if value else "NEPRAVDA   <-- x" + str(i+1))


def test_TODO_DEL():
    main("sat.txt")   # sat T F
    main("sat1.txt")  # sat T F T F
    main("sat2.txt")  # unsat
    main("sat3.txt")  # sat T T T
    main("sat4.txt")  # unsat

    main("sat5.txt")  # sat T F T T F F T F T
    main("sat6.txt")  # sat F T
    main("sat7.txt")  # sat T F F T F
    main("sat8.txt")  # sat F T
    main("sat9.txt")  # unsat

    main("sat10.txt")  # sat T T T
    main("sat11.txt")  # unsat
    main("sat12.txt")  # unsat
    main("sat13.txt")  # unsat
    main("sat14.txt")  # sat T T T T T T T


def main(filename):
    nb_var, nb_clauses, litA, litB = load(filename)
    # vytvorenie grafu
    graph = Graph(nb_var, nb_clauses, litA, litB)
    # vysledky
    result, assignment = graph.is_2SAT()
    # vypis
    print_formula([(litA[i], litB[i]) for i in range(nb_clauses)])
    print_results(result, assignment)


if __name__ == '__main__':
    # main("sat.txt")  # sat T F
    test_TODO_DEL()

