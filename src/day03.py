#!/bin/env python3
from re import sub
from utils import Day
import numpy as np


class Day03(Day):
    def __init__(self):
        super().__init__("03")

    def part1(self):
        res = 0
        self.grid = [list(line) for line in self.input.splitlines()]
        self.grid = np.array(self.grid)
        self.grid = np.pad(self.grid, 1, 'constant', constant_values='.')

        self.is_symbol = np.vectorize(lambda x: x != '.' and not x.isdigit())(self.grid)

        self.part_numbers = np.zeros_like(self.grid, dtype=int)

        for i, line in enumerate(self.grid):
            starting_j = None
            for j, char in enumerate(line):
                if starting_j is not None:
                    if not char.isdigit():
                        part_number = int(''.join(line[starting_j:j]))
                        self.part_numbers[i, starting_j:j] = part_number
                        if np.any(self.is_symbol[i - 1:i + 2, starting_j - 1:j + 1]):
                            res += part_number
                        starting_j = None
                elif char.isdigit():
                    starting_j = j

        return res

    def part2(self):
        res = 0
        for i, j in zip(*np.nonzero(self.grid == '*')):
            part_numbers = np.unique(self.part_numbers[i-1:i+2, j-1:j+2])
            part_numbers = part_numbers[part_numbers != 0]
            if len(part_numbers) == 2:
                res += np.prod(part_numbers)
        return res


if __name__ == '__main__':
    Day03().main(False)
