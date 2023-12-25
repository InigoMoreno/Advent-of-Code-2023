#!/bin/env python3
from utils import Day

from collections import defaultdict
from queue import Queue

import networkx as nx
import matplotlib.pyplot as plt
import time


class Day25(Day):
    def __init__(self):
        super().__init__("25")

    def parse(self, input):
        self.G = nx.Graph()
        for line in input.splitlines():
            left, right = line.split(': ')
            for other in right.split(' '):
                self.G.add_edge(left, other)

    def show(self, **kwargs):
        if self.example:
            if not hasattr(self, 'layout'):
                self.layout = nx.spring_layout(self.G)
            nx.draw_networkx(self.G, with_labels=True, pos=self.layout, **kwargs)
            plt.show(block=False)
            plt.pause(2)
            plt.close()

    def part1(self):
        self.show()

        betweenness = nx.edge_betweenness_centrality(self.G)
        ranking = sorted(self.G.edges, key=betweenness.__getitem__, reverse=True)

        self.show(edge_color=[betweenness[edge] for edge in self.G.edges()])

        self.G.remove_edges_from(ranking[:3])

        self.show()

        cc = list(nx.connected_components(self.G))

        self.show(node_color=[0 if node in cc[0] else 1 for node in self.G.nodes()])

        return len(cc[0]) * len(cc[1])

    def part2(self):
        return None


if __name__ == '__main__':
    Day25().main(example=False)
