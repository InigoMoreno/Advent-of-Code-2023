#!/bin/env python3
from utils import Day
from functools import cache


@cache
def count_valid(spring, groups, accum=0):
    # print(f"count_valid({spring=}, {groups=}, {accum=})")
    match spring, groups, accum:
        case (), (), 0:
            return 1
        case (), groups, accum:
            return len(groups) == 1 and int(groups[0] == accum)
        case ('.', *rest), groups, 0:
            return count_valid(tuple(rest), groups, 0)
        case ('.', *rest), (first_group, *rest_groups), accum:
            if first_group != accum:
                return 0
            return count_valid(tuple(rest), tuple(rest_groups), 0)
        case ('#', *rest), groups, accum:
            return count_valid(tuple(rest), groups, accum + 1)
        case ('?', *rest), groups, accum:
            return count_valid(('#', *rest), groups, accum) + count_valid(('.', *rest), groups, accum)
    return 0


class Day12(Day):
    def __init__(self):
        super().__init__("12")

    def parse(self, input):
        lines = [line.split() for line in input.splitlines()]
        self.rows = [(tuple(springs), tuple(map(int, groups.split(',')))) for springs, groups in lines]

    def part1(self):
        return sum(count_valid(*row) for row in self.rows)

    def part2(self):
        return sum(count_valid(tuple('?'.join([''.join(a)] * 5)), b * 5) for a, b in self.rows)


if __name__ == '__main__':
    Day12().main(example=False)
