#!/bin/env python3
from utils import Day, formatter
import numpy as np
from queue import Queue


np.set_string_function(formatter, repr=False)
np.set_string_function(formatter, repr=True)

dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def next_dir(d, tile):
    match d, tile:
        case d, '.':
            return [d]
        case (x1, x2), '\\':
            return [(x2, x1)]
        case (x1, x2), '/':
            return [(-x2, -x1)]
        case (x2, 0), '-':
            return [(0, 1), (0, -1)]
        case (0, x2), '-':
            return [d]
        case (0, x2), '|':
            return [(1, 0), (-1, 0)]
        case (x2, 0), '|':
            return [d]
    return []


class Day16(Day):
    def __init__(self):
        super().__init__("16")

    def parse(self, input):
        self.input = np.array([list(line) for line in input.splitlines()])
        self.input = np.pad(self.input, 1, 'constant', constant_values=' ')

    def part1(self, pos=(1, 1), d=(0, 1)):
        visited = set()
        energized = np.zeros_like(self.input, dtype=bool)
        energized_with_dirs = np.zeros((*self.input.shape, 4), dtype=bool)

        q = Queue()
        q.put((pos, d))

        while not q.empty():
            pos, d = q.get()
            if (pos, d) in visited:
                continue
            energized[pos] = True
            energized_with_dirs[pos][dirs.index(d)] = True
            visited.add((pos, d))
            for d in next_dir(d, self.input[pos]):
                q.put(((pos[0] + d[0], pos[1] + d[1]), d))

        res = np.full_like(energized, ' ', dtype='U1')
        res[energized_with_dirs[:, :, 0]] = '>'
        res[energized_with_dirs[:, :, 1]] = 'v'
        res[energized_with_dirs[:, :, 2]] = '<'
        res[energized_with_dirs[:, :, 3]] = '^'
        s = np.sum(energized_with_dirs, axis=2)
        res[s == 0] = self.input[s == 0]
        res[s > 1] = '2'
        self.log(res[1:-1, 1:-1])
        return np.sum(energized[1:-1, 1:-1])

    def part2(self):
        max_energy = 0
        for i in range(self.input.shape[0]):
            max_energy = max(max_energy, self.part1((i, 1), (0, 1)))
            max_energy = max(max_energy, self.part1((i, self.input.shape[1] - 2), (0, -1)))
        for i in range(self.input.shape[1]):
            max_energy = max(max_energy, self.part1((1, i), (1, 0)))
            max_energy = max(max_energy, self.part1((self.input.shape[0] - 2, i), (-1, 0)))
        return max_energy


if __name__ == '__main__':
    Day16().main(example=False)
