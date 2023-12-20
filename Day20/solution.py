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

def single_low(heap, name):
    # low pulse is sent to name
    for item in heap:
        if item[1] == 0 and item[2] == name:
            return True
    return False

def single_high(heap, name):
    # high pulse is sent to name
    for item in heap:
        if item[1] == 1 and item[2] == name:
            return True
    return False

def print_to(names, current_heap, status):
    count = 0
    for item in current_heap:
        if item[2] in names:
            #print(f"{item[0]} -{"high" if item[1] == 1 else "low"}-> {item[2]}")
            if item[1] == status:
                count += 1
    return count

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
    all_map_copy = copy.deepcopy(all_map)
    count = 0
    current_heap = []
    next_heap = []
    high, low = 0, 0
    ac=0
    bc=0
    cc=0
    dc=0
    #while count == 0 or all_map != all_map_copy:
    while True:
    #for i in range(1000):
        count += 1
        heapq.heappush(next_heap, ("button", 0, "broadcaster"))
        while len(next_heap) > 0:
            current_heap = copy.deepcopy(next_heap)
            next_heap = []
            #print_heap(current_heap)
            #h, l = count_high_low(current_heap)
            #high += h
            #low += l
            # if single_low(current_heap, "dx"):
            #     print(f"dx count:{count}")
            #     #exit()
            # if single_low(current_heap, "ck"):
            #     print(f"ck count:{count}")
            #     #exit()
            # if single_low(current_heap, "cs"):
            #     print(f"cs count:{count}")
            #     #exit()
            # if single_low(current_heap, "jh"):
            #     print(f"jh count:{count}")
            #     #exit()
            # if single_high(current_heap, "mp"):
            #     print(f"mp count:{count}")
            #     #exit()
            # if single_high(current_heap, "qt"):
            #     print(f"qt count:{count}")
            #     #exit()
            # if single_high(current_heap, "qb"):
            #     print(f"qb count:{count}")
            #     #exit()
            # if single_high(current_heap, "ng"):
            #     print(f"ng count:{count}")
            #     #exit()
            #if single_low(current_heap, "dr"):
            #   print(f"dr count:{count}")
            #   #exit()
            # if single_low(current_heap, "rx"):
            #     print(f"rx count:{count}")
            #     #exit()
            # print_to(["dr"], current_heap)
            a = ['zz', 'ch', 'qp', 'rm', 'dd', 'tn', 'rr', 'xz']
            b = ['rj', 'hr', 'pl', 'rk', 'cg', 'kd', 'xq', 'km', 'ns']
            c = ['ls', 'pq', 'kk', 'pj', 'pr', 'tl', 'tc', 'vn', 'pm', 'jd']
            d = ['st', 'gg', 'cr', 'fl', 'rz', 'jg', 'sg', 'ps', 'nx']
            if ac == 0 and check_map(a, all_map, 1) == len(a):
                print(f"a count:{count}")
                ac = count
            if bc == 0 and check_map(b, all_map, 1) == len(b):
                print(f"b count:{count}")
                bc = count
            if cc == 0 and check_map(c, all_map, 1) == len(c):
                print(f"c count:{count}")
                cc = count
            if dc == 0 and check_map(d, all_map, 1) == len(d):
                print(f"d count:{count}")
                dc = count
            if ac != 0 and bc != 0 and cc != 0 and dc != 0:
                print(f"{ac*bc*cc*dc}")
                exit()
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
    print(high*low)