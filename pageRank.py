from Graph import Graph
import argparse
import pandas as pd
import time


def value_calc(graph, row, prev_col):
    d_factor = 0.85
    node_label = row
    incoming_nodes = graph.nodes[node_label].incoming_edges
    pr = ((1 - d_factor)/len(graph.nodes)) + d_factor * \
        sum([prev_col[node]/len(graph.nodes[node].outgoing_edges)
            for node in incoming_nodes])
    return pr


def pagerank(graph, num_iterations=None):
    # init pagerank matrix
    begin = time.perf_counter()
    num_iterations = 5 if not num_iterations else num_iterations
    pagerank = pd.DataFrame(columns=[f"iter{iteration}" for iteration in range(
        num_iterations)], index=graph.nodes.keys())
    pagerank['iter0'] = 1/len(graph.nodes.keys())
    for iteration in range(1, num_iterations):
        pagerank[f'iter{iteration}'] = pagerank.index.map(lambda entry: value_calc(
            graph, entry, pagerank[f'iter{iteration - 1}']))
    end = time.perf_counter()
    graph.set_pagerank_time(end - begin)
    return pagerank


def sort_pagerank(df):
    last_iteration_col = df[df.columns[-1]]
    sorted_series = last_iteration_col.sort_values(ascending=False)
    return sorted_series


def initialize_graph(dataset):
    graph = Graph(dataset)
    return graph


def print_metrics(graph, page_scores, iterations):
    print(f"Number of iterations: {iterations}")
    print("Graph initialization (read) time: {:.6f} seconds".format(graph.initialization_time))
    if len(graph.nodes) <= 500:
        for x in page_scores:
            print(x)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("PageRank calculation.")
    parser.add_argument('dataset', type=str,
                        help='path to the dataset to perform pagerank on.')
    args = parser.parse_args()
    g = initialize_graph(args.dataset)
    pr = pagerank(g, 20)
    page_scores = sort_pagerank(pr)
    print_metrics(g, page_scores, 20)

