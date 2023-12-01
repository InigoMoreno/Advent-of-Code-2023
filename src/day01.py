#!/bin/env python3
from utils import Day


class Day1(Day):
    def __init__(self):
        super().__init__("01")

    def find_digits1(self, line):
        digits = []
        for char in line:
            if char.isdigit():
                digits.append(int(char))
        return digits

    def find_digits2(self, line):
        # This time the digits can also be typed out as words
        possible_words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
                          '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        smallest_index = len(line)
        smallest_digit = None
        biggest_index = -1
        biggest_digit = None
        for i, word in enumerate(possible_words):
            if word in line:
                index = line.find(word)
                if index < smallest_index:
                    smallest_index = index
                    smallest_digit = i % 10
                index = line.rfind(word)
                if index > biggest_index:
                    biggest_index = index
                    biggest_digit = i % 10
        return smallest_digit, biggest_digit

    def part0(self, fn):
        digits_per_line = [fn(line) for line in self.input.splitlines()]
        return sum(digits[0] * 10 + digits[-1] for digits in digits_per_line)

    def part1(self):
        return self.part0(self.find_digits1)

    def part2(self):
        return self.part0(self.find_digits2)


if __name__ == '__main__':
    Day1().main()
