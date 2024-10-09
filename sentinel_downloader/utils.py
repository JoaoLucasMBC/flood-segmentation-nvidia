import math
import os

def create_dir(save_dir):
        # create /data directory if it does not exist
        if not os.path.isdir("./data"):
            os.makedirs("./data")

        # create directory inside data if it does not exist, if exists return error
        if not os.path.isdir(f".{save_dir}"):
            os.makedirs(f".{save_dir}")
        else:
            raise ValueError("Directory already exists inside /data")
        
        os.makedirs(f"{save_dir}/tif", exist=True)
        os.makedirs(f"{save_dir}/png", exist=True)


def divide_big_area(coords, step):
        # Create list to hold smaller bounding boxes
        bbox_list = []

        # Calculate the number of tiles (smaller bounding boxes)
        number_boxes_lat = math.ceil(abs(coords[0] - coords[2]) / step) # rows
        number_boxes_lon = math.ceil(abs(coords[1] - coords[3]) / step) # columns

        # Create smaller bounding boxes
        for i in range(number_boxes_lat):
            for j in range(number_boxes_lon):
                bbox = [coords[0] + i * step, coords[1] + j * step, coords[0] + (i + 1) * step, coords[1] + (j + 1) * step]
                bbox_list.append(bbox)

        return bbox_list

