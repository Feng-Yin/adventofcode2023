import re
import os

from collections import OrderedDict

from multiprocessing import Pool, cpu_count 
from functools import partial

def search_func(time, totaltime, distance):
    if (totaltime - time) * time > distance:
        return 1
    return 0

if __name__ == '__main__':
    times = []
    distances = []
    with open("./input.txt", "r") as file:
        lines = []
        for line in file:
            lines.append(line)
        times = re.findall(r"\d+", lines[0])
        distances = re.findall(r"\d+", lines[1])

    print(lines, times, distances)
    result = 1
    for time, distance in zip(times, distances):
        print("search", time, distance)
        ways = 0
        with Pool(processes=cpu_count()) as pool:
            ways = pool.map(partial(search_func, totaltime=int(time), distance=int(distance)), range(int(time)))
        result *= sum(ways)
    print(result)

    result = 1
    print("search", "".join(times), "".join(distances))
    ways = 0
    with Pool(processes=cpu_count()) as pool:
        ways = pool.map(partial(search_func, totaltime=int("".join(times)), distance=int("".join(distances))), range(int("".join(times))))
    result *= sum(ways)
    print(result)
