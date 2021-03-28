# https://github.com/mission-peace/interview/blob/master/src/com/interview/dynamic/NPotGold.java
import numpy as np

# def calculate(T, i, j):
#     return T[i][j] if i <= j else 0
#

# def max_win(tokens):
#     n = len(tokens)
#
#     # priebezne maximalne vyhry
#     PLAYER_TAB = np.diag(tokens)
#
#     for interval_size in range(1, n):  # prechadzaju sa rozne velke intervaly
#
#         for end in range(interval_size, n):  # koniec intervalu
#             start = end - interval_size      # zaciatok intervalu
#
#             if start + 1 > end:
#                 pick_from_start = 0  # tokens[start]
#             elif tokens[start + 1] > tokens[end]:  # start start
#                 pick_from_start = tokens[start] + calculate(PLAYER_TAB, start + 2, end)
#             else:  # start end
#                 pick_from_start = tokens[start] + calculate(PLAYER_TAB, start + 1, end - 1)
#
#             if start > end - 1:
#                 pick_from_end = 0  # tokens[end]
#             elif tokens[end - 1] > tokens[start]:  # end end
#                 pick_from_end = tokens[end] + calculate(PLAYER_TAB, start, end - 2)
#             else:  # end start
#                 pick_from_end = tokens[end] + calculate(PLAYER_TAB, start + 1, end - 1)
#
#             PLAYER_TAB[start, end] = max(pick_from_start, pick_from_end)
#
#     return PLAYER_TAB[0, n-1]


def max_win(tokens):
    n = len(tokens)

    # priebezne maximalne vyhry
    PLAYER_TAB = np.zeros((n, n), dtype=int)
    KRUPIER_TAB = np.zeros((n, n), dtype=int)

    for x in range(n):
        for end in range(x, n):     # koniec intervalu
            start = end - x         # zaciatok intervalu

            # parny interval => vybera hrac
            if (x+1) % 2 == 0:
                pick_from_start = tokens[start] + KRUPIER_TAB[start + 1, end]
                pick_from_end = tokens[end] + KRUPIER_TAB[start, end - 1]

            # neparny interval => vybera krupier
            else:
                pick_from_start = tokens[start]
                pick_from_end = tokens[end]

            # maximalna vyhra
            if pick_from_start > pick_from_end:
                PLAYER_TAB[start, end] = tokens[start] + KRUPIER_TAB[start + 1, end]  # hrac zoberie zo zaciatku
                KRUPIER_TAB[start, end] = PLAYER_TAB[start + 1, end]  # krupierovi ostane <start+1, end>
            else:
                PLAYER_TAB[start, end] = tokens[end] + KRUPIER_TAB[start, end - 1]  # hrac zoberie z konca
                KRUPIER_TAB[start, end] = PLAYER_TAB[start, end - 1]  # krupierovi ostane <start, end-1>

    return PLAYER_TAB[0, n - 1]


if __name__ == '__main__':
    with open("cvicenie6data.txt") as f:
        file_content = list(map(int, f.read()))

    print(max_win(file_content))
