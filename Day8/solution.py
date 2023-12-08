import re
import os
from functools import cmp_to_key

from collections import OrderedDict

from multiprocessing import Pool, cpu_count
from functools import partial
from math import lcm

def is_done(starts):
    for s in starts:
        if s[2] != "Z":
            return False
    return True

def is_done2(pathes):
    for i in range(len(pathes[0])):
        slice = []
        for p in pathes:
            slice.append(p[i])
        if is_done(slice):
            return True, i
    return False, len(pathes[0])

def search_func(idx, starts, network, steps, directions, parts):
    ret = []
    next = starts[idx]
    for i in range(parts):
        d = directions[ i % len(directions)]
        if d == "L":
            next = network[next][0]
        else:
            next = network[next][1]
        ret.append(next)
    return ret

def search_func2(idx, pathes):
    tmp = []
    for i in range(len(pathes)):
        tmp.append(pathes[i][idx])
    if is_done(tmp):
        return 1
    return 0

def find_z(path):
    for i in range(len(path)):
        if path[i][2] == "Z":
            return i
    return -1

if __name__ == "__main__":
    directions = ""
    network = {}
    with open("./input.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line == "":
                continue
            if line.count("=") == 1:
                groups = re.match(r"(\w+) = \((\w+)\, (\w+)\)", line).groups()
                network[groups[0]] = (groups[1], groups[2])
                continue
            directions = line
    next = "AAA"
    end = "ZZZ"
    steps = 0
    while False:
        if next == end:
            break
        d = directions[steps % len(directions)]
        if d == "L":
            next = network[next][0]
        else:
            next = network[next][1]
        steps += 1
    
    starts = [ i for i in network.keys() if i[2] == "A"]

    print(starts)
    while True:
        pathes = [[]]
        parts = 1000 * len(directions)
        print("build")
        with Pool(processes=cpu_count()) as pool:
            pathes = pool.map(partial(search_func, starts=starts, network=network, steps=steps, directions=directions, parts=parts), range(len(starts)))

        result = 1
        num = []
        for path in pathes:
            index = find_z(path) + 1
            num.append(index)
            print(index)
            result = lcm(result, index)
        print(result)
        break