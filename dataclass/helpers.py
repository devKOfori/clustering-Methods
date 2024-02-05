import random
import math

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

def generate_data_partitions(k, dataset):
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

def calculate_sum_of_squared_error(dataset, centroids):
    sse = 0
    random_centroid = random.choice(centroids)
    print(f"Random Centroid: {random_centroid}")
    for data in dataset:
        sse += calculate_euclidean_distance(data, random_centroid)**2
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
    try:
        with open("optimal_partition.txt", "a") as file:
            for data in dataset:
                nearest_centroid_index, nearest_centroid = find_nearest_neighbor(data, centroids)
                print(nearest_centroid)
                data_centroids_list.append(nearest_centroid_index)
                output_line = str(nearest_centroid_index) 
                if data != dataset[-1]:
                    output_line += "\n"
                file.write(output_line)
    except Exception as e:
        print(f"An error occured while writing to 'optimal_partition.txt' {e}")
    else:
        # print(data_centroids_list)
        return data_centroids_list

        