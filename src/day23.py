#!/bin/env python3
from collections import defaultdict
from utils import Day, formatter

import numpy as np
import sys
sys.setrecursionlimit(1000000)

np.set_string_function(formatter, repr=False)
np.set_string_function(formatter, repr=True)
np.set_printoptions(threshold=np.inf, linewidth=np.inf, suppress=True)


def dfs(pos, end, visited, connectivity):
    # print(pos, sorted(list(visited)))
    if pos == end:
        return 0
    visited.add(pos)
    res = -1e9
    for next_pos in connectivity[pos]:
        if next_pos not in visited:
            res = max(res, dfs(next_pos, end, visited, connectivity) + 1)
    visited.remove(pos)
    return res


def dfs2(pos, end, visited, connectivity):
    # print(pos, sorted(list(visited)))
    if pos == end:
        return 0
    visited.add(pos)
    res = -1e9
    for next_pos, d in connectivity[pos].items():
        if next_pos not in visited:
            res = max(res, dfs2(next_pos, end, visited, connectivity) + d)
    visited.remove(pos)
    return res


class Day23(Day):
    def __init__(self):
        super().__init__("23")

    def parse(self, input):
        self.grid = np.array([list(line) for line in input.splitlines()])
        self.grid = np.pad(self.grid, 1, constant_values='#')

    def part1(self):
        empties = list(zip(*np.where(self.grid == '.')))
        start, end = empties[0], empties[-1]

        connectivity = defaultdict(set)
        for (x, y) in zip(*np.where(self.grid != '#')):
            match self.grid[x, y]:
                case '>':
                    connectivity[(x, y)].add((x, y + 1))
                case '<':
                    connectivity[(x, y)].add((x, y - 1))
                case '^':
                    connectivity[(x, y)].add((x - 1, y))
                case 'v':
                    connectivity[(x, y)].add((x + 1, y))
                case '.':
                    for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                        if self.grid[x + dx, y + dy] != '#':
                            connectivity[(x, y)].add((x + dx, y + dy))

        return dfs(start, end, set(), connectivity)

    def part2(self):
        empties = list(zip(*np.where(self.grid == '.')))
        start, end = empties[0], empties[-1]

        connectivity = defaultdict(dict)
        for (x, y) in zip(*np.where(self.grid != '#')):
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                if self.grid[x + dx, y + dy] != '#':
                    connectivity[(x, y)][(x + dx, y + dy)] = 1
        # res = dfs2(start, end, set(), connectivity)
        while True:
            try:
                pos, conn = next((pos, conn) for pos, conn in connectivity.items() if len(conn) == 2)
            except StopIteration:
                break
            # print(connectivity)
            del connectivity[pos]
            pos1, pos2 = conn.keys()
            d1, d2 = conn.values()
            if pos2 in connectivity[pos1]:
                print(f"Overwriting {pos1} {pos2} {connectivity[pos1][pos2]} with {d1 + d2}")
                connectivity[pos1][pos2] = max(connectivity[pos1][pos2], d1 + d2)
            else:
                connectivity[pos1][pos2] = d1 + d2
            if pos1 in connectivity[pos2]:
                print(f"Overwriting {pos2} {pos1} {connectivity[pos2][pos1]} with {d1 + d2}")
                connectivity[pos2][pos1] = max(connectivity[pos2][pos1], d1 + d2)
            else:
                connectivity[pos2][pos1] = d1 + d2
            del connectivity[pos1][pos]
            del connectivity[pos2][pos]
            # new_res = dfs2(start, end, set(), connectivity)
            # if res != new_res:
            #     raise Exception(f"Something went wrong when removing {pos} from {pos1} and {pos2}")
        self.log(connectivity)
        # return connectivity
        return dfs2((start), end, set(), connectivity)


if __name__ == '__main__':
    Day23().main(example=False)
