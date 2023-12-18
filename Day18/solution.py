import re
import os
from functools import cmp_to_key

from collections import OrderedDict

from multiprocessing import Pool, cpu_count
from functools import partial
import copy
import heapq
import numpy as np


if __name__ == "__main__":
    lines = []
    dig_map = []
    with open("./input.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line == "":
                continue
            lines.append(line.split(" "))

    #print(lines)
    max_width = 0
    max_deepth = 0
    min_width = 0
    min_deepth = 0
    width = 1
    deepth = 1
    d_map = {"0": "R", "1": "D", "2": "L", "3": "U"}
    for row in lines:
        direction = d_map[row[2][-2]]
        distance = int(row[2][2:-2], 16)
        #direction = row[0]
        #distance = int(row[1])
        if direction == "R":
            width += distance
        elif direction == "L":
            width -= distance
        elif direction == "U":
            deepth -= distance
        elif direction == "D":
            deepth += distance
        max_width = max(max_width, width)
        max_deepth = max(max_deepth, deepth)
        min_width = min(min_width, width)
        min_deepth = min(min_deepth, deepth)
    print(max_width, max_deepth)
    print(min_width, min_deepth)
    new_width = max_width - min_width + 3
    new_deepth = max_deepth - min_deepth + 3
    for y in range(new_deepth):
        dig_map.append([])
        for x in range(new_width):
            dig_map[y].append(".")
    print(len(dig_map), len(dig_map[0]))
    #print(dig_map)
    start_x = 1 - min_width + 1
    start_y = 1 - min_deepth + 1
    for row in lines:
        direction = d_map[row[2][-2]]
        distance = int(row[2][2:-2], 16)
        #direction = row[0]
        #distance = int(row[1])
        if direction == "R":
            for x in range(start_x, start_x + distance + 1):
                dig_map[start_y][x] = "#"
            start_x += distance
        elif direction == "L":
            for x in range(start_x - distance, start_x ):
                dig_map[start_y][x] = "#"
            start_x -= distance
        elif direction == "U":
            for y in range(start_y - distance, start_y):
                dig_map[y][start_x] = "#"
            start_y -= distance
        elif direction == "D":
            for y in range(start_y, start_y + distance + 1):
                dig_map[y][start_x] = "#"
            start_y += distance
    #for line in dig_map:
    #    print("".join(line))
    #exit()
    # while True:
    #     if "#" not in dig_map[1]:
    #         dig_map.pop(1)
    #     else:
    #         break
    # while True:
    #     if "#" not in dig_map[-2]:
    #         dig_map.pop(-2)
    #     else:
    #         break
    rotate_map = np.rot90(dig_map)
    new_map = []
    for line in rotate_map:
        new_map.append(list(line))
    # while True:
    #     if "#" not in new_map[1]:
    #         new_map.pop(1)
    #     else:
    #         break
    # while True:
    #     if "#" not in new_map[-2]:
    #         new_map.pop(-2)
    #     else:
    #         break
    
    new_map[0][0] = "x"
    heap = [(0,0)]
    d = len(new_map)
    w = len(new_map[0])
    while len(heap) > 0:
        y, x = heapq.heappop(heap)

        if x - 1 >= 0 and new_map[y][x-1] != "#" and new_map[y][x-1] != "x":
            #print(len(dig_map), len(dig_map[0]))
            #print(y, x-1)
            new_map[y][x-1] = "x"
            heapq.heappush(heap, (y, x - 1))
        if x + 1 < w and new_map[y][x+1] != "#" and new_map[y][x+1] != "x":
            #print(len(dig_map), len(dig_map[0]))
            #print(y, x+1)
            new_map[y][x+1] = "x"
            heapq.heappush(heap, (y, x + 1))
        if y -1>= 0 and new_map[y-1][x] != "#" and new_map[y-1][x] != "x":
            #print(len(dig_map), len(dig_map[0]))
            #print(y-1, x)
            new_map[y-1][x] = "x"
            heapq.heappush(heap, (y-1, x))
        if y + 1 < d and new_map[y+1][x] != "#" and new_map[y+1][x] != "x":
            #print(len(dig_map), len(dig_map[0]))
            #print(y+1, x)
            new_map[y+1][x] = "x"
            heapq.heappush(heap, (y+1, x))
    r = 0
    for line in new_map:
        r += line.count(".")
        r += line.count("#")
        print("".join(line))
    print(r)
    
    