#!/bin/env python3
from utils import Day

import numpy as np
import math


class Day08(Day):
    def __init__(self):
        super().__init__("08")

    def parse(self, input):
        self.steps, block2 = input.split('\n\n')
        self.map = {line[:3]: (line[7:10], line[12:15]) for line in block2.splitlines()}

    def part1(self):
        pos = 'AAA'
        i = 0
        while pos != 'ZZZ':
            step = self.steps[i % len(self.steps)]
            pos = self.map[pos][step == 'R']
            i += 1

        return i

    def compute_loop(self, pos):
        i = 0
        visited_set = set()
        visited_list = list()
        while True:
            step = self.steps[i % len(self.steps)]
            key = (pos, i % len(self.steps))
            if key in visited_set:
                break
            visited_list.append(key)
            visited_set.add(key)
            pos = self.map[pos][step == 'R']
            i = (i + 1)
        loop_index = visited_list.index(key)
        loop_length = len(visited_list) - loop_index
        return loop_length

    def part2(self):
        positions = [key for key in self.map.keys() if key[-1] == 'A']
        return math.lcm(*[self.compute_loop(pos) for pos in positions])


if __name__ == '__main__':
    Day08().main(example=True)
