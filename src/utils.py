import argparse
import cProfile
import os


class Day():
    def __init__(self, day):
        self.day = day

    def part1(self):
        raise NotImplementedError

    def part2(self):
        raise NotImplementedError

    def main(self, example=False):
        parser = argparse.ArgumentParser()
        parser.add_argument('--real', '-r', action='store_true')
        parser.add_argument('--example', '-e', action='store_true')
        parser.add_argument('--profile', '-p', action='store_true')
        args = parser.parse_args()

        if args.example:
            example = True
        if args.real:
            example = False

        file = f'input/day{self.day}/example.txt' if example else f'input/day{self.day}/input.txt'
        with open(file) as f:
            self.input = f.read().strip()

        if args.profile:
            cProfile.runctx('self.part1()', globals(), locals(), sort='tottime')
        print(f'Part 1: {self.part1()}')

        if example and os.path.exists(f'input/day{self.day}/example2.txt'):
            with open(f'input/day{self.day}/example2.txt') as f:
                self.input = f.read().strip()

        if args.profile:
            cProfile.runctx('self.part2()', globals(), locals(), sort='tottime')
        print(f'Part 2: {self.part2()}')
