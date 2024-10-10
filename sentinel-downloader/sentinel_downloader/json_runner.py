from sentinel1 import Sentinel1
from sentinel2 import Sentinel2
from utils import divide_big_area, create_dir, load_evalscript
from error_handler import *
from image_processing import process_image, normalize, png_conversion
import ast
from datetime import datetime
import shutil
import json

def main():
    with open("../config.json") as f:
        data = json.load(f)
    
    
    if "satellite" not in data:
        raise ValueError("No satellite specified, please input a satellite (sentinel1, sentinel2, or both).")
    if "coords" not in data:
        raise ValueError("No coordinates specified, please input coordinates.")
    if "time_interval" not in data:
        raise ValueError("No time interval specified, please input a time interval.")
    
    satellite = data["satellite"]
    coords = data["coords"]
    time_interval = data["time_interval"]
    resolution = data["resolution"] if "resolution" in data else 512
    save_dir = data["save_dir"] if "save_dir" in data else f"{datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
    filename = data["filename"] if "filename" in data else "file"
    evalscript = data["evalscript"] if "evalscript" in data else "rgb"
    cloud_removal = data["cloud_removal"] if "cloud_removal" in data else False

    save_dir_created = False

    try:
        # Error handling

        # Check if satellite is valid
        satellite = satellite_error_handling(satellite)

        coords = ast.literal_eval(coords)
        coordinate_error_handling(coords)
        coords = (coords[1], coords[0], coords[3], coords[2])
        

        time_interval = ast.literal_eval(time_interval)
        time_interval_error_handling(time_interval)


        resolution_error_handling(resolution, satellite)
        resolution = (resolution, resolution)
        step = 0.0459937425 * resolution[0] / 512

        save_dir_error_handling(save_dir)
        # save_dir = os.path.join(os.getcwd(), "output", args.save_dir) --> change to users cwd?
        save_dir = f"./output/{save_dir}"
        create_dir(save_dir, satellite)
        save_dir_created = True

        filename_error_handling(filename)

        if satellite == "sentinel2" or satellite == "both":
            
            evalscript_error_handling(evalscript)
            evalscript = load_evalscript(evalscript)

            cloud_removal_error_handling(cloud_removal)

            sentinel2 = Sentinel2()

            if abs(abs(coords[0]) - abs(coords[2])) > step or abs(abs(coords[1]) - abs(coords[3])) > step:
                list_coords = divide_big_area(coords, step)
            else:
                list_coords = [[coords]]
            
            if cloud_removal:
                sentinel2.collect_best_image(list_coords, evalscript, time_interval, resolution, save_dir, filename)
            else:
                sentinel2.collect_image(list_coords, evalscript, time_interval, resolution, save_dir, filename)

        if satellite == "sentinel1" or satellite == "both":

            sentinel1 = Sentinel1()

            if abs(abs(coords[0]) - abs(coords[2])) > step or abs(abs(coords[1]) - abs(coords[3])) > step:
                list_coords = divide_big_area(coords, step)
            else:
                list_coords = [[coords]]

            sentinel1.collect_image(list_coords, coords, time_interval, save_dir, filename)

            vv_vh_list, filenames = process_image(save_dir)

            image_final_list = normalize(vv_vh_list)
            png_conversion(image_final_list, filenames, save_dir, resolution[0])
            
    except Exception as e:
        if save_dir_created:
            shutil.rmtree(save_dir)
        print(e)

if __name__ == "__main__":
    main()