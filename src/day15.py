#!/bin/env python3
from utils import Day


def hash(string):
    current_value = 0
    for char in string:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256
    return current_value


class Day15(Day):
    def __init__(self):
        super().__init__("15")

    def parse(self, input):
        self.input = input

    def part1(self):
        return sum(hash(step) for step in self.input.split(','))

    def part2(self):
        return None


if __name__ == '__main__':
    Day15().main(example=False)
