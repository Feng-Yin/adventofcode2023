import re
import os
from functools import cmp_to_key

from collections import OrderedDict

from multiprocessing import Pool, cpu_count
from functools import partial

import numpy as np
import copy

def find_center(input_map):
    max_len = 0
    for ix, line in enumerate(input_map):
        counts = min(ix+1, len(input_map) - ix - 1)
        is_mirror = True
        for offset in range(counts):
            #print(f"for {ix} compare Line {ix-offset}: {ix+offset+1}")
            #print(f"for {ix} compare Line {input_map[ix-offset]}: {input_map[ix+offset+1]}")
            if input_map[ix-offset] != input_map[ix+offset+1]:
                # not a mirror
                is_mirror = False
                #print(f"Line {ix-offset} is not a mirror")
                break
        if is_mirror and ix < len(input_map) - 1:
            #print(f"Line {ix} is a mirror")
            max_len = max(max_len, ix+1)
    return max_len

def find_all_center(input_map):
    all_m = []
    for ix, line in enumerate(input_map):
        counts = min(ix+1, len(input_map) - ix - 1)
        is_mirror = True
        for offset in range(counts):
            #print(f"for {ix} compare Line {ix-offset}: {ix+offset+1}")
            #print(f"for {ix} compare Line {input_map[ix-offset]}: {input_map[ix+offset+1]}")
            if input_map[ix-offset] != input_map[ix+offset+1]:
                # not a mirror
                is_mirror = False
                #print(f"Line {ix-offset} is not a mirror")
                break
        if is_mirror and ix < len(input_map) - 1:
            #print(f"Line {ix} is a mirror")
            all_m.append(ix+1)
    return all_m


if __name__ == "__main__":
    map_list = []
    with open("./input.txt", "r") as file:
        tmp_map = []
        for ix, line in enumerate(file):
            line = line.strip()
            if line != "":
                tmp_map.append(list(line))
            else:
                #print(f"Map: {tmp_map}")
                if len(tmp_map) > 0:
                    map_list.append(tmp_map)
                    tmp_map = []
        if len(tmp_map) > 0:
            map_list.append(tmp_map)
    r = 0
    olds = []
    for tmp_map in map_list:
        copy_map = copy.deepcopy(tmp_map)
        # find H value
        h = find_center(copy_map)
        #find V value
        rotate_maps = [list(i) for i in list(zip(*copy_map[::-1]))]
        v = find_center(rotate_maps)
        #print(f"h v: {h} {v}")
        r += h * 100 + v
        olds.append([h, v])
    print(f"Result: {r}")
    #######################################################
    # Second part
    r = 0
    i = 0
    for tmp_map, old in zip(map_list, olds):
        found_smuge = False
        for ix in range(len(tmp_map)):
            for iy in range(len(tmp_map[ix])):
                copy_map = copy.deepcopy(tmp_map)
                if copy_map[ix][iy] == "#":
                    copy_map[ix][iy] = "."
                else:
                    copy_map[ix][iy] = "#"
                #print(f"try: {ix, iy}")
                #print(f"copy_map: {copy_map}")
                # find H value
                h = find_all_center(copy_map)
                #find V value
                rotate_maps = [list(i) for i in list(zip(*copy_map[::-1]))]
                #print(f"rotate_maps: {rotate_maps}")
                v = find_all_center(rotate_maps)
                #print(f"before dedup h v: {h,v} {old}")
                finalh = 0
                finalv = 0
                for nh in h:
                    if nh != old[0] and nh > 0:
                        finalh = nh
                for nv in v:
                    if nv != old[1] and nv > 0:
                        finalv = nv

                if finalh + finalv > 0:
                    r += finalh * 100 + finalv
                    found_smuge = True
                    break
            if found_smuge:
                break
        i += 1
        if not found_smuge:
            print("Not found smuge", i)
    print(f"Result: {r}")