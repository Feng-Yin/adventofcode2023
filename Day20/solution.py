import re
import os
from functools import cmp_to_key

from collections import OrderedDict

from multiprocessing import Pool, cpu_count
from functools import partial
import copy
import heapq
import numpy as np
from functools import lru_cache as cached


class module:
    def __init__(self, str):
        groups = str.split(" -> ")
        self.listeners = groups[1].split(", ")
        self.status = 0
        self.inputs = {}
        if "%" in groups[0]:
            self.type = "ff"
            self.name = groups[0][1:]
        elif "&" in groups[0]:
            self.type = "con"
            self.name = groups[0][1:]
        else:
            self.type = "broadcaster"
            self.name = groups[0]

    def __repr__(self):
        return f"name:{self.name} type:{self.type} listeners:{self.listeners} status:{self.status} inputs:{self.inputs}"
    
    def __eq__(self, other): 
        return self.name == other.name and self.type == other.type and self.listeners == other.listeners and self.status == other.status and self.inputs == other.inputs

def print_heap(heap):
    for item in heap:
        print(f"{item[0]} -{"high" if item[1] == 1 else "low"}-> {item[2]}")

def count_high_low(heap):
    high = 0
    low = 0
    for item in heap:
        if item[1] == 1:
            high += 1
        else:
            low += 1

    return high, low

def check_map(names, map, status):
    count = 0
    for name in names:
        if map[name].status == status:
            count += 1
    return count

if __name__ == "__main__":
    lines = []
    dig_map = []
    with open("./input.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line == "":
                continue
            lines.append(line)
    all_map = {}
    ff_map = {}
    con_map = {}
    for line in lines:
        m = module(line)
        all_map[m.name] = m
        if m.type == "ff":
            ff_map[m.name] = m
        elif m.type == "con":
            con_map[m.name] = m
    for ck, cv in con_map.items():
        for k, v in all_map.items():
            if ck in v.listeners:
                cv.inputs[k] = 0
    #print(all_map)
    count = 0
    current_heap = []
    next_heap = []
    high, low = 0, 0
    ac=0
    bc=0
    cc=0
    dc=0
    #####################################
    # part 2
    while True:
    #####################################
    # part 1
    #for i in range(1000):
    #####################################
        if count == 1000:
            print(f"part 1: {high*low}")
        count += 1
        heapq.heappush(next_heap, ("button", 0, "broadcaster"))
        while len(next_heap) > 0:
            current_heap = copy.deepcopy(next_heap)
            next_heap = []
            #####################################
            # part 1
            #print_heap(current_heap)
            h, l = count_high_low(current_heap)
            high += h
            low += l
            #####################################
            # part 2
            a = ['zz', 'ch', 'qp', 'rm', 'dd', 'tn', 'rr', 'xz']
            b = ['rj', 'hr', 'pl', 'rk', 'cg', 'kd', 'xq', 'km', 'ns']
            c = ['ls', 'pq', 'kk', 'pj', 'pr', 'tl', 'tc', 'vn', 'pm', 'jd']
            d = ['st', 'gg', 'cr', 'fl', 'rz', 'jg', 'sg', 'ps', 'nx']
            if ac == 0 and check_map(a, all_map, 1) == len(a):
                #print(f"a count:{count}")
                ac = count
            if bc == 0 and check_map(b, all_map, 1) == len(b):
                #print(f"b count:{count}")
                bc = count
            if cc == 0 and check_map(c, all_map, 1) == len(c):
                #print(f"c count:{count}")
                cc = count
            if dc == 0 and check_map(d, all_map, 1) == len(d):
                #print(f"d count:{count}")
                dc = count
            if ac != 0 and bc != 0 and cc != 0 and dc != 0:
                print(f"part 2: {ac*bc*cc*dc}")
                exit()
            #####################################
            while len(current_heap) > 0:
                source, input, destination = heapq.heappop(current_heap)
                if destination not in all_map:
                    continue
                module = all_map[destination]
                if module.type == "broadcaster":
                    for listener in all_map["broadcaster"].listeners:
                        heapq.heappush(next_heap, (module.name, 0, listener))
                elif module.type == "ff":
                    if input == 0:
                        module.status = (module.status + 1) % 2
                        for listener in module.listeners:
                            heapq.heappush(next_heap, (module.name, module.status, listener))
                elif module.type == "con":
                    module.inputs[source] = input
                    #print(f"{module.name}'s inpus {module.inputs}")
                    output = 0 if len(module.inputs) == sum(module.inputs.values()) else 1
                    for listener in module.listeners:
                        heapq.heappush(next_heap, (module.name, output, listener))