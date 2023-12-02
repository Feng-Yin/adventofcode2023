import re

def get_game(str):
    str = str.strip()
    strs = str.split(" ")
    return int(strs[1].strip())

def is_valid_game(str):
    games = str.split(";")
    for game in games:
        game = game.strip()
        cubes = game.split(",")
        for cube in cubes:
            color, num = get_cube(cube.strip())
            if input[color] < num:
                return False
            continue
    return True

def get_cube(str):
    strs = str.split(" ")
    return strs[1].strip(), int(strs[0].strip())

def get_power(str):
    set = {}
    games = str.split(";")
    for game in games:
        game = game.strip()
        cubes = game.split(",")
        for cube in cubes:
            color, num = get_cube(cube.strip())
            if color in set:
                set[color] = max(set[color], num)
            else:
                set[color] = num
            continue
    result = 1
    for v in set.values():
        result *= v
    return result

input = {"red": 12, "green": 13, "blue": 14}
result = 0
power = 0
with open("./input.txt", "r") as file:
    for line in file:
        line = line.strip()
        game = get_game(line.split(":")[0].strip())
        if is_valid_game(line.split(":")[1].strip()):
            result += game
        power += get_power(line.split(":")[1].strip())

print(result)
print(power)