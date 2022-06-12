import sys
import math
import numpy as np
import random

from common import print_tour, read_input
from genetic_algorithm import GeneticAlgorithm, Chromosome, Log


def distance(city1, city2):
    """
    2都市間の距離を求める
    """
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def make_dist(cities):
    """
    各都市間の座標の距離を計算したリストを作成する。
    """
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    return dist

def greedy(cities, current_city, dist):
    """
    貪欲法

    Parameters
    ----------
    cities : list
        都市の座標のリスト。
    current_city : int
        貪欲法を始める点。
    dist : list
        各都市間の距離のリスト。
    """
    N = len(cities)

    unvisited_cities = set(range(N))
    unvisited_cities.remove(current_city)
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities, key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city

    return tour


def two_opt(tour, dist):
    """
    2opt

    Parameters
    ----------
    cities : list
        都市の座標のリスト。
    dist : list
        各都市間の距離のリスト。
    """
    N = len(tour)

    while True:
        is_change = False
        for i in range (N-2):
            for j in range(i+2, N):
                l1 = dist[tour[i]][tour[i+1]]
                l2 = dist[tour[j]][tour[(j+1) % N]]
                l3 = dist[tour[i]][tour[j]]
                l4 = dist[tour[i+1]][tour[(j+1) % N]]
                if l1+l2 > l3+l4:
                    new_solution = tour[i+1:j+1]
                    tour[i+1:j+1] = new_solution[::-1]
                    is_change = True
        if not is_change:
            break

    return tour


def solve(cities, mode=0):
    """
    Genetic AlgorithmでTSPを解く。
    """

    dist = make_dist(cities)
    population_size = 10
    initial_population = []
    N = len(cities)

    #初期個体群生成

    #1. ランダムな経路
    if mode == 0:
        path = list(range(len(cities)))
        for _ in range(population_size):
            random.shuffle(path)
            initial_population.append(Chromosome(path.copy()))

    #2. ランダムな点から貪欲法を始める
    elif mode == 1:
        for i in range(population_size):
            init_city = random.randrange(len(cities))
            path = greedy(cities, init_city, dist)
            initial_population.append(Chromosome(path))

    #3. 貪欲法->2opt
    #前に作った経路で、最も長かった辺を構成する点からまた貪欲法->2opt の繰り返し
    elif mode == 2:
        init_city = random.randrange(len(cities))
        for i in range(population_size):
            max_dist = -1
            path = greedy(cities, init_city, dist)
            path = two_opt(path, dist)
            initial_population.append(Chromosome(path))
            for j in range(len(cities)):
                tmp = dist[path[j]][path[(j+1)%N]]
                if tmp > max_dist:
                    max_dist = tmp
                    init_city = j

    else:
        print("mode Error.")
        exit(1)
    

    log = Log(
        cities = cities, 
        steps = 5,
        printer = 1,
        mode = mode)

    ga = GeneticAlgorithm(
        initial_population = initial_population,
        max_generations = 10000,
        crossover_probability = 0.9,
        mutation_probability = 0.2,
        elite_selection_rate = 0.3,
        dist = dist,
        log = log)
    best_path = ga.run_algorithm()

    return best_path

if __name__ == "__main__":
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]), 0)
    print_tour(tour)