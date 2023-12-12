#!/bin/env python3
from utils import Day

import numpy as np


class Day09(Day):
    def __init__(self):
        super().__init__("09")

    def parse(self, input):
        self.histories = [list(map(int, line.split())) for line in input.splitlines()]

    def predict(self, history):
        history_diffs = [np.array(history)]
        while not np.all(history_diffs[-1] == 0):
            history_diffs.append(np.diff(history_diffs[-1]))
        self.log(history_diffs)
        forward = sum(diff[-1] for diff in history_diffs)
        backward = sum(diff[0] * (1 if i % 2 == 0 else -1) for i, diff in enumerate(history_diffs))
        self.log(forward, backward)
        return forward, backward

    def part1(self):
        return sum(self.predict(history)[0] for history in self.histories)

    def part2(self):
        return sum(self.predict(history)[1] for history in self.histories)


if __name__ == '__main__':
    Day09().main(example=False)
