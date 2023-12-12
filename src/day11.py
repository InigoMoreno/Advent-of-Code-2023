#!/bin/env python3
from utils import Day

import numpy as np


def grid_repr(grid):
    # return ''
    return '#' if grid else '.'


# np.set_string_function(grid_repr)
np.set_printoptions(formatter={'bool': grid_repr})


interesting_pairs = [
    (4, 8),
    (0, 6),
    (2, 5),
    (7, 8)
]


class Day11(Day):
    def __init__(self):
        super().__init__("11")

    def parse(self, input):
        self.grid = np.array([list(line) for line in input.splitlines()]) == '#'

    def part1(self):
        # return self.part2(n=2)
        self.log(self.grid)
        empty_rows = np.nonzero(np.all(~self.grid, axis=0))[0]
        empty_cols = np.nonzero(np.all(~self.grid, axis=1))[0]

        expanded_grid = self.grid.copy()
        expanded_grid = np.insert(expanded_grid, empty_cols, 0, axis=0)
        expanded_grid = np.insert(expanded_grid, empty_rows, 0, axis=1)

        self.log(expanded_grid)

        galaxies = list(map(np.array, zip(*np.where(expanded_grid))))
        sum = 0
        for i in range(len(galaxies)):
            for j in range(i + 1, len(galaxies)):
                dist = np.abs(galaxies[i] - galaxies[j]).sum()
                sum += dist
                if (i, j) in interesting_pairs:
                    self.log(f"Between {i+1} and {j+1}: {dist}")
        return sum

    def part2(self, n=None):
        if n is None:
            n = 1000 if self.example else 1000000
        empty_rows = np.all(~self.grid, axis=0)
        empty_cols = np.all(~self.grid, axis=1)
        empty_rows_cumsum = np.cumsum(empty_rows)
        empty_cols_cumsum = np.cumsum(empty_cols)
        galaxies = list(map(np.array, zip(*np.where(self.grid))))
        res = 0
        for i in range(len(galaxies)):
            for j in range(i + 1, len(galaxies)):
                gmin = np.minimum(galaxies[i], galaxies[j])
                gmax = np.maximum(galaxies[i], galaxies[j])

                dist = sum(gmax - gmin)

                # dist += np.sum(empty_rows[gmin[1]:gmax[1]]) * (n-1)
                dist += (empty_rows_cumsum[gmax[1]] - empty_rows_cumsum[gmin[1]]) * (n - 1)
                # dist += np.sum(empty_cols[gmin[0]:gmax[0]]) * (n-1)
                dist += (empty_cols_cumsum[gmax[0]] - empty_cols_cumsum[gmin[0]]) * (n - 1)

                res += dist
                if (i, j) in interesting_pairs:
                    self.log(f"Between {i+1} and {j+1}: {dist}")
        return res


if __name__ == '__main__':
    Day11().main(example=False)
