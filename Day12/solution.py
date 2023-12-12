import re
import os
from functools import cmp_to_key

from collections import OrderedDict

from multiprocessing import Pool, cpu_count
from functools import partial
import numpy as np


def find_nth_occurrence(string, sub_string, n):
    start_index = string.find(sub_string)
    while start_index >= 0 and n > 1:
        start_index = string.find(sub_string, start_index + 1)
        n -= 1
    return start_index


def get_conbinations(str, pos):
    num_of_q = str.count("?")
    possibilities = 0
    for i in range(0, 2**num_of_q):
        str_cp = str
        for qi in range(num_of_q):
            if i % 2 == 1:
                index = find_nth_occurrence(str, "?", qi + 1)
                # print(f"the {qi+1}th ? is at {index}")
                str_cp = str_cp[:index] + "#" + str_cp[index + 1 :]
            i = int(i / 2)
            if i == 0:
                break
        str_cp = str_cp.replace("?", ".")
        # print(f"checking {i}", str_cp)
        # print("=" * 30)
        if pos == [i.count("#") for i in list(filter(None, str_cp.split(r".")))]:
            possibilities += 1
    # print(str, "has", possibilities, "possibilities")
    return possibilities


def get_conbinationsT(str, pos):
    num_of_q = str.count("?")
    possibilities = 0
    for i in range(0, 2**num_of_q):
        str_cp = str
        for qi in range(num_of_q):
            if qi == num_of_q - 1 and str[0] == "#":
                str_cp = str_cp[:-1] + "."
            elif i % 2 == 1:
                index = find_nth_occurrence(str, "?", qi + 1)
                # print(f"the {qi+1}th ? is at {index}")
                str_cp = str_cp[:index] + "#" + str_cp[index + 1 :]
            i = int(i / 2)
            if i == 0:
                break
        str_cp = str_cp.replace("?", ".")
        # print(f"checking {i}", str_cp)
        # print("=" * 30)
        if pos == [i.count("#") for i in list(filter(None, str_cp.split(r".")))]:
            possibilities += 1
    # print(str, "has", possibilities, "possibilities")
    return possibilities


def get_conbinationsH(str, pos):
    num_of_q = str.count("?")
    possibilities = 0
    for i in range(0, 2**num_of_q):
        str_cp = str
        for qi in range(num_of_q):
            if qi == 0 and str[-1] == "#":
                str_cp = "." + str_cp[1:]
            elif i % 2 == 1:
                index = find_nth_occurrence(str, "?", qi + 1)
                # print(f"the {qi+1}th ? is at {index}")
                str_cp = str_cp[:index] + "#" + str_cp[index + 1 :]
            i = int(i / 2)
            if i == 0:
                break
        str_cp = str_cp.replace("?", ".")
        # print(f"checking {i}", str_cp)
        # print("=" * 30)
        if pos == [i.count("#") for i in list(filter(None, str_cp.split(r".")))]:
            possibilities += 1
    # print(str, "has", possibilities, "possibilities")
    return possibilities


def get_conbinations2(idx, maps, poss):
    str = "?".join((maps[idx],) * 5)
    pos = poss[idx] * 5
    print(f"checking {idx}", str, pos)
    num_of_q = str.count("?")
    possibilities = 0
    for i in range(0, 2**num_of_q):
        str_cp = str
        for qi in range(num_of_q):
            if i % 2 == 1:
                index = find_nth_occurrence(str, "?", qi + 1)
                # print(f"the {qi+1}th ? is at {index}")
                str_cp = str_cp[:index] + "#" + str_cp[index + 1 :]
            i = int(i / 2)
            if i == 0:
                break
        str_cp = str_cp.replace("?", ".")
        # print(f"checking {i}", str_cp)
        # print("=" * 30)
        if pos == [i.count("#") for i in list(filter(None, str_cp.split(r".")))]:
            possibilities += 1
    print(str, "has", possibilities, "possibilities")
    return possibilities


def sub_posi(i, stri, pos):
    str_cp = stri
    num_of_q = stri.count("?")
    for qi in range(num_of_q):
        if i % 2 == 1:
            index = find_nth_occurrence(stri, "?", qi + 1)
            # print(f"the {qi+1}th ? is at {index}")
            str_cp = str_cp[:index] + "#" + str_cp[index + 1 :]
        i = int(i / 2)
        if i == 0:
            break
    str_cp = str_cp.replace("?", ".")
    # print(f"checking", str_cp)
    # print("=" * 30)
    if pos == [t.count("#") for t in list(filter(None, str_cp.split(r".")))]:
        return 1
    return 0


def simplify(str, pos):
    print("simplify", str, pos)
    index1 = str.find("?")
    index2 = str.rfind("?")
    part1 = str[:index1]
    part2 = str[index2 + 1 :]
    scount = part1.count("#")
    ecount = part2.count("#")
    while scount >= pos[0]:
        scount -= pos[0]
        pos = pos[1:]
    pos[0] -= scount
    while ecount >= pos[-1]:
        ecount -= pos[-1]
        pos = pos[:-1]
        print(pos)
    pos[-1] -= ecount
    e = min(index2 + 1, len(str))
    print("simplify to", str[index1 : index2 + 1], pos)
    return str[index1 : index2 + 1], pos


if __name__ == "__main__":
    maps = []
    nums = []
    with open("./input.txt", "r") as file:
        for ix, line in enumerate(file):
            line = line.strip()
            if line == "":
                continue
            parts = line.split(" ")
            maps.append(parts[0].strip())
            tmp = []
            for ch in parts[1].strip().split(","):
                tmp.append(int(ch))
            nums.append(tmp)
    print(maps)
    print(nums)
    r = 0
    # for str, pos in zip(maps, nums):
    #     r1 = get_conbinations(str, pos)
    #     print("org", r1)
    #     r2 = 1
    #     # if str[-1] != "#":
    #     r2 = get_conbinations(str + "?" + str, pos * 2)
    #     print("2x", r2)
    #     # if str[0] != "#":
    #     # p = get_conbinationsT(str + "?", pos)
    #     # r2 = max(r2, p)
    #     # print("postfix", p)
    #     ri = r2**4 / r1**3
    #     r += ri
    #     print(f"new {str} has {ri} possibilities")
    # print(r)

    # pathes = []
    # with Pool(processes=cpu_count()) as pool:
    #     pathes = pool.map(
    #         partial(get_conbinations2, maps=maps, poss=nums), range(len(maps))
    #     )
    # print(sum(pathes))

    p1 = []
    for str2, pos2 in zip(maps, nums):
        num_of_q = str2.count("?")
        print(f"checking {str2} {pos2} with {num_of_q} ?")
        pathes = []
        with Pool(processes=cpu_count()) as pool:
            pathes = pool.map(
                partial(sub_posi, stri=str2, pos=pos2), range(2**num_of_q)
            )
        possibilities = sum(pathes)
        print(str2, "has", possibilities, "possibilities")
        p1.append(possibilities)

    p2 = []
    for str2, pos2 in zip(maps, nums):
        new_str = str2 + "?" + str2
        new_pos = pos2 * 2
        num_of_q = new_str.count("?")
        print(f"checking {new_str} {new_pos} with {num_of_q} ?")
        pathes = []
        with Pool(processes=cpu_count()) as pool:
            pathes = pool.map(
                partial(sub_posi, stri=new_str, pos=new_pos), range(2**num_of_q)
            )
        possibilities = sum(pathes)
        print(new_str, "has", possibilities, "possibilities")
        p2.append(possibilities)

    r = 0
    for r1, r2 in zip(p1, p2):
        r += r2**4 / r1**3
    print(r)
