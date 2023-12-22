#!/bin/env python3
from utils import Day, formatter

import numpy as np
from queue import Queue


np.set_string_function(formatter, repr=False)
np.set_string_function(formatter, repr=True)
dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
np.set_printoptions(threshold=np.inf, linewidth=np.inf, suppress=True)


class Day21(Day):
    def __init__(self):
        super().__init__("21")

    def parse(self, input):
        grid = np.array([list(line) for line in input.splitlines()])
        self.start = next(zip(*np.where(grid == 'S')))
        self.grid = grid == '#'

    def iterate(self, grid, start, n):
        reachable = np.zeros_like(grid, dtype=bool)
        reachable[start] = True
        # self.log(reachable)
        for _ in range(n):
            reachable = self.step(grid, reachable)
        return np.sum(reachable), reachable

    def step(self, grid, reachable):
        reachable_next = np.zeros_like(grid, dtype=bool)
        reachable_next[1:, :] |= reachable[:-1, :]
        reachable_next[:-1, :] |= reachable[1:, :]
        reachable_next[:, 1:] |= reachable[:, :-1]
        reachable_next[:, :-1] |= reachable[:, 1:]
        reachable_next &= ~grid
        reachable = reachable_next
        return reachable

    def part1(self):
        reachable = np.zeros_like(self.grid, dtype=bool)
        reachable[self.start] = True
        for _ in range(6 if self.example else 64):
            reachable = self.step(self.grid, reachable)
        return np.sum(reachable)

    def part2(self):
        W, H = self.grid.shape

        desired = 5000 if self.example else 26501365
        repeating = max(W, H)
        modulo = desired % repeating

        N = 5 if self.example else 3
        biggrid = np.tile(self.grid, (N * 2 + 1, N * 2 + 1))
        bigstart = (self.start[0] + W * N, self.start[1] + H * N)

        reachable = np.zeros_like(biggrid, dtype=bool)
        reachable[bigstart] = True
        steps = modulo + N * repeating
        counts = np.zeros(steps + 1, dtype=int)
        for i in range(steps):
            reachable = self.step(biggrid, reachable)
            count = np.sum(reachable)
            counts[i + 1] = count
        self.log(f"{steps=} {count=}")

        if self.example:  # With this, and increasing steps by max(W,H) we see the pattern growing
            subcounts = np.zeros((N * 2 + 1, N * 2 + 1))
            for i in range(N * 2 + 1):
                for j in range(N * 2 + 1):
                    subreachable = reachable[i * W:(i + 1) * W, j * H:(j + 1) * H]
                    subcounts[i, j] = np.sum(subreachable)
            self.log(subcounts)

        idx = np.array(list(range(len(counts))))[modulo::repeating]
        counts = counts[modulo::repeating]
        dcounts = np.diff(counts)
        ddcounts = np.diff(dcounts)

        self.log(f"{idx=}")
        self.log(f"{counts=}")
        self.log(f"{dcounts=}")
        self.log(f"{ddcounts=}")

        x = counts[-1]
        v = dcounts[-1]
        a = ddcounts[-1]
        t = (desired - idx[-1]) // (repeating)

        return predict(x, v, a, t)


def predict(x0, v0, a, t):
    x = x0 + v0 * t + a * t * (t + 1) // 2
    return x


if __name__ == '__main__':
    Day21().main(example=False)
