#!/bin/env python3
from dataclasses import dataclass
from utils import Day
from collections import Counter

card_order_1 = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'][::-1]
card_order_2 = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J'][::-1]


@dataclass
class Hand:
    hand: str
    bid: int = 0
    with_jokers: bool = False

    def type(self):
        counter = Counter(self.hand)
        if self.with_jokers:
            n_jokers = counter['J']
            counter['J'] = 0
            max_key = max(counter, key=counter.get)
            counter[max_key] += n_jokers
        unique_counts = counter.values()
        if 5 in unique_counts:
            return 7
        if 4 in unique_counts:
            return 6
        if 3 in unique_counts and 2 in unique_counts:
            return 5
        if 3 in unique_counts:
            return 4
        if Counter(unique_counts)[2] == 2:
            return 3
        if 2 in unique_counts:
            return 2
        return 1

    def card_values(self):
        if self.with_jokers:
            return [card_order_2.index(card) for card in self.hand]
        return [card_order_1.index(card) for card in self.hand]

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            if self.type() == other.type():
                return self.card_values() < other.card_values()
            else:
                return self.type() < other.type()

        return NotImplemented


class Day07(Day):
    def __init__(self):
        super().__init__("07")
        self.card_order = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'][::-1]

    def parse(self, input):
        hands = [line.split() for line in input.splitlines()]
        self.hands = [Hand(hand, int(bid)) for hand, bid in hands]

    def part0(self):
        ranking = list(enumerate(sorted(self.hands)))
        self.log(ranking)
        return sum((rank + 1) * hand.bid for rank, hand in ranking)

    def part1(self):
        return self.part0()

    def part2(self):
        for hand in self.hands:
            hand.with_jokers = True
        return self.part0()


if __name__ == '__main__':
    Day07().main(example=False)
