import os
from model import DataPoint
import helpers

BASE_DATA_DIR = r"C:\Users\Eben Ofori-Mensah\Documents\IMPIT\Y1S2P1\ClusteringMethods\Data_Files"
dataset_name = "s1.txt"

file_path = os.path.join(BASE_DATA_DIR, dataset_name)
delim = "    "

def remove_byte_order_mark(file_path: str, export_file_name: str = "processed_data.txt"):
    """
    This function processes the original dataset
    by removing the Byte Order Mark from the data
    and outputs the processed data into a new file
    """

    try:
        with open(file_path, "r", encoding="utf-8-sig") as file:
            lines = file.readlines()
            lines[0] = lines[0].lstrip("\ufeff") #remove byte order mark
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return
    
    try:
        with open(export_file_name, "w") as file:
            file.writelines(lines)
        print(f"Data processed successfully. Saved as '{export_file_name}'.")
    except Exception as e:
        print(f"An error occurred while saving the processed data: {e}")



def load_data(file_path: str = file_path, delim: str=delim, remove_bom: bool = True, export_file_name: str = "processed_data.txt"):
    """
    This function loads data from a text file
    and returns a list of DataPoint objects.
    """
    dataset = []
    if remove_bom and not os.path.exists(export_file_name):
        remove_byte_order_mark(file_path, export_file_name)
    try:
        with open(export_file_name, "r", encoding="utf-8") as file:
            for index, line in enumerate(file, start=1):
                if line and len(line) > 2:
                    data = []
                    obs_no_padding = line.strip()
                    line_arr = obs_no_padding.split(delim)
                    data = [int(d.strip()) for d in line_arr]
                    dataset.append(DataPoint(data))                    
            # lines = file.readlines()            
            # dataset = [line.strip().split(delim) for line in lines if line.isdigit]
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e} - {index}")
    else:
        print("Data loaded successfully.")
        return dataset
    
if __name__ == "__main__":
    ds = load_data()
    # helpers.generate_centroids(15, ds)
    helpers.generate_data_partitions(15, ds)
    # print(ds)
    # print(ds[4998] + ds[4999])
    # print(len(ds))