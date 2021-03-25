import numpy as np
from tqdm import tqdm


def max_win(tokens):
    n = len(tokens)

    # priebezne maximalne vyhry [start, end]
    MAX_WIN = np.zeros((n, n), dtype=int)

    for interval_size in range(n):           # prechadzaju sa rozne velke intervaly
        for end in range(interval_size, n):  # koniec intervalu
            start = end - interval_size      # zaciatok intervalu

            # obaja beru zo zaciatku => zoberu 'start' a 'start+1' prvok
            start_start = MAX_WIN[start + 2][end] if (start + 2 <= end) else 0
            # kazdy z ineho konca => zoberu 'start' a 'end' prvok
            start_end = MAX_WIN[start + 1][end - 1] if (start + 1 <= end - 1) else 0
            # obaja beru z konca => zoberu 'end' a 'end-1' prvok
            end_end = MAX_WIN[start][end - 2] if (start <= end - 2) else 0

            # maximalna vyhra zo zaciatku vs. z konca
            MAX_WIN[start][end] = max(tokens[start] + min(start_start, start_end),
                                      tokens[end] + min(start_end, end_end))

    return MAX_WIN[0][n - 1]


if __name__ == '__main__':
    with open("cvicenie6data.txt") as f:
        file_content = list(map(int, f.read()))

    # print(solve(file_content))
    print(max_win(file_content))
