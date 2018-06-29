from genetic import *
from simulated import *
from random import randint, shuffle
from copy import deepcopy

file_names = "dataset\\usca312_name.txt"
file_distances = "dataset\\usca312_dist.txt"
file_coordinates = "dataset\\usca312_xy.txt"

genetic_algorithm(200,"tournament","one-point",0.001,1000,(1/200000),file_names,file_distances,file_coordinates)
#simulated_annealing(1000,0.0001,file_names,file_distances,file_coordinates)
