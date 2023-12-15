import re
import os
from functools import cmp_to_key

from collections import OrderedDict

from multiprocessing import Pool, cpu_count
from functools import partial

import numpy as np
import copy
from progressbar import progressbar

def build_search_table():
    return None

def get_current_value_char(char, current_value):
    char_int =ord(char)
    return (current_value + char_int) * 17 % 256

def get_current_value_str(str):
    current_value = 0
    for char in str:
        current_value = get_current_value_char(char, current_value)
    return current_value

if __name__ == "__main__":
    groups = []
    with open("./input.txt", "r") as file:
        for ix, line in enumerate(file):
            line = line.strip()
            if line == "":
                continue
            groups = line.split(",")
    print(groups)
    r = 0
    for str in groups:
        r += get_current_value_str(str)
    print(r)
    #################################################
    # Part 2
    #################################################
    boxes = {}
    boxix = -1
    for str in groups:
        if str.find("=") >= 0:
            boxix = get_current_value_str(str[:str.find("=")])
            num = int(str[str.find("=")+1:])
            if boxix not in boxes:
                tmp = []
                tmp.append((str[:str.find("=")], num))
                boxes[boxix] = tmp
            else:
                tmp = boxes[boxix]
                found = None
                for ix, item in enumerate(tmp):
                    if item[0] == str[:str.find("=")]:
                        found = item
                        break
                if found is not None:
                    tmp[ix] = (str[:str.find("=")], num)
                else:
                    tmp.append((str[:str.find("=")], num))
                boxes[boxix] = tmp
        elif str.find("-") >= 0:
            boxix = get_current_value_str(str[:str.find("-")])
            found = None
            if boxix in boxes:
                tmp = boxes[boxix]
                for item in tmp:
                    if item[0] == str[:str.find("-")]:
                        found = item
                        break
                if found is not None:
                    tmp.remove(found)
                boxes[boxix] = tmp
    #print(boxes)
    r = 0
    for k, v in boxes.items():
        if len(v) == 0:
            continue
        else:
            for ix, item in enumerate(v):
                r += (k+1) * (ix+1) * item[1]
    print(r)
                

