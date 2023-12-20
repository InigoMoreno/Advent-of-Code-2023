#!/bin/env python3
import numpy as np
from utils import Day

from collections import defaultdict
from enum import Enum
from queue import Queue
import math


class ModuleTypes(Enum):
    FlipFlop = 1
    Conjunction = 2
    Broadcaster = 3
    Untyped = 4


class Day20(Day):
    def __init__(self):
        super().__init__("20")

    def parse(self, input):
        self.outputs = defaultdict(list)
        self.inputs = defaultdict(list)
        self.types = defaultdict(lambda: ModuleTypes.Untyped)
        for line in input.splitlines():
            name, outputs = line.split(" -> ")
            if name.startswith("%"):
                name = name[1:]
                self.types[name] = ModuleTypes.FlipFlop
            elif name.startswith("&"):
                name = name[1:]
                self.types[name] = ModuleTypes.Conjunction
            elif name == "broadcaster":
                self.types[name] = ModuleTypes.Broadcaster

            self.outputs[name] = list(outputs.split(", "))
            for output in self.outputs[name]:
                self.inputs[output].append(name)

    def part1(self):
        flip_flop_states = {
            name: False for name in self.outputs.keys() if self.types[name] == ModuleTypes.FlipFlop
        }

        conjunction_memories = {
            name: {other: 0 for other in self.inputs[name]}
            for name in self.outputs.keys() if self.types[name] == ModuleTypes.Conjunction
        }

        total_signals = [0, 0]

        for i in range(1000):
            self.log(f"\nRunning {i}...")
            q = Queue()
            q.put(("button", "broadcaster", 0))
            while not q.empty():
                in_name, out_name, value = q.get()
                self.log(f"{in_name} -{value}-> {out_name}")

                total_signals[value] += 1
                if self.types[out_name] == ModuleTypes.Broadcaster:
                    for output in self.outputs[out_name]:
                        q.put((out_name, output, value))
                if self.types[out_name] == ModuleTypes.FlipFlop and value == 0:
                    flip_flop_states[out_name] = not flip_flop_states[out_name]
                    for output in self.outputs[out_name]:
                        q.put((out_name, output, int(flip_flop_states[out_name])))
                if self.types[out_name] == ModuleTypes.Conjunction:
                    conjunction_memories[out_name][in_name] = value
                    all_on = int(not all(conjunction_memories[out_name].values()))
                    for output in self.outputs[out_name]:
                        q.put((out_name, output, all_on))

        return total_signals[0] * total_signals[1]

    def part2(self):
        flip_flop_states = {
            name: False for name in self.outputs.keys() if self.types[name] == ModuleTypes.FlipFlop
        }

        conjunction_memories = {
            name: {other: 0 for other in self.inputs[name]}
            for name in self.outputs.keys() if self.types[name] == ModuleTypes.Conjunction
        }

        total_signals = [0, 0]

        s = set()

        for i in range(9000):
            self.log(f"\nRunning {i}...")
            q = Queue()
            q.put(("button", "broadcaster", 0))
            while not q.empty():
                in_name, out_name, value = q.get()
                self.log(f"{in_name} -{value}-> {out_name}")
                if out_name == "rx" and value == 0:
                    return i

                if any(conjunction_memories["nr"].values()):
                    v = tuple(conjunction_memories["nr"].values())
                    if (i, v) not in s:
                        self.log(i, conjunction_memories["nr"])
                        s.add((i, v))

                total_signals[value] += 1
                if self.types[out_name] == ModuleTypes.Broadcaster:
                    for output in self.outputs[out_name]:
                        q.put((out_name, output, value))
                if self.types[out_name] == ModuleTypes.FlipFlop and value == 0:
                    flip_flop_states[out_name] = not flip_flop_states[out_name]
                    for output in self.outputs[out_name]:
                        q.put((out_name, output, int(flip_flop_states[out_name])))
                if self.types[out_name] == ModuleTypes.Conjunction:
                    conjunction_memories[out_name][in_name] = value
                    all_on = int(not all(conjunction_memories[out_name].values()))
                    for output in self.outputs[out_name]:
                        q.put((out_name, output, all_on))

        Ns = [
            np.diff(sorted([i for i, vs in list(s) if vs[pos] == 1]))[0]
            for pos in range(len(conjunction_memories["nr"].values()))
        ]

        return math.lcm(*Ns)


if __name__ == '__main__':
    Day20().main(example=False)
