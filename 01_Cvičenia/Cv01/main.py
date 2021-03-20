import random
import pprint
import pandas as pd


def find_nearest(array, value):
    return min(array, key=lambda elem: abs(elem - value))


def sort_by_abs(matrix):
    min_abs = []
    sorted_rows = []

    for row in matrix:
        min_abs.append(abs(min(row, key=abs)))  # minimalna absolutna hodnota
        sorted_rows.append(sorted(row))  # zotriedeny riadok matice

    df = pd.DataFrame({
        "max_abs": min_abs,
        "sorted_rows": sorted_rows})

    df = df.sort_values(by=["max_abs"], ascending=False)

    df = df.reset_index()
    df.drop(columns=["index"], inplace=True)
    return df


def find_closest_to_zero(arr):
    min_distance = 1000000
    min_id = -1

    for idx in range(len(arr)):
        if abs(arr[idx]) < min_distance:
            min_distance = abs(arr[idx])
            min_id = idx

    return arr[min_id]


def find_sum2(matrix):
    content_df = sort_by_abs(matrix)

    sum_all = 0
    for item in content_df["sorted_rows"]:

        # suma = 0 => vyberiem cislo najblizsie k 0
        selected = find_closest_to_zero(item)

        # suma je kladna => hladam zaporne cislo
        if sum_all > 0:
            negative_arr = [a for a in item if a < 0]
            if len(negative_arr) == 0:
                negative_arr = item

            # najblizsie opacne cislo
            selected = find_nearest(negative_arr, (-1) * sum_all)

        # suma je zaporna => hladam kladne cislo
        elif sum_all < 0:
            positive_arr = [a for a in item if a >= 0]
            if len(positive_arr) == 0:
                positive_arr = item

            # najblizsie opacne cislo
            selected = find_nearest(positive_arr, (-1) * sum_all)

        sum_all += selected
        print("row:", item)
        print("selected: ", selected)
        print("sum: ", sum_all, "\n___________________________________________")

    print("\nFINAL SUM: ", sum_all)


def find_sum(matrix):
    count = 0

    while True:

        # vypis
        if count % 2000 == 0:
            print(".", end="")
        elif count % 200000 == 0:
            print("\n")
        count += 1

        # vyber nahodnych cisel
        selected_numbers = []
        for row in matrix:
            random_id = random.randint(0, len(row) - 1)
            selected_numbers.append(row[random_id])

        # suma nahodnych cisel
        if abs(sum(selected_numbers)) <= 0:
            break

    print("\n\nSUM: ", sum(selected_numbers), end="\n\n")
    pp = pprint.PrettyPrinter(width=100, compact=True)
    pp.pprint(selected_numbers)


if __name__ == '__main__':

    # nacitanie suboru
    # with open("cvicenie1data2.txt") as f:
    with open("cvicenie1data.txt") as f:
        file_content = [x.strip() for x in f.readlines()]

    # split riadkov
    file_content = pd.Series(file_content[2:]).str.split(' ')

    # konvert.na int
    for i in file_content.index:
        file_content[i] = list(map(int, file_content[i]))

    find_sum(file_content)
    # find_sum2(file_content)


