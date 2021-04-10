"""
Zadanie 2: najst naplnenie ruksaku, aby:
    * nepresahoval vahu W
    * neobsahoval viac ako T krehkych predmetov
    * mal maximalnu moznu hodnotu.

Vstup:
3           pocet predmetov
6           max vaha
2           max pocet krehkych predmetov
1 8 4 0     id hodnota hmotnost krehkost (nie)
2 5 8 1     id hodnota hmotnost krehkost (ano)
3 6 1 0     id hodnota hmotnost krehkost (nie)

Vystup:
14          optimalna hodnota ruksaku
2           pocet predmetov
1           vlozime predmet 1
3           vlozime predmet 3

Zdroje:
 https://stackoverflow.com/questions/55437217/pseudo-code-algorithm-for-knapsack-problem-with-two-constrains
 https://www.guru99.com/knapsack-problem-dynamic-programming.html
"""

import pandas as pd
import numpy as np
from termcolor import colored


class Item:
    def __init__(self, value, weight, fragile):
        self.value = value
        self.weight = weight
        self.fragile = fragile


def print_item(item_num, items_len, item):
    """
    Vypis polozky v ruksaku
    :param item_num: poradove cislo polozky
    :param items_len: pocet vsetkych poloziek
    :param item: polozka
    :return:
    """
    item_id = colored(" " * (len(str(items_len)) - len(str(item_num))) + str(item_num),
                      "cyan", attrs=['bold'])
    val = colored(str(item.value), "red", attrs=['bold'])
    weight = colored(str(item.weight), "red", attrs=['bold'])
    fragile = colored(str(item.fragile), "red", attrs=['bold'])

    print("* Item " + item_id + ": val=" + val, "weight=" + weight, "fragile=" + fragile)


def load(filename):
    """
    Nacitanie vstupneho suboru
    :param filename: nazov
    :return: pole predmetov, maximalna vaha, maximalny pocet krehkych predmetov
    """
    with open(filename) as f:
        file_content = [x.strip() for x in f.readlines()]

    W = int(file_content[1])
    T = int(file_content[2])

    file_content = pd.Series(file_content[3:]).str.split(' ')

    for i in file_content.index:
        file_content[i] = list(map(int, file_content[i]))

    arr = []
    for row in file_content:
        arr.append(Item(int(row[1]), int(row[2]), int(row[3])))

    arr = pd.Series(arr, index=range(1, len(arr) + 1))  # indexy poloziek [1..n]

    return arr, W, T


def save_output(filename, cost, arr):
    """
    Zapis vystupu do suboru
    :param filename: nazov
    :param cost: maximalna hodnota ruksaku
    :param arr: pole predmetov
    """

    to_write = str(cost) + "\n" + str(len(arr))
    for item in reversed(arr):
        to_write += "\n" + str(item)

    with open(filename, "w") as f:
        f.write(to_write)

    print("\n  Obsah ruksaku ulozeny do " + colored(filename, color="cyan", attrs=["bold"]))


def get_items(KNAPSACK, items, max_weight, max_fragile):
    """
    Backtracking predmetov v ruksaku
    :param max_fragile: maximalny pocet krehkych predmetov
    :param KNAPSACK: matica pre optimalnu hodnotu
    :param items: predmety
    :param max_weight: maximalna vaha
    :return: pole predmetov v ruksaku
    """

    w = max_weight
    f = max_fragile
    n = len(items)

    items_in_knapsack = []

    while n > 0:
        # cena nie je rovnaka => bola pridana nova polozka
        if KNAPSACK[n][w][f] != KNAPSACK[n - 1][w][f]:
            item_current = items[n]  # aktualna polozka
            items_in_knapsack.append(n)  # ulozi sa poradove cislo

            print_item(n, len(items), item_current)

            # posun na dalsiu polozku
            w -= item_current.weight
            f -= item_current.fragile

        n -= 1

    return items_in_knapsack


def optimal_knapsack(items, max_weight, max_fragile):
    """
    Optimalne naplnenie ruksaku
    :param items: pole predmetov
    :param max_weight: maximalna hmotnost
    :param max_fragile: maximalny pocet krehkych predmetov
    :return: maximalna hodnota ruksaku, premety v ruksaku
    """

    n = len(items)

    KNAPSACK = np.zeros(shape=(n + 1, max_weight + 1, max_fragile + 1), dtype=int)

    for i in range(1, n + 1):  # i = 1...n  <-- indexy poloziek

        item = items[i]

        for w in range(1, max_weight + 1):  # w = 1...max_weight   <-- (max) vaha ruksaku
            for f in range(1, max_fragile + 1):  # f = 1...max_fragile  <-- (max) pocet krehkych predmetov

                # hodnota z predchadzajuceho kroku (predpokladam, ze sa nic nove neprida)
                KNAPSACK[i, w, f] = KNAPSACK[i - 1, w, f]

                # vaha polozky neprekroci aktualnu hranicu vahy
                if item.weight <= w:

                    # povodna hodnota ruksaku vs. hodnota ked sa prida nova polozka
                    KNAPSACK[i, w, f] = max(KNAPSACK[i, w, f],
                                            KNAPSACK[i - 1, w - item.weight, f - item.fragile] + item.value)

    return KNAPSACK


def main(filename_read, filename_write):
    print("\nSubor:", colored(filename_read, color="cyan", attrs=["bold"]), "\n")

    items_all, max_w, max_f = load(filename_read)

    knapsack = optimal_knapsack(items_all, max_w, max_f)
    max_cost = knapsack[len(items_all), max_w, max_f]

    knapsack_items = get_items(knapsack, items_all, max_w, max_f)
    print("\n  MAX hodnota:", colored(str(max_cost), "red", attrs=['bold']))

    save_output(filename_write, max_cost, knapsack_items)

    print("\n---------------------------------------")


if __name__ == '__main__':
    main("predmety.txt", "outPredmety.txt")
