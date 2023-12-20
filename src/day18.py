#!/bin/env python3
from utils import Day

import numpy as np
from queue import Queue


def formatter(array):
    if array.dtype == np.dtype('U1'):
        return np.array2string(array, separator='', formatter={'all': lambda x: x})
    if array.dtype == np.dtype('bool'):
        return np.array2string(array, separator='', formatter={'bool': lambda x: '#' if x else '.'})
    return np.array2string(array)


np.set_string_function(formatter, repr=False)
np.set_string_function(formatter, repr=True)
dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

dirs = {
    'R': (0, 1),
    'D': (1, 0),
    'L': (0, -1),
    'U': (-1, 0)
}


class Day18(Day):
    def __init__(self):
        super().__init__("18")

    def parse(self, input):
        self.input = input

    def parser1(self, line):
        direction, length, _ = line.split()
        return direction, int(length)

    def parser2(self, line):
        hexa = line.split()[-1][1:-1]
        return list(dirs.keys())[int(hexa[-1])], int(hexa[1:-1], 16)

    def part0_slow(self, parser):
        visited = []
        pos = (0, 0)
        for line in self.input.splitlines():
            direction, length = parser(line)
            for _ in range(length):
                pos = (pos[0] + dirs[direction][0], pos[1] + dirs[direction][1])
                visited.append(pos)
        visited = np.array(visited)
        visited -= np.min(visited, axis=0)

        mat = np.zeros((np.max(visited, axis=0) + 1), dtype=bool)
        mat[visited[:, 0], visited[:, 1]] = True

        mat = np.pad(mat, 1, 'constant', constant_values=False)
        self.log(mat)
        outside = np.zeros_like(mat, dtype=bool)

        q = Queue()
        q.put((0, 0))
        while not q.empty():
            pos = q.get()
            for dx, dy in dirs.values():
                other = (pos[0] + dx, pos[1] + dy)
                if not outside[other] and not mat[other]:
                    outside[other] = True
                    q.put(other)
        # self.log(~outside)
        self.log(f"Perimeter: {np.sum(mat)}")
        self.log(f"Inner area: {np.sum(~outside)-np.sum(mat)}")
        return np.sum(~outside)

    def part0_fast(self, parser):
        visited = []
        pos = (0, 0)
        min_pos = (0, 0)
        max_pos = (0, 0)
        for line in self.input.splitlines():
            direction, length = parser(line)
            pos = (pos[0] + dirs[direction][0] * length, pos[1] + dirs[direction][1] * length)
            min_pos = (min(min_pos[0], pos[0]), min(min_pos[1], pos[1]))
            max_pos = (max(max_pos[0], pos[0]), max(max_pos[1], pos[1]))
            visited.append(pos)

        area = 0
        perimeter = 0
        pos = (0, 0)
        prev_direction = None
        prev_length = None
        for line in self.input.splitlines():
            direction, length = parser(line)
            pos = (pos[0] + dirs[direction][0] * length, pos[1] + dirs[direction][1] * length)
            perimeter += length

            if direction == 'R':
                if prev_direction == 'D':
                    area_under = - 1
                    self.log(f"DR: {area_under}")
                    area += area_under
                height = max_pos[0] - pos[0]
                width = length
                area_under = height * width
                self.log(f"R: {height}*{width} {area_under}")
                area += area_under
            if direction == 'L':
                height = max_pos[0] - pos[0] + 1
                width = length
                area_under = -height * width
                self.log(f"L: {height}*{width} {area_under}")
                area += area_under
            if direction == 'D':
                if prev_direction == 'L':
                    area_under = - 1
                    self.log(f"LD: {area_under}")
                    area += area_under
                area_under = -(length - 1)
                self.log(f"D: {area_under}")
                area += area_under

            prev_direction = direction
            prev_length = length
        self.log(f"Perimeter: {perimeter}")
        self.log(f"Area: {area}")
        return area + perimeter

    def part1(self):
        self.log(self.part0_fast(self.parser1))
        return self.part0_slow(self.parser1)

    def part2(self):
        return self.part0_fast(self.parser2)


if __name__ == '__main__':
    Day18().main(example=False)
