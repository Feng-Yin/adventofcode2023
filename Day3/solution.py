import re
import os


def any_sym(num, startX, endX, startY, endY):
    # print("check:", startY, startX, endX, lines[startY][startX : endX + 1])
    for idx, char in enumerate(lines[startY][startX : endX + 1]):
        if char != "." and not char.isdigit():
            # print(char, "is a sym")
            if char == "*":
                if f"{startY}:{startX+idx}" not in gearMap:
                    gearMap[f"{startY}:{startX+idx}"] = []
                gearMap[f"{startY}:{startX+idx}"].append(num)
            return True
    # print("check:", endY, startX, endX, lines[endY][startX : endX + 1])
    for idx, char in enumerate(lines[endY][startX : endX + 1]):
        if char != "." and not char.isdigit():
            # print(char, "is a sym")
            if char == "*":
                if f"{endY}:{startX+idx}" not in gearMap:
                    gearMap[f"{endY}:{startX+idx}"] = []
                gearMap[f"{endY}:{startX+idx}"].append(num)
            return True
    # print("check: ", startY + 1, startX, lines[startY + 1][startX])
    if lines[startY + 1][startX] != "." and not lines[startY + 1][startX].isdigit():
        # print(lines[startY + 1][startX], "is a sym")
        if lines[startY + 1][startX] == "*":
            if f"{startY+1}:{startX}" not in gearMap:
                gearMap[f"{startY+1}:{startX}"] = []
            gearMap[f"{startY+1}:{startX}"].append(num)
        return True
    # print("check: ", startY + 1, endX, lines[startY + 1][endX])
    if lines[startY + 1][endX] != "." and not lines[startY + 1][endX].isdigit():
        # print(lines[startY + 1][endX], "is a sym")
        if lines[startY + 1][endX] == "*":
            if f"{startY+1}:{endX}" not in gearMap:
                gearMap[f"{startY+1}:{endX}"] = []
            gearMap[f"{startY+1}:{endX}"].append(num)
        return True
    return False


def get_part_num_from_line(line, startY, endY):
    groups = re.findall("\d+", line)
    part_num = 0
    nums = []
    startX = 0
    endX = 0
    for num in groups:
        startX = max(line[startX:].find(num) + startX - 1, 0)
        endX = min(line[startX:].find(num) + startX + len(num), len(line) - 2)
        # print(num, startX, endX, startY, endY)
        if any_sym(num, startX, endX, startY, endY):
            # print(num, "is a part num")
            part_num += int(num)
        else:
            nums.append(num)
            print(lines[startY][startX : endX + 1])
            print(lines[startY + 1][startX : endX + 1])
            if endY > startY + 1:
                print(lines[endY][startX : endX + 1])
            print("-" * 5)
        if not line[startX].isdigit():
            startX += len(num) + 1
        else:
            startX += len(num)
    if endY - startY == 1 and endY + 1 != len(lines):
        line_num = startY
    else:
        line_num = startY + 1
    if len(nums) > 0:
        print(nums, "is not a part num at line", line_num + 1)
        print("+" * 5)
    return part_num


lines = []
result = 0
gearMap = {}
with open(os.getcwd() + "\input.txt", "r") as file:
    for line in file:
        lines.append(line)
    for y, line in enumerate(lines):
        result += get_part_num_from_line(
            line, max(0, y - 1), min(y + 1, len(lines) - 1)
        )

print(result)
print(gearMap)
gear_ratio = 0
for k, v in gearMap.items():
    if len(v) == 2:
        gear_ratio += int(v[0])*int(v[1])
    if len(v) > 2:
        print("xxxxxxxxxxxxxxxxxxx", k, v)
print(gear_ratio)