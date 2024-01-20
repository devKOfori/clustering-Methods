**Project Objectives**

1. Implement clustering tool (using Python) that is capable of reading any
text data from this page: http://cs.uef.fi/sipu/datasets/, and output clustering result in two output files:
centroid.txt and partition.txt.
2. Implement dummy clustering algorithm that selects k (user givenparameter) random data points and
   i. Outputs them as the centroids.
   ii. Select the partition of each datapoint randomly (random number from 1 to k) and output the result into the partition file accordingly.

3. Implement two functions
  (a) distance function
  (b) sum-of-squared errors.
  The first one takes any two data objects (or centroids) as input and output their Euclidean distance.
  The second takes both data and the set of centroids as input. It then calculates the sum of squared distances between each
  data object and one randomly chosen centroid. Using your data, calculate pairwise distances between all
  data points, and report the average distance.

*Output format for partition should be a list of integers each on its own line. For centroids, each centroid
should be on its own line where the attribute values (integer or float) are separated by spaces.*

