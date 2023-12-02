import re

def str2int(str):
    if str == "one":
        return 1
    elif str == "two":
        return 2
    elif str == "three":
        return 3
    elif str == "four":
        return 4
    elif str == "five":
        return 5
    elif str == "six":
        return 6
    elif str == "seven":
        return 7
    elif str == "eight":
        return 8
    elif str == "nine":
        return 9
    else:
        return int(str)

def FindDigitPosAndVal(str):
    m = re.findall(r"\d", str)
    if len(m) == 0:
        return (len(str), 0), (-1, 0)
    return (str.find(m[0]), str2int(m[0])), (str.rfind(m[-1]), str2int(m[-1]))

def FindTextPosAndVal(str, d1i, d1v, dni, dnv):
    #(dt1i, dt1v), (dtni, dtnv) = (-1, 0),  (len(str), 0)
    for dt in ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]:
        m = re.findall(dt, str)
        if len(m) == 0:
            continue
        if str.find(m[0]) < d1i:
            d1i, d1v = str.find(m[0]), str2int(m[0])
        if str.rfind(m[-1]) > dni:
            dni, dnv = str.rfind(m[-1]), str2int(m[-1])
    return (d1i, d1v), (dni, dnv)

num = 0
with open("./input.txt", "r") as file:
    for line in file:
    #line = "2911threeninesdvxvheightwobm"
        (d1i, d1v), (dni, dnv) = FindDigitPosAndVal(line)
        (d1i, d1v), (dni, dnv) = FindTextPosAndVal(line, d1i, d1v, dni, dnv)
        #print((d1i, d1v), (dni, dnv))
        #print((dt1i, dt1v), (dtni, dtnv))
        num += d1v * 10
        num += dnv

print(num)
