#!/usr/bin/env python3

from common import format_tour, read_input

import solver_2opt, solver_ga

CHALLENGES = 7


def generate_sample_output():
    for i in range(CHALLENGES):
        cities = read_input(f"input_{i}.csv")
        
        solver = solver_2opt
        name = "2opt"
        tour = solver.solve(cities)
        with open(f"myresult/{name}_{i}.csv", "w") as f:
            f.write(format_tour(tour) + "\n")

        solver = solver_ga
        for mode, name in enumerate(["random", "greedy", "greedy+2opt"]):
            tour = solver.solve(cities, mode)
            with open(f"myresult/ga({name})_{i}.csv", "w") as f:
                f.write(format_tour(tour) + "\n")
        
        print(f"Finished input_{i}.csv")

if __name__ == "__main__":
    generate_sample_output()
