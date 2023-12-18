import re
import os
from functools import cmp_to_key

from collections import OrderedDict

from multiprocessing import Pool, cpu_count
from functools import partial

import numpy as np
import copy
from progressbar import progressbar

def is_same(plate, rotate_plate):
    for r1, r2 in zip(plate, rotate_plate):
        if r1 != r2.tolist():
            return False
    return True

def get_value(plate):
    r = 0
    for ix, row in enumerate(plate):
        r += row.tolist().count("O") * (len(plate) - ix)
    return r

def repeatedSubstring(source):
    """Look for the shortest substring which when repeated equals
        the source string, without any left over characters.
    """
    length = len(source)
    print('\nOriginal text: {}. Length: {}'.format(source, length))

    # Check candidate strings
    for i in range(1, int(length/2)+1):
        repeat_count, leftovers = divmod(length, i)
        # print 'i: {}, sub: {}, div: {}, mod: {}'.format(i, source[:i], repeat_count, leftovers)
        # print 'repeated: {}'.format(source[:i]*repeat_count)

        # Check for no leftovers characters, and equality when repeated 
        if (leftovers == 0) and (source == source[:i]*repeat_count):
            print('Found repeated substring: {}, count: {}'.format(source[:i], repeat_count))
            break
    else:
        print("Couldn't find any repeated substring")

if __name__ == "__main__":
    plate = []
    with open("./input.txt", "r") as file:
        for ix, line in enumerate(file):
            line = line.strip()
            if line == "":
                continue
            plate.append(list(line))
    #print(plate)
    rotate_plate = copy.deepcopy(plate)

    #for i in range(1000000000):
    v_list = []
    for i in progressbar(range(1000)):
        rotate_plate = np.rot90(rotate_plate, k=1)
        #print(rotate_plate)
        for row in rotate_plate:
            #shift rock
            sharp_ix = -1
            for ix, char in enumerate(row):
                if char == "#":
                    sharp_ix = ix
                    continue
                if char == ".":
                    continue
                if char == "O":
                    start_ix = sharp_ix + 1
                    while start_ix != ix:
                        if row[start_ix] == ".":
                            row[start_ix] = "O"
                            row[ix] = "."
                            break
                        start_ix += 1
        #print(rotate_plate)
        rotate_plate = np.rot90(rotate_plate, k=3)
        #print(rotate_plate)
        ############################
        #count for part1
        #r = 0
        #for ix, row in enumerate(rotate_plate):
        #   r += row.tolist().count("O") * (len(rotate_plate) - ix)
        #print(r)
        ############################
        # go west
        for row in rotate_plate:
            #shift rock
            sharp_ix = -1
            for ix, char in enumerate(row):
                if char == "#":
                    sharp_ix = ix
                    continue
                if char == ".":
                    continue
                if char == "O":
                    start_ix = sharp_ix + 1
                    while start_ix != ix:
                        if row[start_ix] == ".":
                            row[start_ix] = "O"
                            row[ix] = "."
                            break
                        start_ix += 1
        # go west
        rotate_plate = np.rot90(rotate_plate, k=3)
        for row in rotate_plate:
            #shift rock
            sharp_ix = -1
            for ix, char in enumerate(row):
                if char == "#":
                    sharp_ix = ix
                    continue
                if char == ".":
                    continue
                if char == "O":
                    start_ix = sharp_ix + 1
                    while start_ix != ix:
                        if row[start_ix] == ".":
                            row[start_ix] = "O"
                            row[ix] = "."
                            break
                        start_ix += 1
        rotate_plate = np.rot90(rotate_plate, k=1)
        # go east
        rotate_plate = np.rot90(rotate_plate, k=2)
        for row in rotate_plate:
            #shift rock
            sharp_ix = -1
            for ix, char in enumerate(row):
                if char == "#":
                    sharp_ix = ix
                    continue
                if char == ".":
                    continue
                if char == "O":
                    start_ix = sharp_ix + 1
                    while start_ix != ix:
                        if row[start_ix] == ".":
                            row[start_ix] = "O"
                            row[ix] = "."
                            break
                        start_ix += 1
        rotate_plate = np.rot90(rotate_plate, k=2)
        if is_same(plate, rotate_plate):
            print(f"{i} is the report point")
            break
        #else:
        #    print(f"{i}/1000000000")
        v_list.append(get_value(rotate_plate))
        print(get_value(rotate_plate))
    #print(",".join(map(str, v_list)))
    #repeatedSubstring(" ".join(map(str, v_list)))
    ############################
    #count for part2
    #r = 0
    #for ix, row in enumerate(rotate_plate):
    #   r += row.tolist().count("O") * (len(rotate_plate) - ix)
    #print(r)
    ############################
