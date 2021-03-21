from time import sleep
import operator
import pandas as pd
import numpy as np
from termcolor import colored
from tqdm import tqdm
from classes import Tree, Word

''' ******************************************* POMOCNE FUNKCIE ***********************************************'''


def range_inclusive(start, stop):
    """
    Range <start,stop>, kde start aj stop patria do intervalu
    """
    return range(start, stop + 1)


def load_dictionary(filename):
    """
    Nacitanie slovnika zo suboru + lexikograficke usporiadanie
    :param filename: nazov suboru
    :return: word_list (lexikograficky usporiadane), freq_sum (celkova frekvencia)
    """

    word_list = []
    freq_sum = 0

    # nacitanie zo suboru
    with open(filename) as f:
        for line in f:
            freq, val = line.split()
            word_list.append(Word(int(freq), val))
            freq_sum += int(freq)

    # lexikograficke usporiadanie slov
    word_list_sorted = sorted(word_list, key=operator.attrgetter('value'))

    return word_list_sorted, freq_sum


def search_all(search_tree, word_list):
    """
    Prehladavanie vsetkych slov z dictionary.txt
    :param search_tree: vyhladavaci strom
    :param word_list: pole slov Word(frequency, value)
    """

    to_write = ""
    for w in word_list:
        comp = pocet_porovnani(search_tree, w.value, print_results=False)
        to_write += w.value + ":" + str(comp) + "\n"

    with open("search.txt", "w") as f:
        f.write(to_write)
    print(colored("   ulozene do suboru search.txt", color="green"))


''' ************************************************ BST ****************************************************'''


def get_keys(word_list, freq_sum):
    """
    Nacitanie klucov a pravdepodobnosti zo slov
    :param word_list: pole slov Word(frequency, value)
    :param freq_sum: celkova frekvencia
    :return: key_words, key_probabilities, dummy_probabilities, KEYS_COUNT
    """

    key_words = []  # pole klucov (k)
    key_probabilities = []  # pravdepodobnosti klucov (p)
    dummy_probabilities = []  # pravdepodobnosti dummy (q)

    frequency_between = 0  # q_0 = 0 / freq_sum

    for word in word_list:
        if word.frequency <= 50000:  # slova medzi klucmi k_i a k_i+1
            frequency_between += word.frequency

        else:  # novy kluc k_i
            key_words.append(word.value)  # k_i
            key_probabilities.append(word.frequency / freq_sum)  # p_i
            dummy_probabilities.append(frequency_between / freq_sum)  # q_i
            frequency_between = 0
    # q_n
    dummy_probabilities.append(frequency_between / freq_sum)

    KEYS_COUNT = len(key_words)

    # pd.Series s posunutym indexom 1..n
    key_words = pd.Series(key_words, index=range_inclusive(1, KEYS_COUNT))  # k[1..n]
    key_probabilities = pd.Series(key_probabilities, index=range_inclusive(1, KEYS_COUNT))  # p[1..n]

    dummy_probabilities = pd.Series(dummy_probabilities)  # q[0..n]

    return key_words, key_probabilities, dummy_probabilities, KEYS_COUNT


def optimal_BST(p, q, KEYS_COUNT):
    """
    Vytvorenie optimalneho BST
    zdroj: https://edutechlearners.com/download/Introduction_to_algorithms-3rd%20Edition.pdf#page=423
    :param p: pravdepodobnosti klucov p[1..n]
    :param q: dummy pravdepodobnosti  q[0..n]
    :param KEYS_COUNT: pocet klucov (151)
    :return: COST_TABLE (tabulka optimalnych cien), ROOT_TABLE (tabulka root indexov)
    """

    # COST_TABLE[1..n+1, 0..n]
    COST_TABLE = pd.DataFrame(np.diag(q),  # na diagonale su pravdepodobnosti q_i
                              index=range_inclusive(1, KEYS_COUNT + 1))  # [1..n+1] x [0..n]

    # PROBABILITY_SUM_TABLE[1..n+1, 0..n]
    PROBABILITY_SUM_TABLE = COST_TABLE.copy()

    # ROOT_TABLE[1..n, 1..n]
    ROOT_TABLE = pd.DataFrame(np.zeros((KEYS_COUNT, KEYS_COUNT)),  # matica naplnena nulami
                              index=range_inclusive(1, KEYS_COUNT),  # [1..n] x [1..n]
                              columns=range_inclusive(1, KEYS_COUNT),
                              dtype=int)

    for x in tqdm(iterable=range_inclusive(1, KEYS_COUNT)):  # riadky matice 1..n
        for i in range_inclusive(1, KEYS_COUNT - x + 1):  # stlpce matice 1..n-x+1
            j = i + x - 1  # posunutie nad diagonalu matice
            COST_TABLE.at[i, j] = np.inf

            # suma pravdepodobnosti pre p a q
            PROBABILITY_SUM_TABLE.at[i, j] = PROBABILITY_SUM_TABLE.at[i, j - 1] + p.get(j) + q.get(j)

            # prechadzam vsetky kluce s id = i..j a hladam, ktory z nich moze byt root
            for root_tmp in range_inclusive(i, j):

                cost_left = COST_TABLE.at[i, root_tmp - 1]  # cena laveho podstromu (bunka vlavo)
                cost_right = COST_TABLE.at[root_tmp + 1, j]  # cena praveho podstromu (bunka dole)
                probability_current = PROBABILITY_SUM_TABLE.at[i, j]  # suma pravdepodobnosti pre aktualny uzol

                # nova cena = cena laveho podstromu + praveho podstromu + pravdepodobnost aktualneho uzla
                cost_tmp = cost_left + cost_right + probability_current

                # najde sa minimum z aktualnej ceny ulozenej v COST_TABLE a novej vypocitanej ceny
                if cost_tmp < COST_TABLE.at[i, j]:
                    COST_TABLE.at[i, j] = cost_tmp
                    ROOT_TABLE.at[i, j] = root_tmp

    return COST_TABLE, ROOT_TABLE


