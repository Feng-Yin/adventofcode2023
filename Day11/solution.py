import re
import os
from functools import cmp_to_key

from collections import OrderedDict

from multiprocessing import Pool, cpu_count
from functools import partial

import numpy as np
values = np.array([1,2,3,1,2,4,5,6,3,2,1])
searchval = 3
ii = np.where(values == searchval)[0]

def expand_map_v(maps):
    expanded_maps = []
    for row in maps:
        tmp_row = []
        for idx, char in enumerate(row):
            if char == ".":
                tmp_row.append(char)
            else:
                tmp_row.append(char)
                tmp_row.append(char)
        expanded_maps.append(tmp_row)
        expanded_maps.append(tmp_row)
    return expanded_maps

if __name__ == "__main__":
    maps = []
    tmp_maps = []
    startx = 0
    starty = 0
    count_maps = []
    empty_row = []
    empty_col = []
    original_g_list = []
    with open("./input.txt", "r") as file:
        for ix, line in enumerate(file):
            line = line.strip()
            if line == "":
                continue
            tmp_row = []
            for idx, char in enumerate(line):
                tmp_row.append(char)
            values = np.array(tmp_row)
            searchval = "#"
            ii = np.where(values == searchval)[0]
            for iy in ii:
                original_g_list.append((ix, iy))
            maps.append(tmp_row)
            tmp_maps.append(tmp_row)
            if tmp_row.count(".") == len(tmp_row):
                empty_row.append(ix)
                tmp_maps.append(tmp_row)
    rotate_maps = list(zip(*tmp_maps[::-1]))
    expand_rotate_maps = []
    for row in rotate_maps:
        expand_rotate_maps.append(list(row))
        if row.count(".") == len(row):
            expand_rotate_maps.append(list(row))
    # find all g
    g_list = []
    for idy, row in enumerate(expand_rotate_maps):
        values = np.array(row)
        searchval = "#"
        ii = np.where(values == searchval)[0]
        for idx in ii:
            g_list.append((idx, idy))
    r = 0
    for idx, g in enumerate(g_list):
        if idx == len(g_list) - 1:
            break
        x1, y1 = g
        for x2, y2 in g_list[idx+1:]:
            r += abs(x1 - x2) + abs(y1 - y2)
    print(r)
    #########################################
    # part 2
    print(empty_row)
    r_maps = list(zip(*maps[::-1]))
    for iy, row in enumerate(r_maps):
        if row.count(".") == len(row):
            empty_col.append(iy)
    print(empty_col)

    r = 0
    for idx, g in enumerate(original_g_list):
        if idx == len(original_g_list) - 1:
            break
        x1, y1 = g
        for x2, y2 in original_g_list[idx+1:]:
            xb = max(x1, x2)
            xs = min(x1, x2)
            add_empty = 0
            for x in empty_row:
                if xs < x < xb:
                    #print("one empty row")
                    add_empty += 1
            yb = max(y1, y2)
            ys = min(y1, y2)
            for x in empty_col:
                if ys < x < yb:
                    #print("one empty col")
                    add_empty += 1
            #print("total empty", add_empty, "for", g, (x2, y2))
            r += abs(x1 - x2) + abs(y1 - y2) + add_empty * (1000000-1)
    print(r)