#!/bin/env python3
from utils import Day

import numpy as np

np.set_printoptions(formatter={'bool': lambda x: '#' if x else '.'})


class Day13(Day):
    def __init__(self):
        super().__init__("13")

    def parse(self, input):
        self.blocks = [np.array([list(line) for line in block.splitlines()]) == '#' for block in input.split('\n\n')]

    def is_reflect_vertical(self, block, n, off_by=0):
        left_hand_side = block[:, :n][:, ::-1]
        right_hand_side = block[:, n:]
        min_width = min(left_hand_side.shape[1], right_hand_side.shape[1])
        left_hand_side = left_hand_side[:, :min_width]
        right_hand_side = right_hand_side[:, :min_width]
        return np.sum(left_hand_side != right_hand_side) == off_by

    def reflect_value(self, block, off_by=0):
        for n in range(1, block.shape[1]):
            if self.is_reflect_vertical(block, n, off_by):
                return n
        for n in range(1, block.shape[0]):
            if self.is_reflect_vertical(block.T, n, off_by):
                return n*100
        return None

    def part1(self):
        return sum(self.reflect_value(block) for block in self.blocks)

    def part2(self):
        return sum(self.reflect_value(block, off_by=1) for block in self.blocks)


if __name__ == '__main__':
    Day13().main(example=False)
