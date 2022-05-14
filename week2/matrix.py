"""
step2022 -week2-
1. Write code to calculate C = A * B, where A, B and C are matrices of size N * N
Measure the execution time of your code for various Ns, and plot a graph between N and the execution time
"""

import numpy, sys, time
import matplotlib.pyplot as plt

def mult_matrix(n) -> time:

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
            c[i, j] = sum([a[i, ii]*b[ii, j] for ii in range(n)])

    end = time.time()

    print("Finished calculating a %d×%d Matrix" %(n, n))
    return end - begin

#the largest N
max = 100

Ns = [i for i in range(0, max+1, 20)]
res = [mult_matrix(n) for n in Ns]

x = numpy.linspace(0, max, 10000)
#Find the appropriate coefficients
a = res[-1] / max**3

plt.plot(Ns, res)
plt.plot(x, a*(x**3), label="$(%.0e)*x^3$" % a)
plt.xlabel("Matrix size (N×N)")
plt.ylabel("Time")
plt.legend() 
plt.title("Graph of Execution time of Matrix Multiplication")

plt.show()