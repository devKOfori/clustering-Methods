import numpy as np
import math
import random
import os

file_path = "/home/swine/Documents/UEF Courses/Y1_S2_P1/Clustering Methods/Exercises/Exercise 1/Task & Dataset/Ex1 Dataset/s1/s1.txt"
file_name = "s1.txt"
labelled_data_file_path = "optimal_partition.txt"
centroids_file_path = "centroid.txt"

current_dir = os.getcwd()
new_file_path = os.path.join(current_dir, file_name)

def process_original_data(file_path: str):
    """
    This function processes the original dataset
    by removing the Byte Order Mark from the data
    and outputs the processed data into a new file
    """
    with open(file_path, "r") as file:
        lines = file.readlines()
        lines[0] = lines[0].lstrip("\ufeff")

    with open(file_name, "w") as file:
        file.writelines(lines)

def read_data(file_path: str, delim: str="", apply_lstrip: bool = False):
    """
    This function loads data from a text file
    and returns a numpy array as a dataset containing
    all the loaded data
    """
    if apply_lstrip:
        if not os.path.exists(new_file_path):
            process_original_data(file_path)
    dataset = np.genfromtxt(file_path, dtype=int, skip_header=0)
    return dataset

def output_centroids(dataset, k: int, delim: str=""):
    """
    This function selects k random data points 
    and outputs them as centroids.
    The centroids are outputted into the file centroid.txt
    """

    output_file_path = 'centroid.txt'

    centroid_indices = np.random.choice(dataset.shape[0], k, replace=False)
    centroids = dataset[centroid_indices, :]
    np.savetxt(output_file_path, centroids, fmt="%d", delimiter=delim)
    return centroids

def output_partitions(dataset, k):
    '''
    This function selects the partition of each data point randomly
    as a number from 1 to k
    where k is the total number of partitions
    and outputs the partition number to partition.txt file
    '''
    with open('partition.txt', 'a') as file:
        for point in dataset:
            partition = random.randint(1, k)
            output_line = str(partition) + '\n'
            file.write(output_line)

def calculate_euclidean_distance(dp1, dp2):
    '''
    This function takes two data objects (or centroids)
    and returns the Euclidean distance between them
    '''
    return np.linalg.norm(dp1 - dp2)

def calculate_sum_of_squared_distance(dataset, centroids, random_centroid: bool = False):
    '''
    This function calculate the sum of squared distance 
    between each data point and a randomly chosen centroid
    '''
    sum_of_squared_distance = 0
    if random_centroid:
        centroid = np.random.choice(centroids.shape[0])
    else:
        centroid = centroids
    for data in dataset:
        sum_of_squared_distance += (calculate_euclidean_distance(data, centroid))**2
    return sum_of_squared_distance

def calculate_pairwise_distance(dataset):
    '''
    This function calculates the pairwise distance 
    between all data points
    and outputs the average pairwise distance between all the data points
    '''
    total_pairwise_distance = 0
    N = len(dataset)
    for i in range(0, N-1):
        for j in range(i+1, N-1):
            euclidean_dist = calculate_euclidean_distance(dataset[i], dataset[j])
            total_pairwise_distance += euclidean_dist
    average_pairwise_distance = total_pairwise_distance / N
    return average_pairwise_distance

def find_nearest_neighbor(datapoint, dataset, tolerance=1e-8):
    # print(f"Data Point: {datapoint}\nDataset: {dataset}")
    # exclude the datapoint itself from the pairwise distance calculations
    dataset_without_datapoint = dataset[~np.all(np.isclose(dataset, datapoint, atol=tolerance), axis=1)]
    distances = np.linalg.norm(dataset_without_datapoint - datapoint, axis=1)
    minimum_distance = np.min(distances)
    nearest_neighbor_index = np.argmin(distances)
    return nearest_neighbor_index, dataset[nearest_neighbor_index]

def get_datapoint_nearest_centroid_index(datapoint, centroids):
    nearest_centroid_index = find_nearest_neighbor(datapoint[:-1], centroids)[0]
    return nearest_centroid_index

