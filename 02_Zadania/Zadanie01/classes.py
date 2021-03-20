from termcolor import colored


class Word:
    def __init__(self, frequency, value):
        self.frequency = frequency
        self.value = value


class Tree:
    def __init__(self, value):
        self.value = value          # hodnota kluca
        self.left_subtree = None    # lavy podstrom
        self.right_subtree = None   # pravy podstrom

    def set_left_subtree(self, left_sub):
        self.left_subtree = left_sub

    def set_right_subtree(self, right_sub):
        self.right_subtree = right_sub

    def pocet_porovnani(self, search_string, comparisons=1, print_results=True):
        """
        Funkcia vrati pocet porovnani, ktore sa vykonaju pocas hladania vstupneho retazca
        v zostrojenom optimalnom binarnom vyhladavacom strome.
        :param search_string: hladane slovo
        :param comparisons: pocet porovnani
        :param print_results: zobrazit vypisy? true/false
        :return: pocet porovnani
        """

        LEFT = self.left_subtree    # lavy podstrom
        RIGHT = self.right_subtree  # pravy podstrom
        CURRENT = self.value        # aktualny uzol

        if print_results:
            self.print_comparison(comparisons, search_string)

        # retazec je mensi => ide do laveho podstromu
        if search_string < CURRENT:

            # rekurzivne do laveho podstromu, o 1 viac porovnani
            if LEFT is not None:
                return LEFT.pocet_porovnani(search_string, comparisons + 1, print_results)

            # koniec stromu => dostal sa na dummy kluc
            if print_results:
                self.print_comparison(comparisons, search_string, dummy=True)
            return comparisons + 1

        # retazec je vacsi => ide do praveho podstromu
        elif search_string > CURRENT:

            # rekurzivne do praveho podstromu, o 1 viac porovnani
            if RIGHT is not None:
                return RIGHT.pocet_porovnani(search_string, comparisons + 1, print_results)

            # koniec stromu => dostal sa na dummy kluc
            if print_results:
                self.print_comparison(comparisons, search_string, dummy=True)
            return comparisons + 1

        # retazec bol najdeny medzi klucmi
        return comparisons

    def print_comparison(self, comparisons, search_string, dummy=False):
        """
        Vypis pre aktualne porovnanie retazcov
        :param comparisons: poradove cislo porovnania
        :param search_string: hladane slovo
        :param dummy: dostal sa na dummy kluc? True/False
        """

        # dostane sa na dummy kluc
        if dummy:
            print("\nPorovnanie", str(comparisons + 1) + ":",
                  colored("\n  -- DUMMY kluc: " + search_string + " --", "green", attrs=['bold']),
                  "\n  Hladany retazec:", colored(search_string, "green", attrs=['bold']),
                  "\n  Zhoda:", colored(True, "green", attrs=['bold']),
                  "\n\n*******************")

        # medzivysledok
        else:
            color = "green" if self.value == search_string else "red"
            print("\nPorovnanie", str(comparisons) + ":",
                  "\n  Aktualny kluc:", colored(self.value, color, attrs=['bold']),
                  "\n  Hladany retazec:", colored(search_string, color, attrs=['bold']),
                  "\n  Zhoda:", colored(self.value == search_string, color, attrs=['bold']),
                  "\n\n*******************")

    def print_levels(self, save_to_file=False):
        """
        Vypis stromu po leveloch
        zdroj: https://www.geeksforgeeks.org/print-level-order-traversal-line-line/
        """
        output = ""
        queue = [self]

        # prechadzaju sa levely
        i = 1
        while queue:
            output += "\n--------------------------------\nLevel "+str(i) + ":\n"
            # prechadzaju sa uzly j v i-tom leveli
            j = len(queue)
            while j > 0:
                # zoberie sa uzol zo zaciatku queue
                temp = queue.pop(0)
                output += temp.value + "  "

                # enqueue vsetky uzly v lavom podstrome
                if temp.left_subtree:
                    queue.append(temp.left_subtree)

                # enqueue vsetky uzly v pravom podstrome
                if temp.right_subtree:
                    queue.append(temp.right_subtree)
                j -= 1
            i += 1

        if save_to_file:
            with open("tree.txt", "w") as f:
                f.write(output)

        print(output)
