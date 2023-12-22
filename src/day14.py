#!/bin/env python3
from utils import Day, formatter

import numpy as np


np.set_string_function(formatter, repr=False)
np.set_string_function(formatter, repr=True)


def find_slide_up_pos(block, i):
    while True:
        if i == 0:
            return i
        if block[i - 1] in ('#', 'O'):
            return i
        i -= 1


def slide_up(block, i):
    res = find_slide_up_pos(block, i)
    block[res], block[i] = block[i], block[res]


def find_rocks(block):
    return tuple(zip(*np.where(block == 'O')))


def slide_all_axis(block):
    for rock in find_rocks(block):
        slide_up(block, *rock)


def slide_all(block):
    np.apply_along_axis(slide_all_axis, 0, block)


def compute_load(block):
    return np.sum(np.where(block[::-1, :] == 'O')[0] + 1)


def compute_loop(i1, i2, i):
    """ Given a seuence of values where i2 loops back to i1, compute the index equivalent to i """
    return i1 + (i - i1) % (i2 - i1)


class Day14(Day):
    def __init__(self):
        super().__init__("14")

    def parse(self, input):
        self.block = np.array([list(line) for line in input.splitlines()])

    def part1(self):
        block = self.block.copy()
        slide_all(block)
        return compute_load(block)

    def part2(self):
        # return
        north_block = self.block.copy()
        east_block = np.rot90(north_block)
        south_block = np.rot90(east_block)
        west_block = np.rot90(south_block)
        rocks = tuple(find_rocks(north_block))
        s = {rocks: (0)}
        l = [compute_load(north_block)]
        for i in range(1, 1000000000):
            slide_all(north_block)
            slide_all(west_block)
            slide_all(south_block)
            slide_all(east_block)
            rocks = tuple(find_rocks(north_block))
            if rocks in s:
                break
            s[rocks] = (i)
            l.append(compute_load(north_block))
        return l[compute_loop(s[rocks], i, 1000000000)]


if __name__ == '__main__':
    Day14().main(example=False)
