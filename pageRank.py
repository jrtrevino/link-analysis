from Graph import Graph
import argparse
import pandas as pd
import time


# Calculate the PageRank of a provided "node" in a dataframe.
# graph -> our overall graph structure object
# node_label -> the name of the node, provided by a dataframe index.
# prev_col -> the prior computed column in our pagerank matrix to assist with
# the calculation.
# return -> float value representing the pagerank with a default dampening factor.
def value_calc(graph, node_label, prev_col):
    d_factor = 0.85
    incoming_nodes = graph.nodes[node_label].incoming_edges
    pr = ((1 - d_factor)/len(graph.nodes)) + d_factor * \
        sum([prev_col[node]/len(graph.nodes[node].outgoing_edges)
            for node in incoming_nodes])
    return pr

# Calculate a PageRank matrix for a provided graph.
# If num_iterations is not provided, a default of 50 is used.
# If a threshold value is met before num_iterations is finished,
# the calculation stops.
# graph -> our overall graph structure object
# num_iterations -> number of pagerank iterations (optional)
# returns -> a DataFrame with pagerank calculations.


def pagerank(graph, provided_iterations=None):
    # init pagerank matrix and variables
    num_iterations = 50 if not provided_iterations else provided_iterations
    stopping_iter = None
    pagerank = pd.DataFrame(columns=[f"iter{iteration}" for iteration in range(
        num_iterations)], index=graph.nodes.keys())
    pagerank['iter0'] = 1/len(graph.nodes.keys())
    threshold = 0.000000000001
    # calculate pagerank
    begin = time.perf_counter()
    for iteration in range(1, num_iterations):
        pagerank[f'iter{iteration}'] = pagerank.index.map(lambda entry: value_calc(
            graph, entry, pagerank[f'iter{iteration - 1}']))
        t = abs(pagerank[f'iter{iteration}'] -
                pagerank[f'iter{iteration - 1}']).mean()
        # only break if user did not provide an iteration number.
        if t < threshold and iteration > 2 and not provided_iterations:
            stopping_iter = iteration
            break
    end = time.perf_counter()
    graph.set_iterations(stopping_iter if stopping_iter else num_iterations)
    graph.set_pagerank_time(end - begin)
    # remove unused columns if max_iter not met
    return pagerank[pagerank.columns[:stopping_iter if stopping_iter else num_iterations + 1]]

# Creates a graph object from a given dataset.
# dataset -> a string path to our csv file.
# returns -> Graph object.
def initialize_graph(dataset):
    graph = Graph(dataset)
    return graph

# Prints the metrics associated with the pagerank calculation.
# graph -> graph returned from initialize_graph
# df -> PageRank matrix returned from pagerank().
# returns -> None
def print_metrics(graph, df, verbose=False):
    series = df[df.columns[-1]].sort_values(ascending=False)
    indices = series.index
    values = series.values
    
    if not g.snap or verbose:
        for i in range(len(values)):
            print("{} {} with pagerank: {}".format(i, indices[i], values[i]))
    else:
        for i in range(10):
            print("{} {} with pagerank: {}".format(i, indices[i], values[i]))
        print(".")
        print(".")
        print(".")
        for i in range(10):
            print("{} {} with pagerank: {}".format(len(values) - 10 + i, indices[len(values) - 10 + i], values[len(values) - 10 + i]))
    print("Read time: {:.6f} seconds".format(
        graph.initialization_time))
    print("Processing time: {:.6f} seconds".format(
        graph.pagerank_calc_time))
    print(f"\nNumber of iterations: {graph.iterations}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser("PageRank calculation.")
    parser.add_argument('dataset', type=str,
                        help='path to the dataset to perform pagerank on.')
    parser.add_argument('--iterations', '--i', type=int, help='Number of iterations to run PageRank for.')
    parser.add_argument('--verbose', '--v', help='Option to display full output of program.', action="store_true")
    args = parser.parse_args()
    g = initialize_graph(args.dataset)
    pr = pagerank(g, args.iterations)
    print_metrics(g, pr, args.verbose)
