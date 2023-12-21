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


def count_v(steps, steps_type):
    r = 0
    for k, v in steps.items():
        if v % 2 == steps_type:
            # print(k)
            r += 1
    return r


if __name__ == "__main__":
    lines = []
    dig_map = []
    start_y = 0
    start_x = 0
    steps_map = {}
    seen = {}
    with open("./input.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line == "":
                continue
            lines.append(list(line))
    total = 0
    for yi, line in enumerate(lines):
        for xi, ch in enumerate(line):
            if ch == "S":
                start_y = yi
                start_x = xi
            if ch == "S" or ch == ".":
                total += 1
    print(f"total: {total}")
    for i in range(10):
        print(i * (i + 1) * 15410 + 134 * i + 3916)
    i = int(26501365 / 131)
    print(i * (i + 1) * 15410 + 134 * i + 3916)
    exit()

    c_y = start_y
    c_x = start_x
    c_heap = []
    n_heap = []
    height = len(lines)
    width = len(lines[0])
    steps = 26501365
    heapq.heappush(n_heap, (c_y, c_x))
    seen[(c_y, c_x)] = 1
    print(height, width)
    up_s = (start_y - height, start_x)
    down_s = (start_y + height, start_x)
    left_s = (start_y, start_x - width)
    right_s = (start_y, start_x + width)
    garden = 0
    for i in range(0, steps + 1):
        # print(f"step {i}, heap len {len(n_heap)}")
        c_heap = copy.deepcopy(n_heap)
        n_heap = []
        while len(c_heap) > 0:
            c_y, c_x = heapq.heappop(c_heap)
            steps_map[(c_y, c_x)] = i
            if (
                # c_y - 1 >= 0 and
                (c_y - 1, c_x) not in seen
                and lines[(c_y - 1) % height][c_x % width] != "#"
            ):
                heapq.heappush(n_heap, (c_y - 1, c_x))
                seen[(c_y - 1, c_x)] = 1
            if (
                # c_y + 1 < height and
                (c_y + 1, c_x) not in seen
                and lines[(c_y + 1) % height][c_x % width] != "#"
            ):
                heapq.heappush(n_heap, (c_y + 1, c_x))
                seen[(c_y + 1, c_x)] = 1
            if (
                # c_x - 1 >= 0 and
                (c_y, c_x - 1) not in seen
                and lines[c_y % height][(c_x - 1) % width] != "#"
            ):
                heapq.heappush(n_heap, (c_y, c_x - 1))
                seen[(c_y, c_x - 1)] = 1
            if (
                # c_x + 1 < width and
                (c_y, c_x + 1) not in seen
                and lines[c_y % height][(c_x + 1) % width] != "#"
            ):
                heapq.heappush(n_heap, (c_y, c_x + 1))
                seen[(c_y, c_x + 1)] = 1
        if up_s in steps_map:
            # print(f"up s {up_s}: with {i} steps")
            up_s = (up_s[0] - height, up_s[1])
        if down_s in steps_map:
            # print(f"down s {down_s}: with {i} steps")
            down_s = (down_s[0] + height, down_s[1])
        if left_s in steps_map:
            # print(f"left s {left_s}: with {i} steps")
            left_s = (left_s[0], left_s[1] - width)
        if right_s in steps_map:
            # print(f"right s {right_s}: with {i} steps")
            right_s = (right_s[0], right_s[1] + width)
            tmp = count_v(steps=steps_map, steps_type=i % 2)
            # print(f"Garden {tmp} delta {tmp-garden}")
            garden = tmp
        if i % 131 == 65:
            print(f"Garden {count_v(steps=steps_map, steps_type=i % 2)}")
    # print(steps_map)
    # r = 0
    # for k, v in steps_map.items():
    #     if v % 2 == 0:
    #         # print(k)
    #         r += 1
    # print(r)
