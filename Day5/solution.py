import re
import os

from collections import OrderedDict

from multiprocessing import Pool, cpu_count 
from functools import partial

seeds = []
result = 0
seed_to_soil = {}
soil_to_fertilizer = {}
fertilizer_to_water = {}
water_to_light = {}
light_to_temperature = {}
temperature_to_humidity = {}
humidity_to_location = {}

seed_to_soil_ordered = {}
soil_to_fertilizer_ordered = {}
fertilizer_to_water_ordered = {}
water_to_light_ordered = {}
light_to_temperature_ordered = {}
temperature_to_humidity_ordered = {}
humidity_to_location_ordered = {}

def search_func(seed, maps):
    search_for = int(seed)
    for map in maps:
        for k, v in map.items():
            if search_for >= k and search_for <= k + v[1] - 1:
                search_for = v[0] + search_for - k
                break
    #print("SEARCH", seed, "GOT:", search_for)
    return search_for



if __name__ == '__main__':
    seeds = []
    result = 0
    seed_to_soil = {}
    soil_to_fertilizer = {}
    fertilizer_to_water = {}
    water_to_light = {}
    light_to_temperature = {}
    temperature_to_humidity = {}
    humidity_to_location = {}
    with open("./input.txt", "r") as file:
        current_map = {}
        for line in file:
            line = line.strip()
            print(line)
            if line == "":
                continue
            elif line.find("seeds:") != -1:
                print("seeds line")
                seeds = re.findall(r"\d+", line[len("seeds:"):])
            elif line.find("map:") != -1:
                if line.find("seed-to-soil") != -1:
                    current_map = seed_to_soil
                elif line.find("soil-to-fertilizer") != -1:
                    current_map = soil_to_fertilizer
                elif line.find("fertilizer-to-water") != -1:
                    current_map = fertilizer_to_water
                elif line.find("water-to-light") != -1:
                    current_map = water_to_light
                elif line.find("light-to-temperature") != -1:
                    current_map = light_to_temperature 
                elif line.find("temperature-to-humidity") != -1:
                    current_map = temperature_to_humidity 
                elif line.find("humidity-to-location") != -1:
                    current_map = humidity_to_location
            else:
                numbers = re.findall(r"\d+", line)
                current_map[int(numbers[1])] = (int(numbers[0]), int(numbers[2]))

    print("seeds", seeds)
    print("seed_to_soil", seed_to_soil)
    print("soil_to_fertilizer", soil_to_fertilizer)
    print("fertilizer_to_water", fertilizer_to_water)
    print("water_to_light", water_to_light)
    print("light_to_temperature", light_to_temperature)
    print("temperature_to_humidity", temperature_to_humidity)
    print("humidity_to_location", humidity_to_location)

    seed_to_soil_ordered = OrderedDict(sorted(seed_to_soil.items(), key=lambda t: int(t[0])))
    soil_to_fertilizer_ordered = OrderedDict(sorted(soil_to_fertilizer.items(), key=lambda t: int(t[0])))
    fertilizer_to_water_ordered = OrderedDict(sorted(fertilizer_to_water.items(), key=lambda t: int(t[0])))
    water_to_light_ordered = OrderedDict(sorted(water_to_light.items(), key=lambda t: int(t[0])))
    light_to_temperature_ordered = OrderedDict(sorted(light_to_temperature.items(), key=lambda t: int(t[0])))
    temperature_to_humidity_ordered = OrderedDict(sorted(temperature_to_humidity.items(), key=lambda t: int(t[0])))
    humidity_to_location_ordered = OrderedDict(sorted(humidity_to_location.items(), key=lambda t: int(t[0])))

    print("seeds", seeds)
    print("seed_to_soil_ordered", seed_to_soil_ordered)
    print("soil_to_fertilizer_ordered", soil_to_fertilizer_ordered)
    print("fertilizer_to_water_ordered", fertilizer_to_water_ordered)
    print("water_to_light_ordered", water_to_light_ordered)
    print("light_to_temperature_ordered", light_to_temperature_ordered)
    print("temperature_to_humidity_ordered", temperature_to_humidity_ordered)
    print("humidity_to_location_ordered", humidity_to_location_ordered)

    locations = []
    for seed in seeds:
        print("Seed", seed)
        search_for = int(seed)
        for map in [seed_to_soil_ordered, soil_to_fertilizer_ordered, fertilizer_to_water_ordered, water_to_light_ordered, light_to_temperature_ordered, temperature_to_humidity_ordered, humidity_to_location_ordered]:
            for k, v in map.items():
                if search_for >= k and search_for <= k + v[1] - 1:
                    search_for = v[0] + search_for - k
                    break
            print(search_for)
        locations.append(search_for)

    print(locations)
    locations.sort()
    print(locations)



    locations = []
    for seed_start, len in zip(*[iter(seeds)]*2):
        print("Seeds", seed_start, len)
        with Pool(processes=cpu_count()) as pool:
            all_maps = [seed_to_soil_ordered, soil_to_fertilizer_ordered, fertilizer_to_water_ordered, water_to_light_ordered, light_to_temperature_ordered, temperature_to_humidity_ordered, humidity_to_location_ordered]
            sublocations = pool.map(partial(search_func, maps=all_maps), range(int(seed_start), int(seed_start) + int(len)))
            sublocations.sort()
            locations.append(sublocations[0])
    #    for seed in range(int(seed_start), int(seed_start) + int(len)):
    #        #print("Seed", seed)
    #        search_for = int(seed)
    #        for map in [seed_to_soil_ordered, soil_to_fertilizer_ordered, fertilizer_to_water_ordered, water_to_light_ordered, light_to_temperature_ordered, temperature_to_humidity_ordered, humidity_to_location_ordered]:
    #            for k, v in map.items():
    #                if search_for >= k and search_for <= k + v[1] - 1:
    #                    search_for = v[0] + search_for - k
    #                    break
    #            #print(search_for)
    #        locations.append(search_for)

    #print(locations)
    locations.sort()
    print(locations[0])
