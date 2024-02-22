import random
import math
from model import DataPoint

def generate_centroids(k, dataset):
    '''
    This function selects k random data points 
    and outputs them as centroids.
    The centroids are outputted into the file centroid.txt
    '''
    centroids = random.sample(dataset, k)
    with open('centroid.txt', 'a') as file:
        for point in centroids:
            # print(point)
            output_line = ""
            for cord in point.features:
                output_line = output_line + str(cord).strip()
                if cord != point.features[-1]:
                    output_line += "\t"
                else:
                    output_line += "\n"
                # print(output_line)
            file.write(output_line)
    return centroids

def generate_random_partitions(k, dataset):
    '''
    This function selects the partition of each data point randomly
    as a number from 1 to k
    where k is the total number of partitions
    and outputs the partition number to partition.txt file
    '''
    try:
        with open('partition.txt', 'a') as file:
            for point in dataset:
                partition = random.randint(1, k)
                output_line = str(partition) + '\n'
                file.write(output_line)
                return True
    except Exception as e:
        print(f"Some error occured while creating the data partitions: {e}")

def square_of_differences(x):
    return x**2

def calculate_euclidean_distance(dp1, dp2):
    substraction_list = dp1 - dp2
    substraction_list_squared = list(map(square_of_differences, substraction_list))
    euclidean_distance = math.sqrt(sum(substraction_list_squared))
    return euclidean_distance

def calculate_sum_of_squared_error(dataset, centroids, random_centroid=True):
    sse = 0
    centroid = centroids
    if random_centroid:
        centroid = random.choice(centroids)
        print(f"Random Centroid: {centroid}")
    for data in dataset:
        sse += calculate_euclidean_distance(data, centroid)**2
    return sse

def calculate_pairwise_distance(dataset):
    sum_of_pairwise_distance = 0
    N = len(dataset)
    len_of_pairwise_distance = (N * (N-1)) / 2
    for i in range(N):
        for j in range(1, N-1):
            euclidean_distance = calculate_euclidean_distance(dataset[i], dataset[j])
            sum_of_pairwise_distance += euclidean_distance
    average_pairwise_distance = sum_of_pairwise_distance / len_of_pairwise_distance
    return average_pairwise_distance

def find_nearest_neighbor(dp, dataset):
    N = len(dataset)
    random_index = random.randint(0, N-1)
    p_nearest_neighbor = dataset[random_index]
    if p_nearest_neighbor == dp:
        random_index = random_index + 1 % N
    minimum_distance = calculate_euclidean_distance(dp, p_nearest_neighbor)
    nearest_neighbor_index = random_index
    nearest_neighbor = p_nearest_neighbor

    for data_index, data in enumerate(dataset, start=1):
        if data == p_nearest_neighbor or data == dp:
            continue
        euclidean_distance = calculate_euclidean_distance(dp, data)
        if euclidean_distance < minimum_distance:
            minimum_distance = euclidean_distance
            nearest_neighbor_index = data_index
            nearest_neighbor = data
    return nearest_neighbor_index, nearest_neighbor

def generate_optimal_partitions(dataset, centroids):
    data_centroids_list = []
    
    for data in dataset:
        nearest_centroid_index, nearest_centroid = find_nearest_neighbor(data, centroids)
        print(nearest_centroid)
        data_centroids_list.append(nearest_centroid_index)
        output_line = str(nearest_centroid_index) 
        if data != dataset[-1]:
            output_line += "\n"
        output_partitions("optimum_partition.txt", output_line)
    return data_centroids_list
    
def output_partitions(output_file: str, partitions_string: str):
    try:
        with open(output_file, "a") as file:
            file.write(partitions_string)
    except Exception as e:
        print(f"An error has occured while outputing partions to file")

def compute_centroid_average(datapoints):
    if not datapoints:
        raise ValueError("Input list is empty")
    
    num_datapoints = len(datapoints)
    num_features = len(datapoints[0].features)
    sum_features = [0] * num_features
    
    for datapoint in datapoints:
        if len(datapoint.features) != num_features:
            raise ValueError("All DataPoint objects must have the same dimension")
        sum_features = [sum(x) for x in zip(sum_features, datapoint.features)]
    
    average_features = [x / num_datapoints for x in sum_features]
    return average_features

