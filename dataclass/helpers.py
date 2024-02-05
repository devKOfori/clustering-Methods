import random

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
    with open('partition.txt', 'a') as file:
        for point in dataset:
            partition = random.randint(1, k)
            output_line = str(partition) + '\n'
            file.write(output_line)
