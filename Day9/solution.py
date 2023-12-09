import re
import os
from functools import cmp_to_key

from collections import OrderedDict

from multiprocessing import Pool, cpu_count
from functools import partial


def find_history(line):
    print("input:", line)
    group = line.strip().split(" ")
    # print("group", group)
    tmp_list = []
    for str in group:
        tmp_list.append(int(str))
    historys = []
    historys.append(tmp_list)
    # print(historys)
    idx = 0
    while True:
        tmp_list = []
        for i, v in enumerate(historys[idx]):
            if i + 1 < len(historys[idx]):
                tmp_list.append(historys[idx][i + 1] - historys[idx][i])
        historys.append(tmp_list)
        if tmp_list.count(0) == len(tmp_list):
            break
        idx += 1
    hr = 0
    for history in historys:
        hr += history[-1]
    """ historys[-1].append(0)
    for idx, history in enumerate(historys):
        if len(historys) - 2 - idx >= 0:
            print(
                "append",
                historys[len(historys) - 2 - idx][-1]
                + historys[len(historys) - 1 - idx][-1],
            )
            historys[len(historys) - 2 - idx].append(
                historys[len(historys) - 2 - idx][-1]
                + historys[len(historys) - 1 - idx][-1]
            ) """
    print(historys)
    print(hr)
    print("=" * 20)
    return hr


def find_history2(line):
    print("input:", line)
    group = line.strip().split(" ")
    # print("group", group)
    tmp_list = []
    for str in group:
        tmp_list.append(int(str))
    historys = []
    historys.append(tmp_list)
    # print(historys)
    idx = 0
    while True:
        tmp_list = []
        for i, v in enumerate(historys[idx]):
            if i + 1 < len(historys[idx]):
                tmp_list.append(historys[idx][i + 1] - historys[idx][i])
        historys.append(tmp_list)
        if tmp_list.count(0) == len(tmp_list):
            break
        idx += 1
    hr = 0
    factor = 1
    for history in historys:
        hr += history[0] * factor
        factor = factor * (-1)
    return hr


if __name__ == "__main__":
    lines = []
    sub = []
    with open("./input.txt", "r") as file:
        for line in file:
            lines.append(line)
        for line in lines:
            sub.append(find_history2(line))
    print(sum(sub))
