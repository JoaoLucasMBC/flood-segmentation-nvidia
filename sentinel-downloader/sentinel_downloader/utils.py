import math
import os
import sys

def create_dir(save_dir, satellite):
        # create /output directory if it does not exist
        if not os.path.isdir(f"{os.getcwd()}/output"):
            os.makedirs(f"{os.getcwd()}/output")
            os.chmod(f"{os.getcwd()}/output", 0o777)

        # create directory inside output if it does not exist, if exists return error
        if os.path.exists(f"{save_dir}"):
            raise ValueError("Directory already exists, please choose a different name.")
        else:
            os.makedirs(f"{save_dir}")
            os.chmod(f"{save_dir}", 0o777)

        if satellite == "sentinel1":
            os.makedirs(f"{save_dir}/sentinel1")
            os.makedirs(f"{save_dir}/sentinel1/tif")
        elif satellite == "sentinel2":
            os.makedirs(f"{save_dir}/sentinel2")
        else:
            os.makedirs(f"{save_dir}/sentinel1")
            os.makedirs(f"{save_dir}/sentinel1/tif")
            os.makedirs(f"{save_dir}/sentinel2")
    
import math

def divide_big_area(coords, step):
    bbox_list = []
    min_lon, min_lat, max_lon, max_lat = coords

    number_boxes_lat = math.ceil(abs(max_lat - min_lat) / step)  # rows (latitudinal direction)
    number_boxes_lon = math.ceil(abs(max_lon - min_lon) / step)  # columns (longitudinal direction)

    for i in range(number_boxes_lat):
        row_bboxs = []
        for j in range(number_boxes_lon):
            tile_min_lat = min_lat + i * step
            tile_max_lat = min_lat + (i + 1) * step
            tile_min_lon = min_lon + j * step
            tile_max_lon = min_lon + (j + 1) * step

            bbox = (tile_min_lon, tile_min_lat, tile_max_lon, tile_max_lat)
            row_bboxs.append(bbox)

        bbox_list.append(row_bboxs)

    new_expanded_bbox_cords = (min_lat + number_boxes_lat * step,
                               min_lon,
                                min_lat,
                                min_lon + number_boxes_lon * step)

    return bbox_list, new_expanded_bbox_cords


def load_evalscript(script_name):
        try:
            script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'evalscripts', script_name + ".js"))
            with open(script_path, 'r') as file:
                evalscript = file.read()
        except:
            raise ValueError(f"Invalid evalscript name: {script_name}.\n Please make sure the evalscript exists in the 'evalscripts' folder.")
        return evalscript

class SuppressPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout.close()
        sys.stdout = self._original_stdout