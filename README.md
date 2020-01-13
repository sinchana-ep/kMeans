# kMeans from scratch

This script implements the k-Means clustering from scratch with an optimization criterion that minimizes the sum of intra-cluster distances. Two data sets are given named Example and Gauss2 as tsv files which can be used to run the program. This script implements a k-Means with k = 3 and the initialization set to c1 = (0, 5), c2 = (0, 4) and c3 = (0, 3).

To run the code give the following command: 

```python kMeans.py --data <PathToInputFile> --output <OutputDirectory>```

For example, the script can be run as follows:

```python kMeans.py --data Example.tsv --output \output```

The output of the program will be two tsv files. One file contains the prototypes for each iteration (including initialization) and the other the optimization criteria.
