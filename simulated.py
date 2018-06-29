from helpers import *
from math import exp
from copy import deepcopy
from random import uniform, randint,shuffle


def acceptance_probabilty(energy, new_energy, temperature):
    if new_energy < energy:
        return 1
    else:
        return exp((energy - new_energy) / temperature)


def generate_successor(route):
    new_route = Route(deepcopy(route.cities))

    pos1 = randint(0, len(new_route.cities) - 1)
    pos2 = randint(0, len(new_route.cities) - 1)

    temp = new_route.cities[pos1]
    new_route.cities[pos1] = new_route.cities[pos2]
    new_route.cities[pos2] = temp

    new_route.set_total_distance()
    return new_route


def simulated_annealing(temperature, cooling_rate, file_names, file_distances,file_coordinates):
    read_cities(file_names, file_distances,file_coordinates)

    route = Route(deepcopy(data_cities))
    route.set_total_distance()
    best = Route(deepcopy(route.cities))
    best.set_total_distance()

    while (temperature > 1):
        new_route = generate_successor(route)
        current_energy = route.distance
        next_energy = new_route.distance

        if acceptance_probabilty(current_energy, next_energy, temperature) > uniform(0, 1):
            route = Route(deepcopy(new_route.cities))
            route.set_total_distance()

        if route.get_fitness() > best.get_fitness():
            best = Route(deepcopy(route.cities))
            best.set_total_distance()

        temperature *= 1 - cooling_rate
        print(best.distance)

    plot_path(best)
    print(best.cities)
    return best