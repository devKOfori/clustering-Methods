import random
import math

dataset = []

class DataPoint:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return f'({self.x}, {self.y})'
    
    def __repr__(self):
        return f'({self.x}, {self.y})'
    
    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return x, y


def read_data(file_path: str, delim=''):
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            line_content = line.strip()
            line_content = line_content.replace('\ufeff', '') # The '\ufeff' is the Unicode character for the byte order mark (BOM), which sometimes appears at the beginning of UTF-8 encoded files.
            # line_container = line_content.split(delim)
            line_container = [cord.strip() for cord in line_content.split(delim) if cord]
            # print(line_container)
            if line_content and len(line_container) >= 2:
                try:
                    # print(line_container[0].strip(), line_container[0])
                    x, y = int(line_container[0].strip()), int(line_container[1].strip())
                    data_point = DataPoint(x, y)
                    dataset.append(data_point)
                except ValueError as e:
                    print(f"Error converting line {line_number} to integers: {e}")
                    print(f"Problematic line: {line_content}")
    return dataset

def output_centroids(k, dataset):
    centroids = random.sample(dataset, k)
    with open('centroid.txt', 'a') as file:
        for point in centroids:
            output_line = f'{point.x}    {point.y} \n'
            file.write(output_line)
    return centroids

def output_partitions(k, dataset):
    with open('partition.txt', 'a') as file:
        for point in dataset:
            partition = random.randint(1, k)
            output_line = str(partition) + '\n'
            file.write(output_line)

def calculate_euclidean_distance(dp1, dp2):
    difference_tuple = dp1 - dp2
    x_diff, y_diff = difference_tuple
    euclidean_distance = math.sqrt((x_diff**2) + (y_diff**2))
    return euclidean_distance

def calculate_sum_of_squared_error(dataset, centroids_list):
    sum_of_squared_error = 0
    random_centroid = random.choice(centroids_list)
    for datapoint in dataset:
        difference_tuple = datapoint - random_centroid
        x_diff, y_diff = difference_tuple
        sum_of_squared_error += x_diff**2 + y_diff**2
    return sum_of_squared_error

def pairwise_distance(dataset):
    total_pairwise_distance = 0
    N = len(dataset)
    for i in range(0, N-1):
        for j in range(i+1, N-1):
            euclidean_dist = calculate_euclidean_distance(dataset[i], dataset[j])
            total_pairwise_distance += euclidean_dist
    average_pairwise_distance = total_pairwise_distance / N
    print(f'The average distance between all data points is {average_pairwise_distance}')

def main():
    k = int(input('How many partitions do you want to create? '))
    delim = ' ' * 4
    file_path = '/home/swine/Documents/UEF Courses/Y1_S2_P1/Ex1 Dataset/s1/s1.txt'
    print('Reading file...')
    dataset = read_data(file_path, delim)
    print('Reading file completed\n\n\n')
    centroids = output_centroids(k, dataset)
    output_partitions(k, dataset)
    print(f'The sum of squared error is {calculate_sum_of_squared_error(dataset, centroids)}')

if __name__ == '__main__':
    main()