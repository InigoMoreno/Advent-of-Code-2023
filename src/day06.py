#!/bin/env python3
from turtle import distance
from utils import Day

import math
import numpy as np


class Day06(Day):
    def __init__(self):
        super().__init__("06")

    def parse(self, input):
        time_line, distance_line = input.split('\n')
        self.times = [int(element) for element in time_line.split(' ')[1:] if element]
        self.distances = [int(element) for element in distance_line.split(' ')[1:] if element]

    def compute_ways(self, time, distance):
        self.log(f'{time=} {distance=}')
        tp1 = (-time + math.sqrt(time**2 - 4 * distance)) / -2
        tp2 = (-time - math.sqrt(time**2 - 4 * distance)) / -2
        self.log(tp1, tp2)
        tp1 = math.floor(tp1 + 1)
        tp2 = math.ceil(tp2 - 1)
        self.log(tp1, tp2)
        ways = tp2 - tp1 + 1
        return ways

    def part1(self):
        return np.prod([self.compute_ways(time, distance) for time, distance in zip(self.times, self.distances)])

    def part2(self):
        return self.compute_ways(
            time=int(''.join(map(str, self.times))),
            distance=int(''.join(map(str, self.distances)))
        )


if __name__ == '__main__':
    Day06().main(example=False)
