#!/bin/env python3
from numpy import maximum
from utils import Day
from collections import defaultdict


class Day02(Day):
    def __init__(self):
        super().__init__("02")

    def part1(self):
        maximums = {
            'red': 12,
            'green': 13,
            'blue': 14,
        }
        res = 0
        for i, line in enumerate(self.input.splitlines()):
            _, game = line.split(': ')
            possible = True
            for step in game.split('; '):
                for amount_color in step.split(', '):
                    amount, color = amount_color.split(' ')
                    amount = int(amount)
                    if amount > maximums[color]:
                        possible = False
                        break
            if possible:
                res += i + 1
        return res

    def part2(self):
        res = 0
        for i, line in enumerate(self.input.splitlines()):
            _, game = line.split(': ')
            shown = defaultdict(int)
            for step in game.split('; '):
                for amount_color in step.split(', '):
                    amount, color = amount_color.split(' ')
                    amount = int(amount)
                    if amount > shown[color]:
                        shown[color] = amount
            power = shown['red'] * shown['green'] * shown['blue']
            res += power
        return res


if __name__ == '__main__':
    Day02().main(False)