def evaluate_datapoint_centroid(dataset, centroids, write_to_file: bool = True):
    """
    This function finds the nearest centroid for each datapoint
    in the dataset
    """
    optimal_partition = []
    with open(labelled_data_file_path, "a") as file:
        for datapoint in dataset:
            nearest_centroid_index = get_datapoint_nearest_centroid_index(datapoint, centroids)
            optimal_partition.append(nearest_centroid_index)
            output_line = f"{str(datapoint[0])} \t {str(datapoint[1])} \t {str(nearest_centroid_index)} \n"
        if write_to_file:    
            file.write(output_line)

    return optimal_partition

def get_centroid_partitions(dataset, centroid_index):
    # print(f"dataset: {dataset}\ncentroid_index: {centroid_index}")
    partition_indices = dataset[:, -1] == centroid_index
    return dataset[partition_indices]

def calculate_centroid_sse(labelled_data_file_path: str, centroids_file_path: str, delim: str = ""):
    labelled_data = read_data(labelled_data_file_path, delim)
    centroids = read_data(centroids_file_path, delim=delim)
    for centroid_index, centroid in enumerate(centroids):
        centroid_partitions = get_centroid_partitions(labelled_data, centroid_index)
        centroid_sse = calculate_sum_of_squared_distance(centroid_partitions[:, :-1], centroid)
        print(f"Centroid {centroid_index + 1}: {centroid} \nSSE Value: {centroid_sse} \n{'-' * 50}")


def update_centroid(dataset):
    new_centroid = np.mean(dataset, axis=0)
    return new_centroid

def kMeans(labelled_data_file_path: str, centroids_file_path: str, delim: str = ""):
    labelled_data = read_data(labelled_data_file_path, delim)
    centroids = read_data(centroids_file_path, delim=delim)
    
    iteration = 0
    centroid_changes_list = []
    while True:
        iteration += 1
        assignment = []

        print(f"{'-----' * 5}\n{iteration}\n{'-----' * 5}")
        for datapoint_index, datapoint in enumerate(labelled_data):
            nearest_centroid_index = get_datapoint_nearest_centroid_index(datapoint, centroids)
            assignment.append(nearest_centroid_index)
            datapoint[-1] = nearest_centroid_index
            print(f"{datapoint_index}. Datapoint: {datapoint}\ncentroid Index: {nearest_centroid_index}")
        print(f"Iteration Number {iteration}\nCentroid Assigned Completely...\n\n\n\n\n\n\n\n\n\n\n")
        
        new_centroids = []
        for centroid_index, centroid in enumerate(centroids):
            centroid_partitions = get_centroid_partitions(labelled_data, centroid_index)
            new_centroid = update_centroid(centroid_partitions)
            print(f"Old Centroid: {centroids[centroid_index]}\nNew Centroid: {new_centroid}")
            new_centroid = new_centroid[:-1]
            centroids[centroid_index] = new_centroid
            new_centroids.append(new_centroid)
        

        centroid_changes = np.linalg.norm(np.array(new_centroids) - np.array(centroids))
        centroid_changes_list.append(centroid_changes)
        if iteration > 1:
            if centroid_changes_list[iteration -2] == centroid_changes_list[iteration-1]:
                print(f"-----------------\n{iteration}\n-----------------")
                break
        # print(centroid_changes)


        

def main():
    # k = int(input('How many partitions do you want to create? '))
    delim = "\t"
    # print("Reading file...")
    # dataset = read_data(file_path, delim, apply_lstrip=True)
    # print("Reading file completed\n\n\n")
    # centroids = output_centroids(dataset, k, delim)
    # output_partitions(dataset, k)
    # print(f"Euclidean Distance: {calculate_euclidean_distance(dataset[1], dataset[1])}")
    # ssd = calculate_sum_of_squared_distance(dataset, centroids, random_centroid=True)
    # apd = calculate_pairwise_distance(dataset)
    # print(f"Sum of Squared Distance: {ssd}")
    # print(f"Average Pairwise Distance: {apd}")
    # nearest_neighbor_index, nearest_neighbor = find_nearest_neighbor(dataset[0], dataset)
    # print(f"Nearest neighbor for point {dataset[301]} is {nearest_neighbor}")

    # optimal_partition = evaluate_datapoint_centroid(dataset, centroids)
    # calculate_centroid_sse(labelled_data_file_path, centroids_file_path, delim)
    kMeans(labelled_data_file_path, centroids_file_path, delim)
if __name__ == "__main__":
    main()