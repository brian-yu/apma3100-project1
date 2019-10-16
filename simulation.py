import random
import math
import numpy as np
import sys

sys.setrecursionlimit(1500)

def random_number_generator(i):

    multiplier = 24693
    increment = 3967
    modulus = 2**15
    seed = 1000

    def helper(j):
        if j <= 0:
            return seed
        return (multiplier * helper(j-1) + increment) % modulus

    return helper(i) / modulus

def random_variable_generator(random_num):
    def inverse_cdf(p):
        return -12 * math.log(1-p)

    return inverse_cdf(random_num)

def sample_cdf(sample, x):
    return np.where(sample <= x)[0].size / sample.size

def print_cdf(sample, x, complementary=False):
    if not complementary:
        print(f"P[W <= {x}] = {sample_cdf(sample, x)}")
    else:
        print(f"P[W > {x}] = {1 - sample_cdf(sample, x)}")

def simulate(X):

    time = 0
    numCalls = 0

    DIAL_TIME = 6
    BUSY_TIME = 3
    RING_TIME = 25
    END_TIME = 1

    while numCalls < 4:
        numCalls += 1
        time += DIAL_TIME

        r = random.random()

        # Customer is busy
        if r < .2: # BUSY
            time += BUSY_TIME
        # Customer is unavailable
        elif r < .5:
            time += RING_TIME
        # Customer is available
        else: # AVAILABLE
            # Customer doesn't answer in time
            if X > RING_TIME:
                time += RING_TIME
            # Customer picks up
            else:
                time += X
                break

        time += END_TIME

    return time


def main():

    print("Random numbers:")
    for i in range(1, 4):
        print(f"\tu_{i} = {random_number_generator(i)}")
    print()
    for i in range(51, 54):
        print(f"\tu_{i} = {random_number_generator(i)}")
    print()

    N = 1000
    print(f"Running {N} trials.\n")

    times = []

    for trial in range(1, N+1):
        random_num = random_number_generator(trial)
        X = random_variable_generator(random_num)
        time = simulate(X)

        times.append(time)

    times = np.array(times)
    print(f"Finished running {N} trials.\n")

    print(f"Mean: {np.mean(times)}")
    print(f"First quartile: {np.quantile(times, .25)}")
    print(f"Median: {np.median(times)}")
    print(f"Third quartile: {np.quantile(times, .75)}\n")

    print_cdf(times, 15)
    print_cdf(times, 30)
    print_cdf(times, 20)
    print_cdf(times, 40, complementary=True)
    print_cdf(times, 70, complementary=True)
    print_cdf(times, 100, complementary=True)
    print_cdf(times, 120, complementary=True)




if __name__ == "__main__":
    main()