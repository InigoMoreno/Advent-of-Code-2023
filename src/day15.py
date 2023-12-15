#!/bin/env python3
from utils import Day

from collections import defaultdict, OrderedDict


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
        slots = defaultdict(OrderedDict)
        for step in self.input.split(','):
            if '=' in step:
                label, value = step.split('=')
                slots[hash(label)][label] = int(value)
            elif '-' in step:
                label, _ = step.split('-')
                index = hash(label)
                if label in slots[index]:
                    del slots[index][label]
            self.log(f"After \"{step}\"")
            for label, values in slots.items():
                if len(values) > 0:
                    self.log(f"Box {label}: {list(values.items())}")
            self.log()
        return sum([(index + 1) * (position + 1) * value for index, boxes in slots.items()
                   for position, value in enumerate(boxes.values())])


if __name__ == '__main__':
    Day15().main(example=False)
