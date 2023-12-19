#!/bin/env python3
from utils import Day

import dataclasses


@dataclasses.dataclass
class Part:
    x: int
    m: int
    a: int
    s: int


@dataclasses.dataclass
class PartRange:
    x: range
    m: range
    a: range
    s: range


class Day19(Day):
    def __init__(self):
        super().__init__("19")

    def evaluate_part(self, part: Part, workflow_key: str = "in"):
        if workflow_key == "A":
            self.log(part)
            return part.x + part.m + part.a + part.s
        elif workflow_key == "R":
            return 0
        for rule in self.workflows[workflow_key]:
            if len(rule) == 1:
                return self.evaluate_part(part, rule[0])
            if eval(rule[0], {"x": part.x, "m": part.m, "a": part.a, "s": part.s}):
                return self.evaluate_part(part, rule[1])

    def evaluate_part_range_inner(self, part_range: PartRange, workflow: list[tuple[str]]):
        rule, *rest = workflow
        if len(rule) == 1:
            return self.evaluate_part_range(part_range, rule[0])
        comp, out = rule
        var = comp[0]
        compchar = comp[1]
        compval = int(comp[2:])
        varrange = getattr(part_range, var)

        successful = None
        failing = None

        # self.log(var, varrange, compchar, compval)

        if compchar == "<":
            if varrange.start >= compval:
                failing = part_range
            elif varrange.stop < compval:
                successful = part_range
            else:
                successful = PartRange(*[range(varrange.start, compval) if v ==
                                         var else getattr(part_range, v) for v in "xmas"])
                failing = PartRange(*[range(compval, varrange.stop) if v ==
                                    var else getattr(part_range, v) for v in "xmas"])
        elif compchar == ">":
            if varrange.stop <= compval:
                failing = part_range
            elif varrange.start > compval:
                successful = part_range
            else:
                successful = PartRange(*[range(compval + 1, varrange.stop) if v ==
                                         var else getattr(part_range, v) for v in "xmas"])
                failing = PartRange(*[range(varrange.start, compval + 1) if v ==
                                    var else getattr(part_range, v) for v in "xmas"])

        res = 0
        if successful:
            res += self.evaluate_part_range(successful, out)
        if failing:
            res += self.evaluate_part_range_inner(failing, rest)
        return res

    def evaluate_part_range(self, part_range: PartRange, workflow_key: str = "in"):
        if workflow_key == "A":
            self.log(part_range)
            return len(part_range.x) * len(part_range.m) * len(part_range.a) * len(part_range.s)
        elif workflow_key == "R":
            return 0
        return self.evaluate_part_range_inner(part_range, self.workflows[workflow_key])

    def parse(self, input):
        workflows, parts = input.split("\n\n")
        workflows = [line.split("{") for line in workflows.splitlines()]
        workflows = [(k, v[:-1].split(",")) for k, v in workflows]
        workflows = {k: [v.split(':') for v in vs] for k, vs in workflows}
        self.workflows = workflows
        parts = [[int(field.split('=')[1]) for field in part[1:-1].split(',')]
                 for part in parts.splitlines()]
        self.parts = [Part(*part) for part in parts]

    def part1(self):
        return sum(self.evaluate_part(part) for part in self.parts)

    def part2(self):
        init_range = PartRange(range(1, 4001), range(1, 4001),
                               range(1, 4001), range(1, 4001))
        return self.evaluate_part_range(init_range, "in")


if __name__ == '__main__':
    Day19().main(example=False)
