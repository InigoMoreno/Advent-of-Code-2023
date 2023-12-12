#!/bin/env python3
from utils import Day

import numpy as np


class Day05(Day):
    def __init__(self):
        super().__init__("05")

    def transform(self, id, mapping):
        for dest, source, length in mapping:
            if source <= id and id < source + length:
                return dest + id - source
        return id

    def transform_range(self, start, end, mapping):
        for dest, source, length in mapping:
            if source <= start and start < source + length:
                if end < source + length:
                    return [[dest + start - source, dest + end - source]]
                else:
                    return [[dest + start - source, dest + length]
                            ] + self.transform_range(source + length, end, mapping)
        return [[start, end]]

    def parse(self, input):
        seeds, *rest = input.split('\n\n')
        self.seeds = list(map(int, seeds.split()[1:]))
        self.mappings = {}
        self.names = {}
        for block in rest:
            name, *mapping_lines = block.split('\n')
            mapping_lines = [list(map(int, line.split())) for line in mapping_lines]
            name_from, name_to = name.split()[0].split('-to-')
            self.mappings[name_from] = mapping_lines
            self.names[name_from] = name_to

    def part1(self):
        thing = 'seed'
        things = {}
        things[thing] = self.seeds

        while thing != 'location':
            self.log(f"{things[thing]}")
            mapping = self.mappings[thing]
            new_thing = self.names[thing]
            things[new_thing] = [self.transform(id, mapping) for id in things[thing]]
            thing = new_thing

        return np.min(things['location'])

    def part2_slow(self):
        seeds = []
        for i in range(0, len(self.seeds), 2):
            start = self.seeds[i]
            length = self.seeds[i + 1]
            seeds += list(range(start, start + length))
        # return seeds
        thing = 'seed'
        self.things = {}
        self.things[thing] = seeds

        for i in range(len(self.mappings)):
            mapping = self.mappings[thing]
            new_thing = self.names[thing]
            self.things[new_thing] = [self.transform(id, mapping) for id in self.things[thing]]
            thing = new_thing
            if thing == 'location':
                break

        return np.min(self.things['location'])

    def part2(self):
        if self.example:
            self.log(f"{self.part2_slow()=}")
        seed_ranges = []
        for i in range(0, len(self.seeds), 2):
            start = self.seeds[i]
            length = self.seeds[i + 1]
            seed_ranges.append((start, start + length))
        # return seeds
        thing = 'seed'
        self.things = {}
        self.things[thing] = seed_ranges

        for i in range(len(self.mappings)):
            mapping = self.mappings[thing]
            new_thing = self.names[thing]
            self.log(self.things[thing])
            self.things[new_thing] = sum((self.transform_range(start, end, mapping)
                                         for start, end in self.things[thing]), [])
            thing = new_thing
            if thing == 'location':
                break

        return np.min(self.things['location'])


if __name__ == '__main__':
    Day05().main(example=False)
