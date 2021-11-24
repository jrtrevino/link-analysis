import pandas as pd
import re
import time


class Node:
    outgoing_edges = None
    incoming_edges = None
    node_label = None

    def __init__(self, node_label):
        self.node_label = node_label
        self.outgoing_edges = list()
        self.incoming_edges = list()

    def add_edge(self, node_label, direction):
        # outgoing -> 0
        # incoming -> 1
        if direction == 1:
            self.incoming_edges.append(node_label)
        else:
            self.outgoing_edges.append(node_label)

    def print(self):
        print(f"Node: {self.node_label}")
        print(f"Incoming edges: {self.incoming_edges}")
        print(f"Outgoing edges: {self.outgoing_edges}")


class Graph:
    nodes = None  # key -> node label, val -> node object
    initialization_time = 0
    pagerank_calc_time = 0
    iterations = 0
    threshold = 0
    d_factor = 0
    snap = None

    def __init__(self, file_name):
        begin = time.perf_counter()
        self.nodes = {}
        if "wiki" in file_name or "p2p" in file_name or "soc" in file_name or "amazon" in file_name:
            print("SNAP detected")
            self.snap = True
            with open(file_name, 'r') as file:
                raw_data = file.readlines()
                # remove header comments from snap file.
                [self.node_generator(re.sub(
                    r'(\d)\s+(\d)', r'\1 \2', line.rstrip()).split(' '), True) for line in raw_data[4:]]
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
            node_one_label = re.sub('[!@#"$]', '', csv_line[0]).lstrip()
            node_two_label = re.sub('[!@#$]', '', csv_line[1]).lstrip()
            direction_one = 0
            direction_two = 1
        else:
            # smaller dataset
            node_one_label = re.sub('[!@#"$]', '', csv_line[0]).lstrip()
            direction_one = int(csv_line[1])
            node_two_label = re.sub('[!@#$"]', '', csv_line[2]).lstrip()
            direction_two = int(csv_line[3])

        if node_one_label not in self.nodes:
            node_one = Node(node_one_label)
            self.nodes[node_one_label] = node_one

        if node_two_label not in self.nodes:
            node_two = Node(node_two_label)
            self.nodes[node_two_label] = node_two

        if direction_one <= direction_two:
            # undirected graph
            # add outgoing edges to node
            # should only have to had the line below since each two lines adds
            self.nodes[node_one_label].add_edge(node_two_label, 0)
            self.nodes[node_two_label].add_edge(node_one_label, 1)
        else:
            # node one has incoming edge from two
            self.nodes[node_one_label].add_edge(node_two_label, 1)
            # node two has outgoing edge to one
            self.nodes[node_two_label].add_edge(node_one_label, 0)

    def set_pagerank_time(self, time):
        self.pagerank_calc_time = time

    def set_iterations(self, iterations):
        self.iterations = iterations

    def set_threshold(self, threshold):
        self.threshold = threshold

    def set_dfactor(self, d):
        self.d_factor = d
