import re
import os
from functools import cmp_to_key

from collections import OrderedDict

from multiprocessing import Pool, cpu_count
from functools import partial

import numpy as np
import copy

north = 0
east = 1
south = 2
west = 3

stack = []
input = []
empty_map = []
repeat_detect = []


def print_rep():
    for line in repeat_detect:
        print(line)


def check_repeat(y, x, direction):
    if repeat_detect_cp[y][x] == ".":
        repeat_detect_cp[y][x] = [direction]
        # print(f"add {y}, {x}, {direction}, {repeat_detect[y][x]}")
        return False
    if direction in repeat_detect_cp[y][x]:
        # print(f"repeat {y}, {x}, {repeat_detect[y][x]}")
        return True
    repeat_detect_cp[y][x].append(direction)
    # print(f"add {y}, {x}, {direction}, {repeat_detect[y][x]}")
    return False


def move():
    y, x, direction = stack.pop()
    empty_map_cp[y][x] = "#"
    if check_repeat(y, x, direction):
        return
    if input[y][x] == ".":
        if direction == east:
            if x + 1 < len(input[0]):
                stack.append((y, x + 1, east))
            return
        if direction == south:
            if y + 1 < len(input):
                stack.append((y + 1, x, south))
            return
        if direction == west:
            if x - 1 >= 0:
                stack.append((y, x - 1, west))
            return
        if direction == north:
            if y - 1 >= 0:
                stack.append((y - 1, x, north))
            return
        return
    if input[y][x] == "|":
        if direction == east or direction == west:
            if y + 1 < len(input):
                stack.append((y + 1, x, south))
            if y - 1 >= 0:
                stack.append((y - 1, x, north))
            return
        if direction == south:
            if y + 1 < len(input):
                stack.append((y + 1, x, south))
            return
        if direction == north:
            if y - 1 >= 0:
                stack.append((y - 1, x, north))
            return
        return
    if input[y][x] == "-":
        if direction == east:
            if x + 1 < len(input[0]):
                stack.append((y, x + 1, east))
            return
        if direction == south or direction == north:
            if x + 1 < len(input[0]):
                stack.append((y, x + 1, east))
            if x - 1 >= 0:
                stack.append((y, x - 1, west))
            return
        if direction == west:
            if x - 1 >= 0:
                stack.append((y, x - 1, west))
            return
        return
    if input[y][x] == "\\":
        if direction == east:
            if y + 1 < len(input):
                stack.append((y + 1, x, south))
            return
        if direction == south:
            if x + 1 < len(input[0]):
                stack.append((y, x + 1, east))
            return
        if direction == west:
            if y - 1 >= 0:
                stack.append((y - 1, x, north))
            return
        if direction == north:
            if x - 1 >= 0:
                stack.append((y, x - 1, west))
            return
        return
    if input[y][x] == "/":
        if direction == east:
            if y - 1 >= 0:
                stack.append((y - 1, x, north))
            return
        if direction == south:
            if x - 1 >= 0:
                stack.append((y, x - 1, west))
            return
        if direction == west:
            if y + 1 < len(input):
                stack.append((y + 1, x, south))
            return
        if direction == north:
            if x + 1 < len(input[0]):
                stack.append((y, x + 1, east))
            return
        return


if __name__ == "__main__":
    with open("./input.txt", "r") as file:
        for ix, line in enumerate(file):
            line = line.strip()
            if line == "":
                continue
            input.append(list(line))
            empty_map.append(list("." * len(line)))
            repeat_detect.append(list("." * len(line)))
    # print(input)
    # print(empty_map)
    # print(repeat_detect)
    ############################################
    # part 1
    ############################################
    # stack.append((0, 0, east))
    # while len(stack) > 0:
    #     # for i in range(30):
    #     move()
    #     # for line in empty_map:
    #     #    print(line)
    #     # print("=" * 20)
    #     # print(stack)
    # r = 0
    # for line in empty_map:
    #     r += line.count("#")
    # print(r)

    ############################################
    # part 2
    ############################################
    # top row
    fr = 0
    for x in range(len(input[0])):
        empty_map_cp = copy.deepcopy(empty_map)
        repeat_detect_cp = copy.deepcopy(repeat_detect)
        stack = []
        stack.append((0, x, south))
        while len(stack) > 0:
            # for i in range(30):
            move()
            # for line in empty_map:
            #    print(line)
            # print("=" * 20)
        # print(stack)
        r = 0
        for line in empty_map_cp:
            r += line.count("#")
        fr = max(r, fr)
    # bottom row
    for x in range(len(input[0])):
        empty_map_cp = copy.deepcopy(empty_map)
        repeat_detect_cp = copy.deepcopy(repeat_detect)
        stack = []
        stack.append((len(input) - 1, x, north))
        while len(stack) > 0:
            # for i in range(30):
            move()
            # for line in empty_map:
            #    print(line)
            # print("=" * 20)
        # print(stack)
        r = 0
        for line in empty_map_cp:
            r += line.count("#")
        fr = max(r, fr)
    # left col
    for y in range(len(input)):
        empty_map_cp = copy.deepcopy(empty_map)
        repeat_detect_cp = copy.deepcopy(repeat_detect)
        stack = []
        stack.append((y, 0, east))
        while len(stack) > 0:
            # for i in range(30):
            move()
            # for line in empty_map:
            #    print(line)
            # print("=" * 20)
        # print(stack)
        r = 0
        for line in empty_map_cp:
            r += line.count("#")
        fr = max(r, fr)

    # right col
    for y in range(len(input)):
        empty_map_cp = copy.deepcopy(empty_map)
        repeat_detect_cp = copy.deepcopy(repeat_detect)
        stack = []
        stack.append((y, len(input[0]) - 1, west))
        while len(stack) > 0:
            # for i in range(30):
            move()
            # for line in empty_map:
            #    print(line)
            # print("=" * 20)
        # print(stack)
        r = 0
        for line in empty_map_cp:
            r += line.count("#")
        fr = max(r, fr)
    print(fr)
