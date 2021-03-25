import numpy as np


def max_win(tokens):
    n = len(tokens)

    PLAYER_TAB = np.zeros((n, n), dtype=int)
    KRUPIER_TAB = np.zeros((n, n), dtype=int)

    for interval_size in range(n):  # prechadzaju sa rozne velke intervaly

        for end in range(interval_size, n):  # koniec intervalu
            start = end - interval_size      # zaciatok intervalu

            # parny pocet tahov => porovnavam iba koncove hodnoty
            if interval_size % 2 == 0:
                pick_from_start = tokens[start]  # zo zaciatku
                pick_from_end = tokens[end]  # z konca

            # neparny pocet tahov => pozeram sa na to, aku vyhru moze dostat krupier
            else:
                pick_from_start = tokens[start] + KRUPIER_TAB[start + 1, end]  # zo zaciatku
                pick_from_end = tokens[end] + KRUPIER_TAB[start, end - 1]  # z konca

            # maximalna vyhra
            if pick_from_start > pick_from_end:
                PLAYER_TAB[start, end] = tokens[start] + KRUPIER_TAB[start + 1, end]  # hrac zoberie zo zaciatku
                KRUPIER_TAB[start, end] = PLAYER_TAB[start + 1, end]  # krupierovi ostane <start+1, end>
            else:
                PLAYER_TAB[start, end] = tokens[end] + KRUPIER_TAB[start, end - 1]  # hrac zoberie z konca
                KRUPIER_TAB[start, end] = PLAYER_TAB[start, end - 1]  # krupierovi ostane <start, end-1>

    return PLAYER_TAB[0, n-1]


if __name__ == '__main__':
    with open("cvicenie6data.txt") as f:
        file_content = list(map(int, f.read()))

    print(max_win([2, 6, 9, 1, 2, 9, 2, 8]))
    print(max_win([2, 6, 9, 1, 2, 16, 2, 8]))
    print(max_win(file_content))
