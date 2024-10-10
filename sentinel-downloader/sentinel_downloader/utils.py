import math
import os

def create_dir(save_dir):
        # create /output directory if it does not exist
        if not os.path.isdir("./output"):
            os.makedirs("./output")
            os.chmod("./output", 0o777)

        # create directory inside output if it does not exist, if exists return error
        os.makedirs(f"{save_dir}")
        os.chmod(f"{save_dir}", 0o777)
        
        os.makedirs(f"{save_dir}/tif")
        os.makedirs(f"{save_dir}/png")

    
def divide_big_area(coords, step):
        # Create list to hold smaller bounding boxes
        bbox_list = []

        # Calculate the number of tiles (smaller bounding boxes)
        number_boxes_lat = math.ceil(abs(coords[0] - coords[2]) / step) # rows
        number_boxes_lon = math.ceil(abs(coords[1] - coords[3]) / step) # columns

        # Create smaller bounding boxes
        for i in range(number_boxes_lat):
            row_bbox = []
            for j in range(number_boxes_lon):
                bbox = (coords[0] + i * step, coords[1] + j * step, coords[0] + (i + 1) * step, coords[1] + (j + 1) * step)
                row_bbox.append(bbox)
            bbox_list.append(row_bbox)

        return bbox_list


def load_evalscript(script_name):
        try:
            script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'evalscripts', script_name + ".js"))
            with open(script_path, 'r') as file:
                evalscript = file.read()
        except:
            raise ValueError(f"Invalid evalscript name: {script_name}.\n Please make sure the evalscript exists in the 'evalscripts' folder.")
        return evalscript