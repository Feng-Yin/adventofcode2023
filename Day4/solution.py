import re
import os

def calculate_score(winning_str, my_str):
    winnings_str_array = re.findall(r"\d+", winning_str)
    my_str_array = re.findall(r"\d+", my_str)
    power = 0
    for my_num in my_str_array:
        if my_num in winnings_str_array:
            #print(my_num, "in", winnings_str_array)
            power += 1
    #print("power is", power)
    if power == 0:
        return 0, 0
    else:
        return pow(2, power - 1), power


def get_score(str):
    str = str.strip()
    group1 = str.split(":")
    group2 = group1[1].strip().split("|")
    return calculate_score(group2[0].strip(), group2[1].strip())


lines = []
result = 0
result_array = []
multiply_array = []
with open(os.getcwd() + "\input.txt", "r") as file:
    for line in file:
        lines.append(line)
    for idx, line in enumerate(lines):
        if idx >= len(multiply_array):
            multiply_array.append(1)
        score, power = get_score(line)
        result += score
        result_array.append(score)
        for j in range(multiply_array[idx]):
            for i in range(power):
                if idx + i + 1 >= len(lines):
                    break
                if idx + i + 1 >= len(multiply_array):
                    multiply_array.append(2)
                else:
                    multiply_array[idx + i + 1] += 1

print(result)
print(sum(multiply_array))
