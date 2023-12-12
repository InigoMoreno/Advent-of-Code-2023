#!/bin/env python3
from utils import Day
import numpy as np


class Day04(Day):
    def __init__(self):
        super().__init__("04")

    def part1(self):
        self.cards = [
            tuple(set(int(element) for element in side.split(' ') if element)
                  for side in line.split(': ')[-1].strip().split(' | '))
            for line in self.input.splitlines()
        ]

        points = 0
        self.n_winners = [len(set.intersection(numbers_you_have, winning_numbers))
                          for numbers_you_have, winning_numbers in self.cards]
        for n_winners in self.n_winners:
            if n_winners > 0:
                points += 2**(n_winners - 1)
        return points

    def part2(self):
        N = len(self.cards)
        n_cards = np.ones(N, dtype=int)
        for i in range(N):
            n_won = self.n_winners[i]
            if n_won > 0:
                n_cards[i + 1:i + n_won + 1] += n_cards[i]

        return np.sum(n_cards)


if __name__ == '__main__':
    Day04().main(example=False)
