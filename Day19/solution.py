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


class rule:
    def __init__(self, input):
        name, rests = input.split("{")
        self.name = name
        conditions_str = rests[:-1]
        condition_groups = conditions_str.split(",")
        self.conditions = []
        for condition in condition_groups:
            if ":" not in condition:
                self.conditions.append([None, None, None, condition])
            else:
                comp, output = condition.split(":")
                self.conditions.append([comp[0], comp[1], int(comp[2:]), output])

    # def __repr__(self):
    #    return self.name + " " + str(self.conditions)

    def get_name(self):
        return self.name

    def match(self, input):
        stripped = input[1:-1]
        groups = stripped.split(",")
        inputs = {}
        for group in groups:
            k, v = group.split("=")
            inputs[k] = int(v)
        for condition in self.conditions:
            if condition[0] is None:
                return condition[3]
            else:
                input_value = inputs[condition[0]]
                if condition[1] == ">" and input_value > condition[2]:
                    return condition[3]
                if condition[1] == "<" and input_value < condition[2]:
                    return condition[3]
        return None

    def get_possible_outputs(self):
        output = []
        for condition in self.conditions:
            output.append(condition[3])
        return output


def get_accepted_value(accepted):
    r = 0
    for input in accepted:
        stripped = input[1:-1]
        groups = stripped.split(",")
        for group in groups:
            k, v = group.split("=")
            r += int(v)
    return r


def build_possible_paths(name, rules):
    r = []
    heap = []
    heapq.heappush(heap, name)
    while len(heap) > 0:
        path = heapq.heappop(heap)
        head = path
        if "->" in path:
            head = path.split("->")[0]
        for k, rule in rules.items():
            if head in rule.get_possible_outputs():
                if k == "in":
                    r.append("in->" + path)
                else:
                    #print("pushing", k + "->" + path)
                    #if k == "dp":
                    #    print("pushing", k + "->" + path)
                    #    exit()
                    heapq.heappush(heap, k + "->" + path)
    return set(r)


if __name__ == "__main__":
    rules_str = []
    inputs_str = []
    tlist = rules_str
    with open("./input.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line == "":
                tlist = inputs_str
                continue
            tlist.append(line)
    # print(rules_str)
    # print(inputs_str)
    rules = {}
    for rule_str in rules_str:
        r = rule(rule_str)
        rules[r.get_name()] = r
    accepted = []
    for input_str in inputs_str:
        #print(input_str)
        output = "in"
        while output != "A" and output != "R":
            output = rules[output].match(input_str)
        if output == "A":
            #print("Accepted", input_str)
            accepted.append(input_str)
        # elif output == "R":
        #     print("Rejected", input_str)
        # else:
        #     print("Error", input_str)
    #print(get_accepted_value(accepted))
    all_possible_outputs = build_possible_paths("A", rules)
    #print(all_possible_outputs)
    r = 0
    for path in all_possible_outputs:
        tmp = {
            "x": [1, 4000],
            "m": [1, 4000],
            "a": [1, 4000],
            "s": [1, 4000],
        }
        groups = path.split("->")
        # print(path, groups)
        for ix, name in enumerate(groups):
            if name == "A":
                break
            # print(ix, name)
            rule = rules[name]
            next = groups[ix + 1]
            #print(f"    path: {path}, next: {next}, tmp: {tmp}")
            new_sets = []
            if rule.get_possible_outputs().count(next) > 1:
                if next != "A":
                    print("error", path)
                    exit()
                # # if last condition is default next, we can ignore all other next conditions
                # if rule.conditions[-1][3] == next and rule.conditions[-1][0] is None:
                #     new_set = []
                #     for condition in rule.conditions:
                #         if condition[3] != next:
                #             new_set.append(condition)
                #     new_set.append(rule.conditions[-1])
                #     new_sets.append(new_set)
                # else:
                count = rule.get_possible_outputs().count(next)
                for i in range(1, count + 1):
                    new_set = []
                    tmp_count = 0
                    for condition in rule.conditions:
                        if condition[3] != next:
                            new_set.append(condition)
                        else:
                            tmp_count += 1
                            if i == tmp_count:
                                new_set.append(condition)
                                break
                    new_sets.append(new_set)
            else:
                new_sets.append(rule.conditions)
            
            tmp_set = []
            for new_set in new_sets:
                tmp_copy = copy.deepcopy(tmp)
                for condition in new_set:
                    # print("handdling", condition)
                    if condition[0] is None:
                        break
                    elif condition[3] == next:
                        # print("matched next")
                        if condition[1] == ">":
                            tmp_copy[condition[0]][0] = max(
                                tmp_copy[condition[0]][0], condition[2] + 1
                            )
                        else:
                            tmp_copy[condition[0]][1] = min(
                                tmp_copy[condition[0]][1], condition[2] - 1
                            )
                        break
                    else:
                        # print("not matched next")
                        if condition[1] == ">":
                            tmp_copy[condition[0]][1] = min(tmp_copy[condition[0]][1], condition[2])
                        else:
                            tmp_copy[condition[0]][0] = max(tmp_copy[condition[0]][0], condition[2])
                tmp_set.append(tmp_copy)

            max_i = -1
            max_v = -1
            #if len(tmp_set) > 1:
                #print(f"    tmp_set: {tmp_set}")
            for i, tmp_copy in enumerate(tmp_set):
                tv = 1
                for k, v in tmp_copy.items():
                    diff = v[1] - v[0] + 1
                    if diff <= 0:
                        break
                    tv *= diff
                if tv > max_v and i >= 0:
                    max_v = tv
                    max_i = i
            tmp = tmp_set[max_i]
        print(path, tmp)
        mr = 1
        for k, v in tmp.items():
            diff = v[1] - v[0] + 1
            if diff <= 0:
                print("error", path)
                exit()
            mr *= diff
        if mr >= 0:
            r += mr
        else:
            print("error", path)
    print(r)
