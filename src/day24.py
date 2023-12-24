#!/bin/env python3
from utils import Day
import dataclasses
import scipy.optimize
import numpy as np


@dataclasses.dataclass
class Hailstone:
    px: int
    py: int
    pz: int
    vx: int
    vy: int
    vz: int

    r: np.ndarray = dataclasses.field(init=False)
    v: np.ndarray = dataclasses.field(init=False)

    @classmethod
    def parse(cls, line):
        px, py, pz, vx, vy, vz = map(int, line.replace('@', ',').split(','))
        return cls(px, py, pz, vx, vy, vz)

    def __repr__(self):
        return f"{self.px}, {self.py}, {self.pz} @ {self.vx}, {self.vy}, {self.vz}"

    def __post_init__(self):
        self.r = np.array([self.px, self.py, self.pz])
        self.v = np.array([self.vx, self.vy, self.vz])


def distance(h1, h2):
    n = np.cross(h1.v, h2.v)
    d = np.dot(n, h2.r - h1.r)
    return d

# a.px + a.vx*ta = b.px + b.vx * tb
# a.py + a.vy*ta = b.py + b.vy * tb

# (a.px-b.px)/b.vx + a.vx*ta/b.vx = tb
# (a.py-b.py)/b.vy + a.vy*ta/b.vy = tb

# (a.px-b.px)/b.vx + a.vx*ta/b.vx = (a.py-b.py)/b.vy + a.vy*ta/b.vy

# (a.px-b.px)/b.vx - (a.py-b.py)/b.vy = a.vy*ta/b.vy - a.vx*ta/b.vx

# (a.px-b.px)/b.vx - (a.py-b.py)/b.vy = ta * (a.vy/b.vy - a.vx/b.vx)


def intersection(a, b):
    den = (a.vy / b.vy - a.vx / b.vx)
    if den == 0:
        return None, None
    ta = ((a.px - b.px) / b.vx - (a.py - b.py) / b.vy) / den
    tb = (a.px - b.px) / b.vx + a.vx * ta / b.vx
    return ta, tb


class Day24(Day):
    def __init__(self):
        super().__init__("24")

    def parse(self, input):
        self.hailstones = [Hailstone.parse(line) for line in input.splitlines()]

    def part1(self):
        count = 0
        min_value = 7 if self.example else 200000000000000
        max_value = 27 if self.example else 400000000000000
        for i in range(len(self.hailstones)):
            a = self.hailstones[i]
            for j in range(i + 1, len(self.hailstones)):
                b = self.hailstones[j]
                self.log(f"\nHalistone A: {a}")
                self.log(f"Halistone B: {b}")
                ta, tb = intersection(a, b)
                if ta is None or tb is None or ta < 0 or tb < 0:
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

        # We can try using scipy's fsolve
        # Remember that ti>=0

        # Otherwise we can try to find the start r(x,y,z) vector d = (dx, dy, dz) of the middle hailstone
        # we can assume z=0 and norm(d) = 1
        # such that it intersects all hailstones, no matter the time
        # The vector d has to intersect all hailstone paths
        # then for every hailstone hi:
        # dot(cross(d, hi.v), hi.r - r) = 0

        def equations(vars):
            h = Hailstone(*vars)
            return list(
                distance(h, hi)
                for hi in self.hailstones[:4]
            )

        # root = scipy.optimize.fsolve(equations, (10, 10, 10, 10, 10, 10))

        # print(root)
        import sympy
        from sympy.solvers.diophantine import diophantine
        from sympy.solvers.diophantine.diophantine import diop_solve
        px, py, pz, vx, vy, vz = sympy.symbols('px py pz vx vy vz', integer=True)
        res = sympy.solve(equations([px, py, pz, vx, vy, vz]), [px, py, vx, vy], dict=True)

        solution = None
        for r in res:
            self.log("Solution:")
            h = Hailstone(
                px=float(r[px].subs(pz, 0).subs(vz, 1).evalf()),
                py=float(r[py].subs(pz, 0).subs(vz, 1).evalf()),
                pz=0.,
                vx=float(r[vx].subs(pz, 0).subs(vz, 1).evalf()),
                vy=float(r[vy].subs(pz, 0).subs(vz, 1).evalf()),
                vz=1,
            )
            error = sum(distance(h, hi) for hi in self.hailstones)
            self.log(h, error)

            if error <= len(self.hailstones):
                solution = h
                break
            # for k, v in r.items():
            #     print(type(k))
            #     print(k, v.subs(pz, 0).subs(vz, 1))

        # print(distance(res, h1))

        h1, h2 = self.hailstones[:2]
        _, t1 = intersection(solution, h1)
        _, t2 = intersection(solution, h2)

        self.log(t1, t2)

        t1 = int(t1)
        t2 = int(t2)

        p1 = h1.r + h1.v * t1
        p2 = h2.r + h2.v * t2

        self.log(p1, p2)

        solv = (p2 - p1) // (t2 - t1)
        self.log(solv)
        solr = p1 - solv * t1
        self.log(solr)
        # h1.px + h1.vx * t1 = px + vx * t1
        # h2.px + h2.vx * t2 = px + vx * t2

        # h1.py + h1.vy * t1 = py + vy * t1
        # h2.py + h2.vy * t2 = py + vy * t2
        # h1.pz + h1.vz * t1 = pz + vz * t1
        # h2.pz + h2.vz * t2 = pz + vz * t2

        return sum(solr)


if __name__ == '__main__':
    Day24().main(example=False)
