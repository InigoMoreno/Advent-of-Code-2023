#!/bin/env python3
from utils import Day, formatter

import numpy as np

from collections import defaultdict
import copy


np.set_string_function(formatter, repr=False)
np.set_string_function(formatter, repr=True)
np.set_printoptions(threshold=np.inf, linewidth=np.inf, suppress=True)


class Day22(Day):
    def __init__(self):
        super().__init__("22")

    def parse(self, input):
        self.blocks = []
        for line in input.splitlines():
            start, end = line.split("~")
            start = tuple(map(int, start.split(",")))
            end = tuple(map(int, end.split(",")))
            self.blocks.append((start, end))
        self.block_starts = np.array([start for start, end in self.blocks])
        self.block_ends = np.array([end for start, end in self.blocks])

    def part1(self):
        self.suported_by = defaultdict(set)
        W, D, H = np.max(self.block_ends, axis=0)
        space = np.full((W + 1, D + 1, H + 1), dtype=int, fill_value=0)
        space[:, :, 0] = -1
        order = np.argsort(self.block_starts[:, 2])
        for i in order:
            start, end = self.blocks[i]
            name = i + 1
            while True:
                below = space[start[0]:end[0] + 1, start[1]:end[1] + 1, start[2] - 1]
                if ~np.all(below == 0):
                    self.suported_by[name] |= set(below[below != 0])
                    break
                start = (start[0], start[1], start[2] - 1)
                end = (end[0], end[1], end[2] - 1)
            self.log(name, ':', below)

            space[start[0]:end[0] + 1, start[1]:end[1] + 1, start[2]:end[2] + 1] = name
        self.log(np.swapaxes(space[:, :, ::-1], 1, 2))
        self.log(self.suported_by)

        indispensable = set()
        for name, supported_by in self.suported_by.items():
            if len(supported_by) == 1:
                indispensable.add(list(supported_by)[0])
        return len(self.blocks) - len(indispensable) + 1

    def part2(self):
        res = 0
        for i in range(len(self.blocks)):
            name = i + 1
            falling = set()
            falling.add(name)
            changed = True
            while changed:
                changed = False
                for name, supported_by in self.suported_by.items():
                    if name in falling:
                        continue
                    if len(supported_by - falling) == 0:
                        falling.add(name)
                        changed = True
            self.log(i+1, falling - {i+1})
            res += len(falling) - 1
        return res


if __name__ == '__main__':
    Day22().main(example=False)
