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

        # rearranged:
        # px + vx*ti -hi.vx*ti = hi.px
        # py + vy*ti -hi.vy*ti = hi.py
        # pz + vz*ti -hi.vz*ti = hi.pz

        # if we have n hailstones
        # we have n*3 equations
        # and 6+n unknowns (px, py, pz, vx, vy, vz, t1, t2, ..., tn)
        # So we should be able to solve it with only 3 hailstones
        # It is non-linear because v* and ti are multiplied together

        # h1.px + h1.vx * t1 = px + vx * t1
        # h2.px + h2.vx * t2 = px + vx * t2
        # h1.py + h1.vy * t1 = py + vy * t1
        # h2.py + h2.vy * t2 = py + vy * t2
        # h1.pz + h1.vz * t1 = pz + vz * t1
        # h2.pz + h2.vz * t2 = pz + vz * t2

        equations = []

        h1, h2, h3 = self.hailstones[:3]

        px, py, pz, vx, vy, vz, t1, t2, t3 = sympy.var('px py pz vx vy vz t1 t2 t3')
        equations.append(h1.px + h1.vx * t1 - px - vx * t1)
        equations.append(h2.px + h2.vx * t2 - px - vx * t2)
        equations.append(h3.px + h3.vx * t3 - px - vx * t3)
        equations.append(h1.py + h1.vy * t1 - py - vy * t1)
        equations.append(h2.py + h2.vy * t2 - py - vy * t2)
        equations.append(h3.py + h3.vy * t3 - py - vy * t3)
        equations.append(h1.pz + h1.vz * t1 - pz - vz * t1)
        equations.append(h2.pz + h2.vz * t2 - pz - vz * t2)
        equations.append(h3.pz + h3.vz * t3 - pz - vz * t3)

        solution = sympy.solve(equations, [px, py, pz, vx, vy, vz, t1, t2, t3])[0]

        return sum(solution[:3])


if __name__ == '__main__':
    Day24().main(example=False)
