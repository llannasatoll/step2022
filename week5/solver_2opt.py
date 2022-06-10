#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def greedy(cities):
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    return tour, dist


def solve(cities):
    """
    Args:
        solution:
    
    Returns:
    """
    solution, dist = greedy(cities)
    N = len(solution)

    while True:
        isChange = False
        for i in range (N-2):
            for j in range(i+2, N):
                l1 = dist[solution[i]][solution[i+1]]
                l2 = dist[solution[j]][solution[(j+1) % N]]
                l3 = dist[solution[i]][solution[j]]
                l4 = dist[solution[i+1]][solution[(j+1) % N]]
                if l1+l2 > l3+l4:
                    new_solution = solution[i+1:j+1]
                    solution[i+1:j+1] = new_solution[::-1]
                    isChange = True
        if not isChange:
            break
    return solution


if __name__ == "__main__":
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)