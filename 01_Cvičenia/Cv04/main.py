import pandas as pd
import numpy as np


# https://www.guru99.com/knapsack-problem-dynamic-programming.html
def print_items(knapsack, items, max_weight):
    w = max_weight
    n = len(items)
    while n != 0:
        if knapsack[n][w][0] != knapsack[n - 1][w][0]:
            idx = knapsack[n - 1][w][1]
            item_value = items[n - 1][idx].value
            item_weight = items[n - 1][idx].weight
            print("* Item " + str(n) + ": val=" + str(item_value), "weight=" + str(item_weight))
            w = w - item_weight
        n -= 1


# vaha max 2000, z kazdeho riadku max 1 item
def knapsack_no_repeat(items, max_weight):
    num_items = len(items)

    # pocet zaznamov x max hmotnost x (hodnota, index)
    knapsack = np.zeros(shape=(num_items + 1, max_weight + 1, 2), dtype=int)
    knapsack[:, :, 1] = -1

    for i in range(1, num_items + 1):

        # 2 polozky v 1 riadku
        item1 = items[i - 1][0]
        item2 = items[i - 1][1]

        for wj in range(1, max_weight + 1):
            # hodnota z predchadzajuceho kroku
            knapsack[i][wj][0] = knapsack[i - 1][wj][0]
            knapsack[i][wj][1] = knapsack[i - 1][wj][1]

            # K(w, j) = max{K(w − wj, j − 1) + vj , K(w, j − 1)}
            if item1.weight <= wj:
                knapsack[i][wj][1] = 0
                knapsack[i][wj][0] = max(knapsack[i - 1][wj - item1.weight][0] + item1.value,
                                         knapsack[i][wj][0])
            if item2.weight <= wj:
                knapsack[i][wj][1] = 1
                knapsack[i][wj][0] = max(knapsack[i - 1][wj - item2.weight][0] + item2.value,
                                         knapsack[i][wj][0])

    print_items(knapsack, items, max_weight)
    print("\n  MAX hodnota:", knapsack[num_items][max_weight][0])


class Item:
    def __init__(self, v, w):
        self.value = v
        self.weight = w


if __name__ == '__main__':
    with open("cvicenie4data.txt") as f:
        file_content = [x.strip() for x in f.readlines()]

    # split riadkov
    file_content = pd.Series(file_content).str.split(',')

    items_arr = []
    for r in file_content:
        items_arr.append([Item(int(r[0]), int(r[1])),
                          Item(int(r[2]), int(r[3]))])

    knapsack_no_repeat(items_arr, 2000)
