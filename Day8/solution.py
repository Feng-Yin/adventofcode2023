import re
import os
from functools import cmp_to_key

from collections import OrderedDict

from multiprocessing import Pool, cpu_count
from functools import partial

def is_done(starts):
    for s in starts:
        if s[2] != "Z":
            return False
    return True

def search_func(idx, starts, network, steps, directions):
    d = directions[steps % len(directions)]
    if d == "L":
        starts[idx] = network[starts[idx]][0]
    else:
        starts[idx] = network[starts[idx]][1]
    return starts[idx]


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
        if is_done(starts):
            break
        d = directions[steps % len(directions)]
    
        with Pool(processes=cpu_count()) as pool:
            starts = pool.map(partial(search_func, starts=starts, network=network, steps=steps, directions=directions), range(len(starts)))

        #for idx, start in enumerate(starts):
        #    if d == "L":
        #        starts[idx] = network[starts[idx]][0]
        #    else:
        #        starts[idx] = network[starts[idx]][1]
        #print(starts)
        steps += 1
    print(steps)
