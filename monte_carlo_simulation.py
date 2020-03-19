# runs simulations of the calling process described in the project
# the RNG class is used for generating random numbers
# we only used numpy to compute the quartiles
import math
import numpy as np


class RNG:
    def __init__(self, x_0, a, c, k):
        self.seed = x_0
        self.multiplier = a
        self.increment = c
        self.modulus = k
        self.nums = []

    def generate(self, n=1000):
        """
        Generates n random numbers and returns as a list
        :param n: number of random numbers to generate
        :return: a list of random numbers of length n
        """
        ret = []
        x_i = self.seed
        for i in range(n):
            x_i = (x_i * self.multiplier + self.increment) % self.modulus  # x_i = (x_i-1 * a + c) % K
            ret.append(x_i / self.modulus)  # u_i = x_i / K
        self.nums = ret
        return ret

    def show_51(self):
        """returns u_51, u_52, and u_53. Used for the report"""
        nums = self.generate(55)
        return nums[50], nums[51], nums[52]


def map_rand(u, lam=1 / 12):
    """returns a realization of an exponential random variable with parameter lambda given a random number u"""
    ret = (-1 / lam) * math.log(1 - u)
    # print("F^-1(" + str(u) + "):", ret, end=" --> ")
    return ret


def simulate_call(queue, display_output=False):
    """runs a simulation of the calling process and returns the time in seconds that the process took
    displays debugging prints if display_output is set to true"""
    tries = 1
    t = 0
    while tries <= 4:  # gives up after 4 tries
        u = queue.pop(0)  # get a new random number
        t += 6  # 6 seconds to dial the call
        if u <= .2:
            t += 4  # 3 seconds to detect busy line + 1 second to hang up
            if display_output:
                print("line busy, on try #", tries, "seconds so far:", t)
        elif u <= .5:
            t += 26  # 25s to wait for ringing + 1s to hang up
            if display_output:
                print("no answer on try #", tries, "seconds so far:", t)
        elif u <= 1:
            # print("client answered, u =", u)
            u = queue.pop(0)
            t += map_rand(u, 1 / 12)  # use a new random number to determine the wait time
            if display_output:
                print("client answered after", tries, "tries! Total time:", t)
            return t  # process is complete if phone is answered
        tries += 1
    if display_output:
        print("gave up after 4 tries. Total time:", t)
    return t


def run_mcs(n, display_output=False):
    """runs the Monte-Carlo Simulation (MCS) n times and returns a list of n trial times
    displays debugging prints if display_output is set to true"""
    rng = RNG(1000, 24693, 3517, 2**15)  # make a random number generator with the same parameters as the example
    rand_queue = rng.generate(n*5)  # I'm using a queue so that each random number is used exactly once
    # Each iteration needs at most 5 random numbers, so I had the RNG generate n*5 numbers just to be 100% safe
    times = []  # return value
    for i in range(n):
        if display_output:
            print("---------- simulation", i + 1, "-----------")
        times.append(simulate_call(rand_queue))
    if display_output:
        print("simulation time results:", times)
    return times


def parse_times(times):
    """returns a tuple with the following statistics of the parameter list (respectively)
    (mean, min, first quartile, median, third quartile, max"""
    quartiles = np.percentile(times, [0, 25, 50, 75, 100])
    return np.mean(times), quartiles[0], quartiles[1], quartiles[2], quartiles[3], quartiles[4]

