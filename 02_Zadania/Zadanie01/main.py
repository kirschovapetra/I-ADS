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
    :return: words (lexikograficky usporiadane), freq_sum (celkova frekvencia)
    """

    words = []
    freq_sum = 0

    # nacitanie zo suboru
    with open(filename) as f:
        for line in f:
            freq, val = line.split()
            words.append(Word(int(freq), str(val)))
            freq_sum += int(freq)

    # lexikograficke usporiadanie slov
    return sorted(words, key=operator.attrgetter('value')), freq_sum


def search_all(tree, words):
    """
    Prehladavanie vsetkych slov z dictionary.txt
    :param tree: strom
    :param words: pole slov = Word(frequency, value)
    """

    to_write = ""
    for w in words:
        comparisons = tree.pocet_porovnani(search_string=w.value, print_results=False)
        to_write += w.value + ":" + str(comparisons)+"\n"

    with open("search.txt", "w") as f:
        f.write(to_write)
    print(colored("   ulozene do suboru search.txt", color="green"))


''' ************************************************ BST ****************************************************'''


def get_keys(words, freq_sum):
    """
    Nacitanie klucov a pravdepodobnosti zo slov
    :param words: slova z dictionary.txt = Word(frequency, value)
    :param freq_sum: celkova frekvencia
    :return: key_words, key_probabilities, dummy_probabilities, KEYS_COUNT
    """

    key_words = []              # k[]
    key_probabilities = []      # p[]
    dummy_probabilities = []    # q[]

    frequency_between = 0       # q_0 = 0 / freq_sum

    for word in words:
        if word.frequency <= 50000:  # slova medzi klucmi k_i a k_i+1
            frequency_between += word.frequency

        else:  # novy kluc k_i
            key_words.append(word.value)  # k_i
            key_probabilities.append(word.frequency / freq_sum)       # p_i
            dummy_probabilities.append(frequency_between / freq_sum)  # q_i
            frequency_between = 0
    # q_n
    dummy_probabilities.append(frequency_between / freq_sum)

    KEYS_COUNT = len(key_words)

    # pd.Series s posunutym indexom 1..n
    key_words = pd.Series(key_words, index=range_inclusive(1, KEYS_COUNT))  # k[1..n]
    key_probabilities = pd.Series(key_probabilities,  index=range_inclusive(1, KEYS_COUNT))  # p[1..n]

    dummy_probabilities = pd.Series(dummy_probabilities)  # q[0..n]

    return key_words, key_probabilities, dummy_probabilities, KEYS_COUNT


def optimal_BST(p, q, KEYS_COUNT):
    """
    Vytvorenie optimalneho BST
    :param p: pravdepodobnosti klucov p[1..n]
    :param q: dummy pravdepodobnosti  q[0..n]
    :param KEYS_COUNT: pocet klucov = 151
    :return: COST_TABLE, ROOT_TABLE
    """

    # COST_TABLE[1..n+1, 0..n]
    COST_TABLE = pd.DataFrame(np.diag(q),  # na diagonale su pravdepodobnosti q_i
                              index=range_inclusive(1, KEYS_COUNT + 1))  # [1..n+1] x [0..n]

    # PROBABILITY_SUM_TABLE[1..n+1, 0..n]
    PROBABILITY_SUM_TABLE = COST_TABLE.copy()

    # ROOT_TABLE[1..n, 1..n]
    ROOT_TABLE = pd.DataFrame(np.zeros((KEYS_COUNT, KEYS_COUNT)),    # matica naplnena nulami
                              index=range_inclusive(1, KEYS_COUNT),  # [1..n] x [1..n]
                              columns=range_inclusive(1, KEYS_COUNT),
                              dtype=int)

    for x in tqdm(iterable=range_inclusive(1, KEYS_COUNT)):  # riadky matice
        for i in range_inclusive(1, KEYS_COUNT - x + 1):     # stlpce matice
            j = i + x - 1  # posunutie nad diagonalu matice
            COST_TABLE.at[i, j] = np.inf

            # suma pravdepodobnosti pre p a q
            PROBABILITY_SUM_TABLE.at[i, j] = PROBABILITY_SUM_TABLE.at[i, j - 1] + p.get(j) + q.get(j)

            # prechadzam vsetky kluce s id = i..j a hladam, ktory z nich moze byt root
            for root_tmp in range_inclusive(i, j):

                cost_left = COST_TABLE.at[i, root_tmp - 1]              # cena laveho podstromu (bunka vlavo)
                cost_right = COST_TABLE.at[root_tmp + 1, j]             # cena praveho podstromu (bunka dole)
                probability_current = PROBABILITY_SUM_TABLE.at[i, j]    # suma pravdepodobnosti pre aktualny uzol

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

    # lavy podstrom = mensie indexy i (riadky)
    if i < root_id:
        # rekurzivne do laveho podstromu
        search_tree.set_left_subtree(
            build_tree(keys, ROOT_TABLE, i, root_id - 1))  # root podstromu v bunke vlavo

    # pravy podstrom = vacsie indexy j (stlpce)
    if j > root_id:
        # rekurzivne do praveho podstromu
        search_tree.set_right_subtree(
            build_tree(keys, ROOT_TABLE, root_id + 1, j))  # root podstromu v bunke dole

    return search_tree


''' ************************************************ MAIN ****************************************************'''


if __name__ == '__main__':

    # nacitanie a vytvorenie klucov a pravdepodobnosti

    words, freq_sum = load_dictionary("dictionary.txt")
    key_words, key_probabilities, dummy_probabilities, KEYS_COUNT = get_keys(words, freq_sum)

    # strom

    print(colored("\n***** Optimalny binarny vyhladavaci strom ******\n", color="cyan"))
    cost_tab, root_tab = optimal_BST(key_probabilities, dummy_probabilities, KEYS_COUNT)
    print("\nOptimalna cena: ", cost_tab.at[1, KEYS_COUNT])     # optimalna cena hladania
    tree = build_tree(key_words, root_tab, 1, KEYS_COUNT)       # vytvorenie stromu

    sleep(0.5)
    print(colored("\n*************** Urovne stromu: ****************", color="cyan"))
    tree.print_levels(save_to_file=True)
    sleep(0.5)

    # pocet porovnani

    print(colored("\n*************** Pocet porovnani ****************\n",color="cyan"))

    print("-- test --\n")
    test_words = ["the", "i", "lasagna", "aaagh", "maths", "banana", "must"]
    for word in test_words:
        comparisons = tree.pocet_porovnani(search_string=word, print_results=False)
        print("   "+word+":", colored(comparisons, "green", attrs=["bold"]))

    print("\n-- vsetky slova z dictionary.txt --")
    search_all(tree, words)
