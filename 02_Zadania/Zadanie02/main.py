import pandas as pd
import numpy as np
'''
- kazdy predmet mozeme do ruksaku bud vlozit, alebo nevlozit. 
- Jeden predmet mozeme do ruksaku vlozit najviac 1-krat 
- Nemozeme brat casti predmetu
  
- najst naplnenie ruksaku, nepresahoval vahu W, neobsahoval viac ako T krehkych predmetov a aby mal 
  maximalnu moznu hodnotu. 

Vstup:
3           pocet predmetov
6           max vaha
2           max pocet krehkych predmetov
1 8 4 0     id hodnota hmotnost krehkost (nie)
2 5 8 1     id hodnota hmotnost krehkost (ano)
3 6 1 0     id hodnota hmotnost krehkost (nie)

vystup:
14          optimalna hodnota ruksaku
2           pocet predmetov 
1           vlozime predmet 1
3           vlozime predmet 3

'''


class Item:
    def __init__(self, value, weight, fragile):
        self.value = value
        self.weight = weight
        self.fragile = fragile


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

    return arr, W, T


def save_output(filename, cost, arr):
    """
    Zapis vystupu do suboru
    :param filename: nazov
    :param cost: maximalna hodnota ruksaku
    :param arr: pole predmetov
    """
    to_write = str(cost) + "\n" + str(len(arr))
    for item in arr:
        to_write += "\n" + str(item)

    with open(filename, "w") as f:
        f.write(to_write)


def get_items(knapsack, items, max_weight, max_fragile):
    """
    Backtracking predmetov v ruksaku
    Zdroj: https://www.guru99.com/knapsack-problem-dynamic-programming.html
    :param knapsack: matica pre optimal cost
    :param items: predmety
    :param max_weight: maximalna vaha
    :return: pole predmetov v ruksaku
    """

    w = max_weight
    f = max_fragile
    n = len(items)

    items_in_knapsack = []
    temp = []

    while n != 0:
        if knapsack[n][w][f] != knapsack[n - 1][w][f]:

            item_value = items[n - 1].value
            item_weight = items[n - 1].weight
            item_fragile = items[n - 1].fragile

            print("* Item " + str(n) + ": val=" + str(item_value),
                  "weight=" + str(item_weight),
                  "fragile=" + str(item_fragile))

            items_in_knapsack.append(n)
            temp.append(items[n - 1])

            w -= item_weight
            f -= item_fragile

        n -= 1

    return items_in_knapsack


def init(arr):
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            for k in range(len(arr[i, j])):
                arr[i, j, k] = dict()


def optimal_knapsack(items, max_weight, max_fragile):
    """
    Optimalne naplnenie ruksaku
    :param items: pole predmetov
    :param max_weight: maximalna hmotnost
    :param max_fragile: maximalny pocet krehkych predmetov
    :return: maximalna hodnota ruksaku, premety v ruksaku
    """

    n = len(items)

    # pocet zaznamov x max hmotnost x max fragile (hodnota)
    KNAPSACK = np.zeros(shape=(n + 1, max_weight + 1, max_fragile + 1), dtype=int)

    for i in range(1, n + 1):

        item = items[i - 1]

        for wj in range(1, max_weight + 1):
            for f in range(1, max_fragile + 1):

                # hodnota z predchadzajuceho kroku (init = nic sa neprida)
                KNAPSACK[i, wj, f] = KNAPSACK[i - 1, wj, f]

                # K(w, j) = max{K(w − wj, j − 1) + vj , K(w, j − 1)}
                if item.weight <= wj and item.fragile <= f:
                    KNAPSACK[i, wj, f] = max(KNAPSACK[i - 1, wj - item.weight, f - item.fragile] + item.value,
                                             KNAPSACK[i, wj, f])

    return KNAPSACK[n, max_weight, max_fragile], get_items(KNAPSACK, items, max_weight, max_fragile)


if __name__ == '__main__':

    items, max_weight, max_fragile = load("predmety3.txt")
    n = len(items)

    max_cost, knapsack = optimal_knapsack(items, max_weight, max_fragile)

    print("\n  MAX hodnota:", max_cost)

    save_output("out.txt", max_cost, knapsack)