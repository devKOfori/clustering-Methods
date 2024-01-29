import numpy as np
import math
import random
import os

file_path = "/home/swine/Documents/UEF Courses/Y1_S2_P1/Clustering Methods/Exercises/Exercise 1/Task & Dataset/Ex1 Dataset/s1/s1.txt"
file_name = "s1.txt"

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

def read_data(file_path: str, delim: str=""):
    """
    This function loads data from a text file
    and returns a numpy array as a dataset containing
    all the loaded data
    """
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

def calculate_sum_of_squared_distance(dataset, centroids):
    '''
    This function calculate the sum of squared distance 
    between each data point and a randomly chosen centroid
    '''
    sum_of_squared_distance = 0
    random_centroid = np.random.choice(centroids.shape[0])
    for data in dataset:
        sum_of_squared_distance += (calculate_euclidean_distance(data, random_centroid))**2
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


def main():
    k = int(input('How many partitions do you want to create? '))
    delim = "\t"
    print("Reading file...")
    dataset = read_data(file_path, delim)
    print("Reading file completed\n\n\n")
    centroids = output_centroids(dataset, k, delim)
    output_partitions(dataset, k)
    # print(f"Euclidean Distance: {calculate_euclidean_distance(dataset[1], dataset[1])}")
    ssd = calculate_sum_of_squared_distance(dataset, centroids)
    apd = calculate_pairwise_distance(dataset)
    print(f"Sum of Squared Distance: {ssd}")
    print(f"Average Pairwise Distance: {apd}")
    
if __name__ == "__main__":
    main()