from helpers import *
from random import uniform, shuffle, randint
from copy import deepcopy


def sort_population_stochastic(population):
    for passnum in range(len(population) - 1, 0, -1):
        for i in range(passnum):
            if population[i].get_fitness() < population[i + 1].get_fitness():
                temp = population[i]
                population[i] = population[i + 1]
                population[i + 1] = temp


def stochastic_selection(population):
    sum_fitness = 0
    for x in range(len(population)):
        sum_fitness += population[x].get_fitness()

    random = uniform(0, sum_fitness)

    sum = 0
    for x in range(len(population)):
        sum += population[x].get_fitness()
        if (sum >= random):
            return population[x]

    return population[0]


def tournament_selection(n, population):
    x = 0
    arr = []

    while x < n:
        random = randint(0, len(population) - 1)
        if random not in arr:
            arr.append(random)
            x += 1

    best = arr[0]
    for i in range(len(arr)):
        if (population[arr[i]].get_fitness() > population[best].get_fitness()):
            best = arr[i]

    return population[best]


def selection(criteria, population):
    if "stochastic" in criteria:
        return stochastic_selection(population)
    elif "tournament" in criteria:
        size = int(round(0.1 * len(population)))
        return tournament_selection(size, population)
    else:
        print("Invalid Selection Criteria")


def one_point_crossover(K, parent_one, parent_two):
    child = Route([])
    min = 0.1 * K
    point = randint(min, K - min - 1)
    size = len(parent_one.cities)

    for i in range(point):
        child.cities.append(parent_one.cities[i])

    for i in range(size):
        if parent_two.cities[i] not in child.cities:
            child.cities.append(parent_two.cities[i])

    child.set_total_distance()

    return child


def two_point_crossover(K, parent_one, parent_two):
    child = Route([])
    min = 0.05 * K
    point = randint(min, (K / 2) - min - 1)
    size = len(parent_one.cities)
    arr = []

    for i in range(point):
        child.cities.append(parent_one.cities[i])
        arr.append(parent_one.cities[K - 1 - point + i])

    for i in range(size):
        if parent_two.cities[i] not in child.cities and parent_two.cities[i] not in arr:
            child.cities.append(parent_two.cities[i])

    for i in range(point):
        child.cities.append(arr[i])

    child.set_total_distance()

    return child


def crossover(K, method, parent_one, parent_two):
    if "one-point" in method:
        return one_point_crossover(K, parent_one, parent_two)
    elif "two-point" in method:
        return two_point_crossover(K, parent_one, parent_two)


def get_fittest(K, population):
    best = 0
    for i in range(K):
        if (population[i].get_fitness() > population[best].get_fitness()):
            best = i

    return population[best]


def mutate(route, mutation_rate):
    size = len(route.cities)
    for i in range(size):
        prob = uniform(0, 1)
        if (prob < mutation_rate):
            rand = randint(0, size - 1)
            temp = route.cities[i]
            route.cities[i] = route.cities[rand]
            route.cities[rand] = temp


def genetic_algorithm(K, selection_criteria, cross_method, mutation_rate, max_iters, min_fitness, file_names,
                      file_distances, file_coordinates):
    population = []

    read_cities(file_names, file_distances, file_coordinates)

    for x in range(K):
        route = Route(deepcopy(data_cities))
        shuffle(route.cities)
        route.set_total_distance()
        population.append(route)

    x = 0

    for x in range(max_iters):
        if (selection_criteria == "stochastic"):
            sort_population_stochastic(population)

        new_population = []
        for i in range(K):
            parent_one = selection(selection_criteria, population)
            parent_two = selection(selection_criteria, population)

            child = crossover(K, cross_method, parent_one, parent_two)
            mutate(child, mutation_rate)
            new_population.append(child)

        population = new_population
        fittest = get_fittest(K, population)
        print(fittest.distance)

        if fittest.get_fitness() >= min_fitness:
            break

    print(fittest.cities)
    plot_path(fittest)
    return fittest
