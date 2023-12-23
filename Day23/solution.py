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
from functools import cmp_to_key


path_id_map = {}


def should_go(all_pathes, id, path, next):
    # if next in path:
    # print(f"path id {path[0]}, map {path_id_map[path[0]]}, next {next}")
    if next in path_id_map[id]:
        return False
    pl = len(path) + 1
    for p in all_pathes:
        if next == p[-1] and len(p) > pl:
            return False
    return True


def print_path(pathes):
    print("*" * 50)
    for p in pathes:
        print(p)
    print("*" * 50)


if __name__ == "__main__":
    input_map = []
    with open("./input.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line == "":
                continue
            input_map.append(list(line))
    # print(input_map)
    start = (0, 0)
    end = (0, 0)
    for ix, ch in enumerate(input_map[0]):
        if ch == ".":
            start = (0, ix)
    for ix, ch in enumerate(input_map[-1]):
        if ch == ".":
            end = (len(input_map) - 1, ix)
    print(start, end)
    pathq = []
    heapq.heappush(pathq, [[start], 0])
    path_id_map[0] = {start: 1}
    final_path = []
    steps = 0
    unique_id = 1
    while len(pathq) > 0:
        steps += 1
        if steps % 1000 == 0:
            print(len(pathq))
        # print_path(pathq)
        currentp_id = heapq.heappop(pathq)
        currentp = currentp_id[0]
        id = currentp_id[1]
        lastp = currentp[-1]
        if lastp == end:
            del path_id_map[id]
            final_path.append(currentp)
            continue
        # part 1
        # if input_map[lastp[0]][lastp[1]] == ".":
        # part 2
        if input_map[lastp[0]][lastp[1]] in ".<>v^":
            # left
            if lastp[1] - 1 >= 0 and input_map[lastp[0]][lastp[1] - 1] != "#":
                if should_go(pathq, id, currentp, (lastp[0], lastp[1] - 1)):
                    p = copy.deepcopy(currentp)
                    p.append((lastp[0], lastp[1] - 1))
                    ############################
                    map_copy = copy.deepcopy(path_id_map[id])
                    map_copy[(lastp[0], lastp[1] - 1)] = 1
                    path_id_map[unique_id] = map_copy
                    ############################
                    heapq.heappush(pathq, [p, unique_id])
                    unique_id += 1
            # right
            if (
                lastp[1] + 1 < len(input_map[0])
                and input_map[lastp[0]][lastp[1] + 1] != "#"
            ):
                if should_go(pathq, id, currentp, (lastp[0], lastp[1] + 1)):
                    p = copy.deepcopy(currentp)
                    p.append((lastp[0], lastp[1] + 1))
                    ############################
                    map_copy = copy.deepcopy(path_id_map[id])
                    map_copy[(lastp[0], lastp[1] + 1)] = 1
                    path_id_map[unique_id] = map_copy
                    ############################
                    heapq.heappush(pathq, [p, unique_id])
                    unique_id += 1
            # up
            if lastp[0] - 1 >= 0 and input_map[lastp[0] - 1][lastp[1]] != "#":
                if should_go(pathq, id, currentp, (lastp[0] - 1, lastp[1])):
                    p = copy.deepcopy(currentp)
                    p.append((lastp[0] - 1, lastp[1]))
                    ############################
                    map_copy = copy.deepcopy(path_id_map[id])
                    map_copy[(lastp[0] - 1, lastp[1])] = 1
                    path_id_map[unique_id] = map_copy
                    ############################
                    heapq.heappush(pathq, [p, unique_id])
                    unique_id += 1
            # down
            if (
                lastp[0] + 1 < len(input_map)
                and input_map[lastp[0] + 1][lastp[1]] != "#"
            ):
                if should_go(pathq, id, currentp, (lastp[0] + 1, lastp[1])):
                    p = copy.deepcopy(currentp)
                    p.append((lastp[0] + 1, lastp[1]))
                    ############################
                    map_copy = copy.deepcopy(path_id_map[id])
                    map_copy[(lastp[0] + 1, lastp[1])] = 1
                    path_id_map[unique_id] = map_copy
                    ############################
                    heapq.heappush(pathq, [p, unique_id])
                    unique_id += 1
            del path_id_map[id]
        # elif input_map[lastp[0]][lastp[1]] == "^":
        #     # up
        #     if lastp[0] - 1 >= 0 and input_map[lastp[0] - 1][lastp[1]] != "#":
        #         if should_go(pathq, currentp, (lastp[0] - 1, lastp[1])):
        #             p = copy.deepcopy(currentp)
        #             p.append((lastp[0] - 1, lastp[1]))
        #             heapq.heappush(pathq, p)
        # elif input_map[lastp[0]][lastp[1]] == "v":
        #     # down
        #     if (
        #         lastp[0] + 1 < len(input_map)
        #         and input_map[lastp[0] + 1][lastp[1]] != "#"
        #     ):
        #         if should_go(pathq, currentp, (lastp[0] + 1, lastp[1])):
        #             p = copy.deepcopy(currentp)
        #             p.append((lastp[0] + 1, lastp[1]))
        #             heapq.heappush(pathq, p)
        # elif input_map[lastp[0]][lastp[1]] == "<":
        #     # left
        #     if lastp[1] - 1 >= 0 and input_map[lastp[0]][lastp[1] - 1] != "#":
        #         if should_go(pathq, currentp, (lastp[0], lastp[1] - 1)):
        #             p = copy.deepcopy(currentp)
        #             p.append((lastp[0], lastp[1] - 1))
        #             heapq.heappush(pathq, p)
        # elif input_map[lastp[0]][lastp[1]] == ">":
        #     # right
        #     if (
        #         lastp[1] + 1 < len(input_map[0])
        #         and input_map[lastp[0]][lastp[1] + 1] != "#"
        #     ):
        #         if should_go(pathq, currentp, (lastp[0], lastp[1] + 1)):
        #             p = copy.deepcopy(currentp)
        #             p.append((lastp[0], lastp[1] + 1))
        #             heapq.heappush(pathq, p)
    # print(final_path)
    lenl = []
    for p in final_path:
        lenl.append(len(p) - 1)
    lenl.sort(reverse=True)
    print(lenl)
