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

Hlist = []
Rlist = []
Llist = []
Vlist = []


def on_boundary(y, x):
    for h in Hlist:
        y1, x1, y2, x2 = h
        if y == y1 and x >= x1 and x <= x2:
            return True
    for v in Vlist:
        y1, x1, y2, x2 = v
        if x == x1 and y >= y1 and y <= y2:
            return True
    return False


if __name__ == "__main__":
    lines = []
    dig_map = []
    with open("./input.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line == "":
                continue
            lines.append(line.split(" "))

    # print(lines)
    max_width = 0
    max_deepth = 0
    min_width = 0
    min_deepth = 0
    width = 0
    deepth = 0
    d_map = {"0": "R", "1": "D", "2": "L", "3": "U"}
    for row in lines:
        # direction = d_map[row[2][-2]]
        # distance = int(row[2][2:-2], 16)
        direction = row[0]
        distance = int(row[1])
        if direction == "R":
            Rlist.append((deepth + 1, width + 1, deepth + 1, width + distance + 1))
            Hlist.append((deepth + 1, width + 1, deepth + 1, width + distance + 1))
            # print(f"go right {distance}")
            width += distance
        elif direction == "L":
            Llist.append((deepth + 1, width - distance + 1, deepth + 1, width + 1))
            Hlist.append((deepth + 1, width - distance + 1, deepth + 1, width + 1))
            # print(f"go left {distance}")
            width -= distance
        elif direction == "U":
            Vlist.append((deepth - distance + 1, width + 1, deepth + 1, width + 1))
            # print(f"go up {distance}")
            deepth -= distance
        elif direction == "D":
            Vlist.append((deepth + 1, width + 1, deepth + distance + 1, width + 1))
            # print(f"go down {distance}")
            deepth += distance
        max_width = max(max_width, width)
        max_deepth = max(max_deepth, deepth)
        min_width = min(min_width, width)
        min_deepth = min(min_deepth, deepth)
    print(max_width, max_deepth)
    print(min_width, min_deepth)
    if min_width != 0:
        for i, item in enumerate(Hlist):
            y1, x1, y2, x2 = item
            Hlist.pop(i)
            Hlist.insert(i, (y1, x1 - min_width, y2, x2 - min_width))
        for i, item in enumerate(Vlist):
            y1, x1, y2, x2 = item
            Vlist.pop(i)
            Vlist.insert(i, (y1, x1 - min_width, y2, x2 - min_width))
    if min_deepth != 0:
        for i, item in enumerate(Hlist):
            y1, x1, y2, x2 = item
            Hlist.pop(i)
            Hlist.insert(i, (y1 - min_deepth, x1, y2 - min_deepth, x2))
        for i, item in enumerate(Vlist):
            y1, x1, y2, x2 = item
            Vlist.pop(i)
            Vlist.insert(i, (y1 - min_deepth, x1, y2 - min_deepth, x2))
    new_width = (max_width - min_width + 1) + 2
    new_deepth = (max_deepth - min_deepth + 1) + 2

    #################################
    # Llist = list(reversed(Llist))
    # ri = 0
    # li = 0
    # while ri < len(Rlist) and li < len(Llist):
    #     rseg = Rlist[ri]
    #     lseg = Llist[li]
    #     if rseg[3] > lseg[3]:
    #         # break rseg
    #         rseg1 = (rseg[0], rseg[1], rseg[2], lseg[3])
    #         rseg2 = (rseg[0], lseg[3] + 1, rseg[2], rseg[3])
    #         Rlist.pop(ri)
    #         Rlist.insert(ri, rseg1)
    #         Rlist.insert(ri + 1, rseg2)
    #         ri += 1
    #         li += 1
    #     elif rseg[3] < lseg[3]:
    #         # break lseg
    #         lseg1 = (lseg[0], lseg[1], lseg[2], rseg[3])
    #         lseg2 = (lseg[0], rseg[3] + 1, lseg[2], lseg[3])
    #         Llist.pop(li)
    #         Llist.insert(li, lseg1)
    #         Llist.insert(li + 1, lseg2)
    #         ri += 1
    #         li += 1
    #     else:
    #         ri += 1
    #         li += 1
    # print(Rlist)
    # print(Llist)
    # exit()
    #################################

    # dig_map = np.empty((new_deepth, new_width), dtype=str)
    # dig_map.fill(".")
    # for h in Hlist:
    #     y1, x1, y2, x2 = h
    #     for x in range(x1, x2 + 1):
    #         dig_map[y1][x] = "#"
    # for v in Vlist:
    #     y1, x1, y2, x2 = v
    #     for y in range(y1, y2 + 1):
    #         dig_map[y][x1] = "#"
    # print(dig_map)

    heap = [(0, 0)]
    d = new_deepth
    w = new_width
    seen = []
    while len(heap) > 0:
        print(len(heap), len(seen))
        y, x = heapq.heappop(heap)
        seen.append((y, x))

        if (
            x - 1 >= 0
            and not on_boundary(y, x - 1)
            and ((y, x - 1) not in seen and (y, x - 1) not in heap)
        ):
            # print(f"({y}, {x-1}) not on boundary")
            heapq.heappush(heap, (y, x - 1))
        if (
            x + 1 < w
            and not on_boundary(y, x + 1)
            and ((y, x + 1) not in seen and (y, x + 1) not in heap)
        ):
            # print(f"({y}, {x+1}) not on boundary")
            heapq.heappush(heap, (y, x + 1))
        if (
            y - 1 >= 0
            and not on_boundary(y - 1, x)
            and ((y - 1, x) not in seen and (y - 1, x) not in heap)
        ):
            # print(len(dig_map), len(dig_map[0]))
            # print(y-1, x)
            # print(f"({y-1}, {x}) not on boundary")
            heapq.heappush(heap, (y - 1, x))
        if (
            y + 1 < d
            and not on_boundary(y + 1, x)
            and ((y + 1, x) not in seen and (y + 1, x) not in heap)
        ):
            # print(len(dig_map), len(dig_map[0]))
            # print(y+1, x)
            # print(f"({y+1}, {x}) not on boundary")
            heapq.heappush(heap, (y + 1, x))
    print(new_width, new_deepth, len(seen))
    print(new_deepth * new_width - len(seen))
    exit()

    ####################################
    # Part 1
    # for y in range(new_deepth):
    #    dig_map.append([])
    #    for x in range(new_width):
    #        dig_map[y].append(".")
    dig_map = np.empty((new_deepth, new_width), dtype=str)
    dig_map.fill(".")
    print(dig_map)
    # print(len(dig_map), len(dig_map[0]))
    # print(dig_map)
    start_x = 1 - min_width
    start_y = 1 - min_deepth
    for row in lines:
        # direction = d_map[row[2][-2]]
        # distance = int(row[2][2:-2], 16)
        direction = row[0]
        distance = int(row[1])
        if direction == "R":
            for x in range(start_x, start_x + distance + 1):
                dig_map[start_y][x] = "#"
            start_x += distance
        elif direction == "L":
            for x in range(start_x - distance, start_x):
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
    # for line in dig_map:
    #    print("".join(line))
    # exit()
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
    heap = [(0, 0)]
    d = len(new_map)
    w = len(new_map[0])
    while len(heap) > 0:
        y, x = heapq.heappop(heap)

        if x - 1 >= 0 and new_map[y][x - 1] != "#" and new_map[y][x - 1] != "x":
            # print(len(dig_map), len(dig_map[0]))
            # print(y, x-1)
            new_map[y][x - 1] = "x"
            heapq.heappush(heap, (y, x - 1))
        if x + 1 < w and new_map[y][x + 1] != "#" and new_map[y][x + 1] != "x":
            # print(len(dig_map), len(dig_map[0]))
            # print(y, x+1)
            new_map[y][x + 1] = "x"
            heapq.heappush(heap, (y, x + 1))
        if y - 1 >= 0 and new_map[y - 1][x] != "#" and new_map[y - 1][x] != "x":
            # print(len(dig_map), len(dig_map[0]))
            # print(y-1, x)
            new_map[y - 1][x] = "x"
            heapq.heappush(heap, (y - 1, x))
        if y + 1 < d and new_map[y + 1][x] != "#" and new_map[y + 1][x] != "x":
            # print(len(dig_map), len(dig_map[0]))
            # print(y+1, x)
            new_map[y + 1][x] = "x"
            heapq.heappush(heap, (y + 1, x))
    r = 0
    for line in new_map:
        r += line.count(".")
        r += line.count("#")
        print("".join(line))
    print(r)
