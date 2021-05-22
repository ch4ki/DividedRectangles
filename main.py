# This is a sample Python script.
import numpy as np
from queue import PriorityQueue
from direct import direct


def ackley(x):
    return -20 * np.exp(-0.2 * np.sqrt(0.5 * ((x[0] ** 2) + (x[1] ** 2)))) - \
           np.exp(0.5 * (np.cos(2 * np.pi * x[0]) + np.cos(2 * np.pi * x[1]))) + np.exp(1) + 20




if __name__ == "__main__":
    lower = np.array([-10, -10])
    upperBound = np.array([10, 10])
    solution = direct(ackley, lower, upperBound, 0.01, 10)
    print(f"Solution: {solution} f(x) = {ackley(solution)}")
    print(ackley(solution))
