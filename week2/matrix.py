"""
step2022 -week2-
1. Write code to calculate C = A * B, where A, B and C are matrices of size N * N
Measure the execution time of your code for various Ns, and plot a graph between N and the execution time
"""

import numpy, sys, time
import matplotlib.pyplot as plt

def mult_matrix(n):
    """ Measures time of multiplying n x n matrices.

    Args:
    n: Matrix size. Matrices used in this function are square.

    Returns:
    Calculation time of multiplying square matrices in time object. No initialization time is included.
    """

    a = numpy.zeros((n, n)) # Matrix A
    b = numpy.zeros((n, n)) # Matrix B
    c = numpy.zeros((n, n)) # Matrix C

    # Initialize the matrices to some values.
    for i in range(n):
        for j in range(n):
            a[i, j] = i * n + j
            b[i, j] = j * n + i
            c[i, j] = 0

    begin = time.time()

    # Calculate Matrix C(=AB)
    for i in range(n):
        for j in range(n):
            c[i, j] = sum([a[i, k]*b[k, j] for k in range(n)])

    end = time.time()

    print("Finished calculating a %dx%d Matrix" %(n, n))
    return end - begin

def main(max_n, step):
    #max_n : the largest N
    max_n, step = int(max_n), int(step)
    Ns = numpy.linspace(0, max_n, step, dtype=int)
    calculation_time = [mult_matrix(n) for n in Ns]

    #coe : Coefficient of approximation formula
    coe = numpy.polyfit(Ns, calculation_time, 3)

    x = numpy.linspace(0, max_n, 10000)

    plt.plot(Ns, calculation_time)
    plt.plot(x, coe[0]*x**3 + coe[1]*x**2 + coe[2]*x + coe[3], label="Approximate formula", alpha=0.7)
    plt.xlabel("Matrix size (NxN)")
    plt.ylabel("Time")
    plt.legend() 
    plt.title("Graph of Execution time of Matrix Multiplication")

    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s [Max matrix size] [step]" % sys.argv[0])
        exit(1)
    main(sys.argv[1], sys.argv[2])