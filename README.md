# link-analysis

Joey Trevino, jrtrevin@calpoly.edu

## About

This program calculates the PageRank values and PageScores of all nodes in a dataset using the 
PageRank algorithm.

## Running

To run this program, type:

```
$ python3 pageRank.py [-h] [--iterations ITERATIONS] [--verbose] dataset
```

Where `dataset` is the path to a .csv or .txt file containing a dataset with nodes.

### Optional flags

This program runs, by default, for a number of iterations depending on the dataset.
This number is calculated to stop when a default threshold value is obtained.
To provide your own iteration number, provide the optional `--iterations` flag along with an
integer. For example:

```
$ python3 pageRank.py data.csv --i 50
```

Will run the program with 50 iterations until complete.

The `--verbose` flag is useful when working with larger datasets. By default,
SNAP datasets only provide limited output to display. This output is the first
and last 10 lines of the calculated PageRanks and Pagescore values. To request
the full output, regardless of size, type:

```
$ python3 pageRank.py data.csv --v
```

And all output will be displayed.