import pandas as pd
import re
import time


class Node:
    outgoing_edges = set()
    incoming_edges = set()
    node_label = None

    def __init__(self, node_label):
        self.node_label = node_label

    def add_edge(self, node_label, direction):
        # outgoing -> 0
        # incoming -> 1
        if direction == 1:
            self.incoming_edges.add(node_label)
        else:
            self.outgoing_edges.add(node_label)


class Graph:
    nodes = {}  # key -> node label, val -> node object
    initialization_time = 0

    def __init__(self, file_name):
        begin = time.perf_counter()
        if "wiki" in file_name or "p2p" in file_name or "soc" in file_name or "amazon" in file_name:
            print("SNAP detected")
            with open(file_name, 'r') as file:
                raw_data = file.readlines()
                [self.node_generator(re.sub(r'(\d)\s+(\d)', r'\1 \2', line.rstrip()).split(' '), True) for line in raw_data]
        else:
            with open(file_name, 'r') as file:
                raw_data = file.readlines()
                [self.node_generator(
                    line.rstrip().split(',')) for line in raw_data]
        end = time.perf_counter()
        self.initialization_time = end - begin

    # helper function for init. Feed in one line of a csv.
    def node_generator(self, csv_line, snap=False):
        if snap:
            # snap datasets are formatted differently
            node_one_label = csv_line[0]
            node_two_label = csv_line[1]
            direction_one = 0
            direction_two = 1
        else:
            # smaller dataset
            node_one_label = csv_line[0]
            direction_one = int(csv_line[1])
            node_two_label = csv_line[2]
            direction_two = int(csv_line[3])

        if node_one_label not in self.nodes:
            node_one = Node(node_one_label)
            self.nodes[node_one_label] = node_one

        if node_two_label not in self.nodes:
            node_two = Node(node_two_label)
            self.nodes[node_two_label] = node_two

        if direction_one == direction_two:
            # undirected graph
            # add outgoing edges to node
            self.nodes[node_one_label].add_edge(node_two_label, 1)
            self.nodes[node_two_label].add_edge(node_one_label, 1)
            # add incoming edges to node
            self.nodes[node_one_label].add_edge(node_two_label, 0)
            self.nodes[node_two_label].add_edge(node_one_label, 0)
        else:
            # directed graph
            if direction_one < direction_two:
                self.nodes[node_one_label].add_edge(node_two_label, 1)
                self.nodes[node_two_label].add_edge(node_two_label, 0)
            else:
                self.nodes[node_two_label].add_edge(node_one_label, 1)
                self.nodes[node_one_label].add_edge(node_two_label, 0)


if __name__ == "__main__":
    g = Graph('./data/snap/amazon0505.txt')
    print(g.initialization_time)
    print(g.nodes['410209'].outgoing_edges)
