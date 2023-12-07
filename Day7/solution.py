import re
import os
from functools import cmp_to_key

from collections import OrderedDict

from multiprocessing import Pool, cpu_count
from functools import partial


def get_distinct(str):
    return len(set(str))


def get_max_repeat(str):
    rep = 0
    for ch in set(str):
        rep = max(rep, str.count(ch))
    return rep


def get_level(str):
    # 5 of a kind
    if get_distinct(str) == 1:
        return 7
    if get_distinct(str) == 2:
        # 4 + 1
        if get_max_repeat(str) == 4:
            return 6
        else:
            # 3 + 2
            return 5
    if get_distinct(str) == 3:
        if get_max_repeat(str) == 3:
            # 3 + 1 + 1
            return 4
        else:
            # 2 + 2 + 1
            return 3
    if get_distinct(str) == 4:
        # 2 + 1 + 1 + 1
        return 2
    return 0


AAAAA = 7
AAAAB = 6
AAABB = 5
AAABC = 4
AABBC = 3
AABCD = 2
ABCDE = 0


def get_level2(str):
    # 5 of a kind
    if get_distinct(str) == 1:
        return AAAAA
    if get_distinct(str) == 2:
        # 4 + 1
        if get_max_repeat(str) == 4:
            # up level to 5 of a kind
            if str.count("J") == 1 or str.count("J") == 4:
                return AAAAA
            else:
                # 4 + 1
                return AAAAB
        else:
            # 3 + 2
            if str.count("J") == 2 or str.count("J") == 3:
                # 5
                return AAAAA
            else:
                return AAABB
    if get_distinct(str) == 3:
        if get_max_repeat(str) == 3:
            # 3 + 1 + 1
            if str.count("J") == 1 or str.count("J") == 3:
                # 4 + 1
                return AAAAB
            else:
                # 3 + 1 + 1
                return AAABC
        else:
            # 2 + 2 + 1
            if str.count("J") == 2:
                # 4 + 1
                return AAAAB
            elif str.count("J") == 1:
                # 3 + 2
                return AAABB
            else:
                # 2 + 2 + 1
                return AABBC
    if get_distinct(str) == 4:
        # 2 + 1 + 1 + 1
        if str.count("J") == 1 or str.count("J") == 2:
            # 3 + 1 + 1
            return AAABC
        else:
            # 2 + 1 + 1 + 1
            return AABCD
    if str.count("J") == 1:
        # 2 + 1 + 1 + 1
        return AABCD
    return ABCDE


def get_char_weight(ch):
    if ch == "A":
        return 14
    if ch == "K":
        return 13
    if ch == "Q":
        return 12
    if ch == "J":
        return 11
    if ch == "T":
        return 10
    return int(ch)


def get_char_weight2(ch):
    if ch == "A":
        return 14
    if ch == "K":
        return 13
    if ch == "Q":
        return 12
    if ch == "J":
        return 1
    if ch == "T":
        return 10
    return int(ch)


def compare(stra, strb):
    # print("compare: ", stra, strb)
    a = get_level(stra)
    b = get_level(strb)
    # print("compare: ", a, b)
    if a != b:
        return 1 if a > b else -1
    for ca, cb in zip(stra, strb):
        if ca != cb:
            return 1 if get_char_weight(ca) > get_char_weight(cb) else -1


def compare2(stra, strb):
    # print("compare: ", stra, strb)
    a = get_level2(stra)
    b = get_level2(strb)
    # print("compare: ", a, b)
    if a != b:
        return 1 if a > b else -1
    for ca, cb in zip(stra, strb):
        if ca != cb:
            return 1 if get_char_weight2(ca) > get_char_weight2(cb) else -1


if __name__ == "__main__":
    hands = {}
    with open("./input.txt", "r") as file:
        for line in file:
            hands[line.strip().split(" ")[0].strip()] = int(
                line.strip().split(" ")[1].strip()
            )
    keys = sorted(hands.keys(), key=cmp_to_key(compare))
    result = 0
    for idx, value in enumerate(keys):
        result += hands[value] * (idx + 1)
    print(keys)
    print(result)

    keys = sorted(hands.keys(), key=cmp_to_key(compare2))
    result = 0
    for idx, value in enumerate(keys):
        result += hands[value] * (idx + 1)
    print(keys)
    print(result)
