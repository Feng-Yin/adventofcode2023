import re
import os
from functools import cmp_to_key

from collections import OrderedDict

from multiprocessing import Pool, cpu_count
from functools import partial

up = 0
right = 1
down = 2
left = 3


def get_directions(maps, x, y, entry):
    directions = []
    # check up first
    if maps[y][x] == "|":
        if entry == up:
            directions.append(up)
        elif entry == down:
            directions.append(down)
    elif maps[y][x] == "-":
        if entry == left:
            directions.append(left)
        elif entry == right:
            directions.append(right)
    elif maps[y][x] == "L":
        if entry == down:
            directions.append(right)
        elif entry == left:
            directions.append(up)
    elif maps[y][x] == "F":
        if entry == up:
            directions.append(right)
        elif entry == left:
            directions.append(down)
    elif maps[y][x] == "J":
        if entry == right:
            directions.append(up)
        elif entry == down:
            directions.append(left)
    elif maps[y][x] == "7":
        if entry == right:
            directions.append(down)
        elif entry == up:
            directions.append(left)
    return directions

def do_travel(maps, x, y, entry):
    directions = [entry]
    gox = x
    goy = y
    steps = 0
    while True:
        if maps[goy][gox] == "-" :
            count_maps[goy][gox] = "X"
        else:
            count_maps[goy][gox] = "X"
        #print("(", gox, ", ", goy, ")")
        #print(maps[goy][gox])
        if maps[goy][gox] == "S":
            print("Find S")
            return steps
        directions = get_directions(maps, gox, goy, directions[0])
        if len(directions) == 0:
            return 0
        if len(directions) > 1:
            print("WRONG!!!!!!!!!")
            return 0
        if directions[0] == up:
            if goy == 0:
                return 0
            else:
                #print("go up")
                goy -= 1
        if directions[0] == left:
            if gox == 0:
                return 0
            else:
                #print("go left")
                gox -= 1
        if directions[0] == right:
            if gox == len(maps[0]) - 1:
                return 0
            else:
                #print("go right")
                gox += 1
        if directions[0] == down:
            if goy == len(maps) -1:
                return 0
            else:
                #print("go down")
                goy += 1
        steps += 1

def travel(maps, startx, starty):
    maxL = 0
    count_maps[starty][startx] = "X"
    # check up first
    if maps[starty-1][startx] == "|" or maps[starty-1][startx] == "7" or maps[starty-1][startx] == "F":
        print("try up")
        maxL = max(maxL, do_travel(maps, startx, starty-1, up))
        print("up", maxL + 1)
        if maxL > 0:
            return maxL + 1
    # check right
    if maps[starty][startx+1] == "-" or maps[starty][startx+1] == "J" or maps[starty][startx+1] == "7":
        print("try right")
        maxL = max(maxL, do_travel(maps, startx+1, starty, right))
        print("right", maxL + 1)
        if maxL > 0:
            return maxL + 1
    # check down
    if maps[starty+1][startx] == "|" or maps[starty+1][startx] == "L" or maps[starty+1][startx] == "J":
        print("try down")
        maxL = max(maxL, do_travel(maps, startx, starty+1, down))
        print("down", maxL + 1)
        if maxL > 0:
            return maxL + 1
    # check left
    if maps[starty][startx-1] == "-" or maps[starty][startx-1] == "F" or maps[starty][startx-1] == "L":
        print("try left")
        maxL = max(maxL, do_travel(maps, startx-1, starty, left))
        print("left", maxL + 1)
        if maxL > 0:
            return maxL + 1
    return maxL + 1

def connected(char1, char2):
    #print(char1, char2)
    if char1 == "-" or char1 == "L" or char1 == "F":
        if char2 == "-" or char2 == "J" or char2 == "7":
            return True
    return False

def is_one_wall(char1, char2):
    #print(char1, char2)
    if char1 == "F" and char2 == "J":
        return True
    if char1 == "L" and char2 == "7":
        return True
    return False

def get_cross_count(ix, iy):
    count = 0
    ixt = ix
    LastCmpChar = maps[iy][ixt]
    while ixt < len(maps[0]) - 1:
        if count_maps[iy][ixt+1] == "X":
            if maps[iy][ixt+1] == "-" or (count_maps[iy][ixt] == "X" and is_one_wall(LastCmpChar, maps[iy][ixt+1])):
                if maps[iy][ixt+1] == "-":
                    LastCmpChar = LastCmpChar
                else:
                    LastCmpChar = maps[iy][ixt+1]
                ixt += 1
                continue
            else:
                #print("+1")
                count += 1
        LastCmpChar = maps[iy][ixt+1]
        ixt += 1
    return count

if __name__ == "__main__":
    maps = []
    startx = 0
    starty = 0
    count_maps = []
    with open("./input.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line == "":
                continue
            row = []
            for idx, char in enumerate(line):
                row.append(char)
                if char == "S":
                    startx = idx
                    starty = len(maps)
            count_maps.append(row.copy())
            maps.append(row)
    #print(maps)
    lens = travel(maps, startx, starty)
    print((lens)/2)
    
    r = 0
    maps_range = []
    for iy, row in enumerate(count_maps):
        #print(row)
        #print(maps[iy])
        for ix, char in enumerate(row):
            if char != "X":
                if ix == 0 or ix == len(row) - 1 or iy == 0 or iy == len(count_maps) - 1:
                    continue
                cross_count = get_cross_count(ix, iy)
                #print(ix, iy, char, cross_count)
                if cross_count % 2 == 1:
                    r += 1
    print(r)