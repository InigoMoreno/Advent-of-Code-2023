#!/bin/env python3
from utils import Day, formatter
import numpy as np
from queue import PriorityQueue
from collections import defaultdict


np.set_string_function(formatter, repr=False)
np.set_string_function(formatter, repr=True)
dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def reconstruct_path(cameFrom, current):
    total_path = [current]
    while current in cameFrom.keys():
        current = cameFrom[current]
        total_path.append(current)
    return total_path


class Day17(Day):
    def __init__(self):
        super().__init__("17")

    def parse(self, input):
        self.heat_loss = np.array([list(map(int, line)) for line in input.splitlines()])

    def heuristic(self, item):
        return 0
        pos, _, _ = item
        return 10 * (abs(pos[0] - self.heat_loss.shape[0]) + abs(pos[1] - self.heat_loss.shape[1]))

    def part1(self):
        start = ((0, 0), (0, 0), 1)
        q = PriorityQueue()
        q.put((self.heuristic(start), start))
        openSet = set()
        openSet.add(start)
        cameFrom = {}
        gScore = defaultdict(lambda: float('inf'))
        fScore = defaultdict(lambda: float('inf'))
        gScore[start] = 0
        fScore[start] = self.heuristic(start)

        while not q.empty():
            heat_loss, current = q.get()
            if current[0][0] == self.heat_loss.shape[0] - 1 and current[0][1] == self.heat_loss.shape[1] - 1:
                return heat_loss
            for d in dirs:
                next_pos = (current[0][0] + d[0], current[0][1] + d[1])
                if next_pos[0] < 0 or next_pos[0] >= self.heat_loss.shape[0]:
                    continue
                if next_pos[1] < 0 or next_pos[1] >= self.heat_loss.shape[1]:
                    continue
                if d == (-current[1][0], -current[1][1]):
                    continue
                if d == current[1]:
                    if current[2] == 3:
                        continue
                    neighbor = (next_pos, d, current[2] + 1)
                else:
                    neighbor = (next_pos, d, 1)
                tentative_gScore = gScore[current] + self.heat_loss[next_pos]
                if tentative_gScore < gScore[neighbor]:
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = tentative_gScore + self.heuristic(neighbor)
                    if neighbor not in openSet:
                        q.put((fScore[neighbor], neighbor))
                        openSet.add(neighbor)
        return q

    def part2(self):
        start = ((0, 0), (0, 0), 1)
        q = PriorityQueue()
        q.put((self.heuristic(start), start))
        openSet = set()
        openSet.add(start)
        cameFrom = {}
        gScore = defaultdict(lambda: float('inf'))
        fScore = defaultdict(lambda: float('inf'))
        gScore[start] = 0
        fScore[start] = self.heuristic(start)

        while not q.empty():
            heat_loss, current = q.get()
            if current[0][0] == self.heat_loss.shape[0] - 1 and current[0][1] == self.heat_loss.shape[1] - 1:
                return heat_loss
            next_dirs = dirs
            if current[2] < 4 and current[1] in dirs:
                next_dirs = [current[1]]
            for d in next_dirs:
                next_pos = (current[0][0] + d[0], current[0][1] + d[1])
                if next_pos[0] < 0 or next_pos[0] >= self.heat_loss.shape[0]:
                    continue
                if next_pos[1] < 0 or next_pos[1] >= self.heat_loss.shape[1]:
                    continue
                if d == (-current[1][0], -current[1][1]):
                    continue
                if d == current[1]:
                    if current[2] == 10:
                        continue
                    neighbor = (next_pos, d, current[2] + 1)
                else:
                    neighbor = (next_pos, d, 1)
                tentative_gScore = gScore[current] + self.heat_loss[next_pos]
                if tentative_gScore < gScore[neighbor]:
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = tentative_gScore + self.heuristic(neighbor)
                    if neighbor not in openSet:
                        q.put((fScore[neighbor], neighbor))
                        openSet.add(neighbor)
        return q


if __name__ == '__main__':
    Day17().main(example=False)
