#!/bin/env python3
from utils import Day

import numpy as np
from collections import defaultdict
from queue import Queue

# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile,
# but your sketch doesn't show what shape the pipe has.


north = (-1, 0)
south = (1, 0)
east = (0, 1)
west = (0, -1)

connector = {
    '|': [north, south],
    '-': [east, west],
    'L': [north, east],
    'J': [north, west],
    '7': [south, west],
    'F': [south, east],
    'S': [north, south, east, west],
}


class Day10(Day):
    def __init__(self):
        super().__init__("10")

    def parse(self, input):
        self.grid = np.array([list(line) for line in input.splitlines()])
        self.grid = np.pad(self.grid, 1, constant_values='.')
        self.connections = defaultdict(set)
        for x, y in zip(*np.where(self.grid != '.')):
            if self.grid[x, y] == 'S':
                self.start = (x, y)
            for dx, dy in connector[self.grid[x, y]]:
                self.connections[(x, y)].add((x + dx, y + dy))

        self.log(self.connections)
        # Prune non reflecting connections
        for pos in list(self.connections.keys()):
            new_others = self.connections[pos].copy()
            for other in self.connections[pos]:
                if pos not in self.connections[other]:
                    new_others.remove(other)
            self.connections[pos] = new_others
        self.log(self.connections)

    def part1(self):
        self.distances = np.ones_like(self.grid, dtype=int) * np.inf
        self.distances[self.start] = 0
        self.loop = set()
        q = Queue()
        q.put(self.start)
        while not q.empty():
            pos = q.get()
            self.loop.add(pos)
            for other in self.connections[pos]:
                if self.distances[other] > self.distances[pos] + 1:
                    self.distances[other] = self.distances[pos] + 1
                    q.put(other)
        self.log(self.distances)
        return int(np.max(self.distances[self.distances != np.inf]))

    def part2(self):
        self.part1()
        double_grid = np.zeros((self.grid.shape[0] * 2, self.grid.shape[1] * 2), dtype=int)
        for x, y in self.loop:
            double_grid[2 * x, 2 * y] = 1
            for (nx, ny) in self.connections[(x, y)]:
                double_grid[x + nx, y + ny] = 1
        self.log(double_grid)

        q = Queue()
        q.put((0, 0))
        while not q.empty():
            pos = q.get()
            self.loop.add(pos)
            for dx, dy in [north, south, east, west]:
                other = (pos[0] + dx, pos[1] + dy)
                if double_grid[other] == 0:
                    double_grid[other] = 2
                    q.put(other)
        self.log(double_grid)
        normal_grid = double_grid[::2, ::2]
        self.log(normal_grid)
        return np.sum(normal_grid == 0)


if __name__ == '__main__':
    Day10().main(example=False)
