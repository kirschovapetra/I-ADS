
def print_path(cities, stops_optimal, index):

    if index > 0:
        print_path(cities, stops_optimal, stops_optimal[index])
        print("-> " + str(index) + ".(" + str(cities[index]) + ")", end=" ")


def min_penalty(cities):

    cities.insert(0, 0)             # start = vzdialenost 0

    cities_count = len(cities)      # velkost vstupneho pola
    ideal_distance = 400            # idealna prejdena vzdialenost denne

    stops_optimal = []
    penalties = []

    for i in range(cities_count):

        # init. hodnoty
        stops_optimal.append(0)                              # prva zastavka = nula
        penalties.append((ideal_distance - cities[i]) ** 2)  # (400 - vzdialenost i-teho miesta od 0)^2

        # doteraz navstivene miesta
        for j in range(i):
            # celkova penalta + (400 - vzdialenost od kazdeho predchadzajuceho miesta)^2
            current_penalty = penalties[j] + (ideal_distance - (cities[i] - cities[j])) ** 2

            if current_penalty < penalties[i]:
                penalties[i] = current_penalty  # nove minimum
                stops_optimal[i] = j

    # vypis
    print()
    for i in range(1, cities_count):
        print(str(i) + ".Mesto:", cities[i], "km")
        print("Minimalna penalta:", penalties[i])
        print("Optimalna trasa:", end=" ")
        print_path(cities, stops_optimal, i)
        print("\n\n**********************\n")

    return penalties[cities_count-1]


if __name__ == '__main__':

    with open("cvicenie2data.txt") as f:
        file_content = f.readlines()

    file_content_int = list(map(int, file_content))
    print("MIN. PENALTA = " + str(min_penalty(file_content_int)))