def build_tree(keys, ROOT_TABLE, i, j):
    """
    Vytvorenie stromu podla ROOT_TABLE
    zdroj: https://github.com/CarterZhou/algorithms_practice/blob/master/dp/OptimalBST.java
    :param keys: kluce [1..n]
    :param ROOT_TABLE: tabulka root uzlov pre rozne podstromy
    :param i: index riadku ROOT_TABLE
    :param j: index stlpca ROOT_TABLE
    :return: search_tree
    """

    # index rootu aktualneho podstromu (so suradnicami [i, j] v ROOT_TABLE)
    root_id = ROOT_TABLE.at[i, j]
    # novy podstrom
    search_tree = Tree(keys.get(root_id))

    # rekurzivne do laveho podstromu
    if i < root_id:
        search_tree.set_left_subtree(
            build_tree(keys, ROOT_TABLE, i, root_id - 1))  # root podstromu v bunke vlavo

    # rekurzivne do praveho podstromu
    if j > root_id:
        search_tree.set_right_subtree(
            build_tree(keys, ROOT_TABLE, root_id + 1, j))  # root podstromu v bunke dole

    return search_tree


def pocet_porovnani(node, search_string, comparisons=1, print_results=True):
    """
    Funkcia vrati pocet porovnani, ktore sa vykonaju pocas hladania vstupneho retazca
    v zostrojenom optimalnom binarnom vyhladavacom strome.
    zdroj: https://www.geeksforgeeks.org/binary-search-tree-set-1-search-and-insertion/
    :param node: aktualny uzol stromu
    :param search_string: hladane slovo
    :param comparisons: pocet porovnani
    :param print_results: zobrazit vypisy? true/false
    :return: pocet porovnani
    """
    # vypis
    if print_results:
        print_comparison(node, comparisons, search_string)

    # dostal sa na dummy kluc alebo bol najdeny medzi klucmi
    if node is None or node.value == search_string:
        return comparisons

    LEFT = node.left_subtree  # lavy podstrom
    RIGHT = node.right_subtree  # pravy podstrom
    CURRENT = node.value  # aktualny uzol

    # retazec je mensi - ide do laveho podstromu
    if search_string < CURRENT:
        return pocet_porovnani(LEFT, search_string, comparisons + 1, print_results)

    # retazec je vacsi - ide do praveho podstromu
    return pocet_porovnani(RIGHT, search_string, comparisons + 1, print_results)


def print_comparison(node, comparisons, search_string):
    """
    Vypis pre aktualne porovnanie retazcov
    :param node: aktualny uzol stromu
    :param comparisons: poradove cislo porovnania
    :param search_string: hladane slovo
    """

    # dostane sa na dummy kluc
    if node is None:
        print("\nPorovnanie", str(comparisons + 1) + ":",
              colored("\n  -- DUMMY kluc: " + search_string + " --", "green", attrs=['bold']),
              "\n  Hladany retazec:", colored(search_string, "green", attrs=['bold']),
              "\n  Zhoda:", colored(True, "green", attrs=['bold']),
              "\n\n*******************")

    # medzivysledok
    else:
        color = "green" if node.value == search_string else "red"
        print("\nPorovnanie", str(comparisons) + ":",
              "\n  Aktualny kluc:", colored(node.value, color, attrs=['bold']),
              "\n  Hladany retazec:", colored(search_string, color, attrs=['bold']),
              "\n  Zhoda:", colored(node.value == search_string, color, attrs=['bold']),
              "\n\n*******************")


''' ************************************************ MAIN ****************************************************'''

if __name__ == '__main__':

    # nacitanie a vytvorenie klucov a pravdepodobnosti

    words, freq_sum = load_dictionary("dictionary.txt")
    keys, key_prob, dummy_prob, n = get_keys(words, freq_sum)

    # strom

    print(colored("\n***** Optimalny binarny vyhladavaci strom ******\n", color="cyan"))
    cost_tab, root_tab = optimal_BST(key_prob, dummy_prob, n)
    print("\nOptimalna cena: ", cost_tab.at[1, n])  # optimalna cena hladania
    tree = build_tree(keys, root_tab, 1, n)  # vytvorenie stromu

    sleep(0.5)
    print(colored("\n*************** Urovne stromu: ****************", color="cyan"))
    tree.print_levels(save_to_file=True)
    sleep(0.5)

    # pocet porovnani

    print(colored("\n*************** Pocet porovnani ****************\n", color="cyan"))

    print("-- test --\n")
    test_words = ["slaughter", "the", "i", "lasagna", "aaagh", "maths", "banana", "must"]
    for word in test_words:
        comparisons = pocet_porovnani(tree, word, print_results=False)
        print("   " + word + ":", colored(comparisons, "green", attrs=["bold"]))

    print("\n-- vsetky slova z dictionary.txt --")
    search_all(tree, words)
