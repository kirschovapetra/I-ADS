import pandas as pd
import numpy as np
import pprint
global rows, cols, damage


def print_path(pixels):
    mask = np.zeros((rows, cols), dtype=np.bool)
    col = np.argmin(damage[rows-1])

    for row in reversed(range(rows)):
        mask[row, col] = True
        col = pixels[row, col]

    print("Cesta:")
    pp = pprint.PrettyPrinter(width=160, compact=True)
    pp.pprint(list(damage[mask]))


def get_min_damage():
    path = np.zeros((rows, cols), dtype=np.int)

    damage_optimal = np.zeros((rows - 1, cols), dtype=np.int)
    damage_optimal = np.insert(damage_optimal, 0, damage[0], 0)

    for row in range(1, rows):
        for col in range(0, cols):
            if col == 0:
                min_id = col + np.argmin([damage_optimal[row - 1, col],              # stlpec 'col' (0.)
                                          damage_optimal[row - 1, col + 1]])         # stlpec vpravo
            elif col == cols - 1:
                min_id = col + np.argmin([damage_optimal[row - 1, col - 1],          # stlpec vlavo
                                          damage_optimal[row - 1, col]])             # stlpec 'col' (posledny)
            else:
                min_id = (col - 1) + np.argmin([damage_optimal[row - 1, col - 1],    # stlpec vlavo
                                                damage_optimal[row - 1, col],        # stlpec 'col'
                                                damage_optimal[row - 1, col + 1]])   # stlpec vpravo
            # index
            path[row, col] = min_id
            # predchadzajuca damage + nove minimum z predosleho riadku
            damage_optimal[row, col] = damage[row, col] + damage_optimal[row - 1, min_id]

    print_path(path)
    print("\nNajmensie poskodenie: ", min(damage_optimal[rows - 1]))


if __name__ == '__main__':
    with open("cvicenie3data.txt") as f:
        file_content = [x.strip() for x in f.readlines()]

    # split riadkov
    file_content = pd.Series(file_content).str.split(' ')

    # konvert.na int
    for i in file_content.index:
        file_content[i] = list(map(int, file_content[i]))

    damage = np.array(file_content.values.tolist())
    rows, cols = damage.shape
    get_min_damage()
