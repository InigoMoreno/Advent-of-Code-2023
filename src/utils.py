import argparse
import cProfile
import os
import numpy as np


class Day():
    def __init__(self, day):
        self.day = day

    def parse(self, input):
        self.input = input

    def part1(self):
        raise NotImplementedError

    def part2(self):
        raise NotImplementedError

    def log(self, *args, **kwargs):
        if self.example:
            print(*args, **kwargs)

    def main(self, example=False):
        parser = argparse.ArgumentParser()
        parser.add_argument('--real', '-r', action='store_true')
        parser.add_argument('--example', '-e', action='store_true')
        parser.add_argument('--profile', '-p', action='store_true')
        args = parser.parse_args()

        self.example = example
        if args.example:
            self.example = True
        if args.real:
            self.example = False

        file = f'input/day{self.day}/example.txt' if self.example else f'input/day{self.day}/input.txt'
        with open(file) as f:
            self.parse(f.read().strip())

        if args.profile:
            cProfile.runctx('self.part1()', globals(), locals(), sort='tottime')
        print(f'Part 1: {self.part1()}')

        if self.example and os.path.exists(f'input/day{self.day}/example2.txt'):
            with open(f'input/day{self.day}/example2.txt') as f:
                self.parse(f.read().strip())

        if args.profile:
            cProfile.runctx('self.part2()', globals(), locals(), sort='tottime')
        print(f'Part 2: {self.part2()}')


def formatter(array):
    if array.dtype == np.dtype('U1'):
        return np.array2string(array, separator='', formatter={'all': lambda x: x})
    if array.dtype == np.dtype('bool'):
        return np.array2string(array, separator='', formatter={'bool': lambda x: '#' if x else '.'})
    return np.array2string(array)
