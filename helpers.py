import matplotlib.pyplot as plt
from matplotlib.path import Path
import numpy as np
import matplotlib.patches as patches

data_cities = []
data_distances = {}
data_coordinates = {}


def read_cities(file_names, file_distances, file_coordinates):
    input_names = open(file_names, 'r')

    for line in input_names:
        if '#' not in line:
            name = line.strip()
            name = name.replace(" ", "")
            data_cities.append(name)

    input_distances = open(file_distances, 'r')

    index = 0
    count = 0
    data_distances[data_cities[index]] = {}
    for line in input_distances:
        if '#' not in line:
            arr = [int(x) for x in line.split()]

            for x in arr:
                if (count == 312):
                    index += 1
                    data_distances[data_cities[index]] = {}
                    count = 0

                data_distances[data_cities[index]][data_cities[count]] = x
                count += 1

    input_coordinates = open(file_coordinates, 'r')

    index = 0

    for line in input_coordinates:
        if '#' not in line:
            arr = [float(x) for x in line.split()]
            data_coordinates[data_cities[index]] = {}

            data_coordinates[data_cities[index]]['x'] = arr[0]
            data_coordinates[data_cities[index]]['y'] = arr[1]
            index += 1


class Route:
    def __init__(self, cities):
        self.cities = cities
        self.distance = 0

    def set_total_distance(self):
        for x in range(len(self.cities)):
            if x < (len(self.cities) - 1):
                curr_city = self.cities[x]
                next_city = self.cities[x + 1]
                self.distance += data_distances[curr_city][next_city]
            else:
                curr_city = self.cities[x]
                next_city = self.cities[0]
                self.distance += data_distances[curr_city][next_city]

    def get_fitness(self):
        return 1 / self.distance


def plot_path(route):
    size = len(route.cities)
    vertices = np.zeros(shape=(size, 2))
    codes =  np.zeros(shape=(size))

    for i in range(size):
        if i==0:
            codes[i] = Path.MOVETO
        else:
            codes[i] = Path.LINETO

        vertices[i, 0] = data_coordinates[route.cities[i]]['x']
        vertices[i, 1] = data_coordinates[route.cities[i]]['y']

    path = Path(vertices, codes)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(-12000, -3000)
    patch = patches.PathPatch(path, facecolor='white', lw=2)
    ax.add_patch(patch)
    ax.set_ylim(1000, 6000)
    plt.show()
