# https://github.com/phvargas/TSP-python/blob/master/TSP.py
from itertools import combinations
import pandas as pd
import numpy as np
from tqdm import tqdm


def load_matrix():

    # nacitanie suboru
    with open("cvicenie5data.txt", "r") as f:
        file_content = [x.strip() for x in f.readlines()]

    # split riadkov
    file_content = pd.Series(file_content[1:]).str.split(' ')

    n = len(file_content)

    # # konvert.na int
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            matrix[i][j] = int(file_content[i][j])

    return matrix, n


def min_distance(i, subset, distances, OPTIMAL_DIST):

    if (i, subset) not in OPTIMAL_DIST:  # kombinacia (i,subset) nebola navstivena

        # aka je najmensia vzdialenost, ked pridam i
        values_to_compare = []

        # prechadzaju sa mesta v podmnozine
        for j in subset:
            # pre kazde mesto sa vytvori podmnozina subset - {j}
            subset_without_j = list(subset).copy()
            subset_without_j.remove(j)

            # hlada sa optimalna cesta pre mensie podmnoziny miest
            result = min_distance(j, tuple(subset_without_j), distances, OPTIMAL_DIST)

            values_to_compare.append(result + distances[i][j])

        # minimalna vzdialenost
        OPTIMAL_DIST[i, subset] = min(values_to_compare)

    return OPTIMAL_DIST[i, subset]


if __name__ == '__main__':

    # nacitanie matice
    distances, n = load_matrix()

    # 9-prvkove kombinacie miest
    cities_combinations = list(combinations(range(1, n), 9))

    OPTIMAL_DIST = {}  # dictionary[i, subset]
    for i in range(n):
        # priame vzdialenosti od i-teho mesta po zaciatok
        OPTIMAL_DIST[i, ()] = distances[i][0]

    result_distances = []
    for i in tqdm(range(len(cities_combinations))):

        result_distances.append(min_distance(0, cities_combinations[i], distances, OPTIMAL_DIST))

    print("Minimalna dlzka trasy: ", min(result_distances))