def output_labeled_data(k, dataset):
    centroids = generate_centroids(k, dataset)
    try:
        with open("labeled_data.txt", "a") as file:
            for data in dataset:
                nearest_centroid_index, nearest_centroid = find_nearest_neighbor(data, centroids)
                output_line = "\t".join([str(feature) for feature in data.features])
                output_line += "\t" + str(nearest_centroid_index)
                if data != dataset[-1]:
                    output_line += "\n"
                file.write(output_line)
    except Exception as e:
        print(f"An error occured while writing to 'labeled_data.txt' {e}")
    
def find_data_clusters(labeled_dataset: str, centroids):
    try:
        with open(labeled_dataset, "r") as file:
            labeled_data_list = file.readlines()
            print(labeled_data_list)
            total = 0
            for centroid_index, centroid in enumerate(centroids):
                centroid_points = find_centroid_points(centroid_index, labeled_data_list)
                # for data in labeled_data_list:
                #     features_and_centroid = data.split("\t")
                #     # print(features_and_centroid)
                #     data_centroid_index = int(features_and_centroid[2].rstrip("\n"))
                #     # print(data_centroid_index)
                #     if data_centroid_index == centroid_index:
                #         centroid_points.append(features_and_centroid[:2])
                total += len(centroid_points)
                print(f"Centroid index: {centroid_index}\nNo. of Partitions: {len(centroid_points)}")
                print(f"\ntotal {total}")
                # centroid_partitions = [data for data in labeled_data_list if labeled_data_list.split("\t")[2]==centroid_index]
                # print(len(centroid_partitions))
                # # centroid_partition = [data.split("\t")[:2] for data in centroid_partition]
                # centroid_partitions = [DataPoint(list(map(int, centroid_partition.split()[:2]))) for centroid_partition in centroid_partitions]
                # sse = calculate_sum_of_squared_error(centroid_partitions, centroid, random_centroid=False)
                # print(f"Centroid: {centroid}\nSSE: {sse}")
    except Exception as e:
        print(f"An error occured while opening 'labeled_data.txt' {e}")

def find_centroid_points(centroid_index, labeled_data):
    centroid_points = []
    for data in labeled_data:
        features_and_centroid = data.split("\t")
        # print(features_and_centroid)
        data_centroid_index = int(features_and_centroid[2].rstrip("\n"))
        # print(data_centroid_index)
        if data_centroid_index == centroid_index:
            centroid_points.append(features_and_centroid[:2])
    return centroid_points

def update_centroids(dataset, assignments, k):
    new_centroids = []
    for i in range(k):
        # cluster_points = [dataset[j].features for j in range(len(dataset)) if assignments[j] == i]
        cluster_points = [dataset[j] for j in range(len(dataset)) if assignments[j] == i]
        if cluster_points:
            # new_centroid = compute_centroid_average([DataPoint(features) for features in cluster_points])
            new_centroid = compute_centroid_average([datapoint for datapoint in cluster_points])
            new_centroids.append(new_centroid)
        else:
            new_centroids.append(random.choice(dataset).features)  # If empty cluster, choose random point
    return new_centroids


def assign_to_nearest_centroid(dataset, centroids):
    assignments = []
    for point in dataset:
        nearest_centroid_index, _ = find_nearest_neighbor(point, centroids)
        assignments.append(nearest_centroid_index)
    return assignments


def KMeans(dataset, k, max_iterations=100):
    centroids = generate_centroids(k, dataset)
    for i in range(max_iterations):
        assignments = assign_to_nearest_centroid(dataset, centroids)
    
    # print(centroids)
    # for _ in range(max_iterations):
    #     old_centroids = centroids[:]
        
    #     # Assign points to nearest centroid
    #     assignments = assign_to_nearest_centroid(dataset, centroids)
    #     # print(assignments)
        
    #     # Update centroids
    #     centroids = update_centroids(dataset, assignments, k)
    #     print(centroids)
        
    #     # Check for convergence
    #     if all(c1 == c2 for c1, c2 in zip(old_centroids, centroids)):
    #         break
