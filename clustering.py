import random

dataset = []

class DataPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'
    
    def __repr__(self):
        return f'({self.x}, {self.y})'


def read_data(file_path: str, delim=''):
    with open(file_path, 'r') as file:
        for line in file:
            line_content = line.strip()
            line_container = line_content.split(delim)
            x, y = line_container[0], line_container[1]
            data_point = DataPoint(x, y)
            dataset.append(data_point)
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


def main():
    delim = ' ' * 4
    file_path = '/home/swine/Documents/UEF Courses/Y1_S2_P1/Ex1 Dataset/s1/s1.txt'
    print('Reading file...')
    dataset = read_data(file_path, delim)
    print('Reading file completed\n\n\n')
    output_centroids(15, dataset)
    output_partitions(15, dataset)

if __name__ == '__main__':
    main()