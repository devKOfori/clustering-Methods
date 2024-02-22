import random
import math
import helpers

class DataPoint:
    def __init__(self, features):
        self.features = features

def generate_centroids(k, dataset):
    centroids = random.sample(dataset, k)
    return centroids

def assign_to_nearest_centroid(dataset, centroids):
    assignments = []
    for point in dataset:
        nearest_centroid_index, _ = helpers.find_nearest_neighbor(point, centroids)
        assignments.append(nearest_centroid_index)
    return assignments

def update_centroids(dataset, assignments, k):
    new_centroids = []
    for i in range(k):
        cluster_points = [dataset[j].features for j in range(len(dataset)) if assignments[j] == i]
        if cluster_points:
            new_centroid = helpers.compute_centroid_average([DataPoint(features) for features in cluster_points])
            new_centroids.append(new_centroid)
        else:
            new_centroids.append(random.choice(dataset).features)  # If empty cluster, choose random point
    return new_centroids

def KMeans(dataset, k, max_iterations=100):
    centroids = generate_centroids(k, dataset)
    
    for _ in range(max_iterations):
        old_centroids = centroids[:]
        
        # Assign points to nearest centroid
        assignments = assign_to_nearest_centroid(dataset, centroids)
        
        # Update centroids
        centroids = update_centroids(dataset, assignments, k)
        
        # Check for convergence
        if all(c1 == c2 for c1, c2 in zip(old_centroids, centroids)):
            break
    
    return assignments, centroids

# Example usage:
# Assuming dataset is a list of DataPoint objects
# assignments, centroids = KMeans(dataset, k=3)
