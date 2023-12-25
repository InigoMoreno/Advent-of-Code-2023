#!/bin/env python3
from utils import Day
import dataclasses
import sympy
import numpy as np


@dataclasses.dataclass
class Hailstone:
    px: int
    py: int
    pz: int
    vx: int
    vy: int
    vz: int

    @classmethod
    def parse(cls, line):
        px, py, pz, vx, vy, vz = map(int, line.replace('@', ',').split(','))
        return cls(px, py, pz, vx, vy, vz)

    def __repr__(self):
        return f"{self.px}, {self.py}, {self.pz} @ {self.vx}, {self.vy}, {self.vz}"


class Day24(Day):
    def __init__(self):
        super().__init__("24")

    def parse(self, input):
        self.hailstones = [Hailstone.parse(line) for line in input.splitlines()]

    def part1(self):
        # a.px + a.vx*ta = b.px + b.vx * tb
        # a.py + a.vy*ta = b.py + b.vy * tb

        # (a.px-b.px)/b.vx + a.vx*ta/b.vx = tb
        # (a.py-b.py)/b.vy + a.vy*ta/b.vy = tb

        # (a.px-b.px)/b.vx + a.vx*ta/b.vx = (a.py-b.py)/b.vy + a.vy*ta/b.vy

        # (a.px-b.px)/b.vx - (a.py-b.py)/b.vy = a.vy*ta/b.vy - a.vx*ta/b.vx

        # (a.px-b.px)/b.vx - (a.py-b.py)/b.vy = ta * (a.vy/b.vy - a.vx/b.vx)
        count = 0
        min_value = 7 if self.example else 200000000000000
        max_value = 27 if self.example else 400000000000000
        for i in range(len(self.hailstones)):
            a = self.hailstones[i]
            for j in range(i + 1, len(self.hailstones)):
                b = self.hailstones[j]
                self.log(f"\nHalistone A: {a}")
                self.log(f"Halistone B: {b}")
                den = (a.vy / b.vy - a.vx / b.vx)
                if den == 0:
                    self.log("Hailstones are parallel\n")
                    continue
                ta = ((a.px - b.px) / b.vx - (a.py - b.py) / b.vy) / den
                tb = (a.px - b.px) / b.vx + a.vx * ta / b.vx
                if ta < 0 or tb < 0:
                    self.log("Hailstones' intersection is in the past\n")
                    continue
                x = a.px + ta * a.vx
                y = a.py + ta * a.vy
                self.log(f"x = {x}, y = {y}")
                if x < min_value or x > max_value or y < min_value or y > max_value:
                    self.log("Hailstones' intersection is out of bounds\n")
                    continue
                count += 1
        return count

    def part2(self):
        # for every hailstone hi:
        # hi.px + hi.vx * ti = px + vx * ti
        # hi.py + hi.vy * ti = py + vy * ti
        # hi.pz + hi.vz * ti = pz + vz * ti

        # if we have n hailstones
        # we have n*3 equations
        # and 6+n unknowns (px, py, pz, vx, vy, vz, t1, t2, ..., tn)
        # So we should be able to solve it with only 3 hailstones
        # It is non-linear because v* and ti are multiplied together

        equations = []

        vars = sympy.var('px py pz vx vy vz')
        px, py, pz, vx, vy, vz = vars

        for i, hi in enumerate(self.hailstones[:3]):
            ti = sympy.var(f't{i}')
            vars += (ti,)
            equations.append(hi.px + hi.vx * ti - px - vx * ti)
            equations.append(hi.py + hi.vy * ti - py - vy * ti)
            equations.append(hi.pz + hi.vz * ti - pz - vz * ti)

        solution = sympy.solve(equations, vars)[0]

        self.log(solution)

        return sum(solution[:3])


if __name__ == '__main__':
    Day24().main(example=True)
