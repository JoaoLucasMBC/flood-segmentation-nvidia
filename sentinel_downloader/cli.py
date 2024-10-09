from argparse import ArgumentParser
from sentinel1 import Sentinel1
from utils import divide_big_area, create_dir
from error_handler import *
from image_processing import process_image, normalize, png_conversion
import os
import ast
from datetime import datetime

def main():
    parser = ArgumentParser(description="Sentinel-Downloader API")
    # Choose between sentinel 1 and sentinel 2
    parser.add_argument("-s", "--satellite", type=str, required=True)

    # All satellites
    parser.add_argument("-c", "--coords", type=str, required=True)
    parser.add_argument("-t", "--time-interval", type=str, required=True)
    parser.add_argument("-r", "--resolution", type=int, required=False, default=512)
    parser.add_argument("-s", "--save-dir", type=str, required=False, default=f"{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    parser.add_argument("-f", "--filename", type=str, required=False, default="file")

    # Only for sentinel 2
    parser.add_argument("-ev", "--evalscript", type=str, required=False, default="rgb")
    parser.add_argument("-cr", "--cloud-removal", type=bool, required=False, default=False)

    args = parser.parse_args()

    try:
        # Error handling

        # Check if satellite is valid
        satellite = satellite_error_handling(args.satellite)

        coords = ast.literal_eval(args.coords)
        coordinate_error_handling(coords)

        time_interval = ast.literal_eval(args.time_interval)
        time_interval_error_handling(time_interval)


        resolution_error_handling(args.resolution, satellite)
        resolution = (args.resolution, args.resolution)
        step = 0.0459937425 * args.resolution / 512

        save_dir_error_handling(args.save_dir)
        save_dir = f"/output/{args.save_dir}"
        create_dir(save_dir)

        filename_error_handling(args.filename)
        filename = args.filename

        if satellite == "sentinel1":
    
            sentinel1 = Sentinel1()

            if abs(abs(coords[0]) - abs(coords[2])) > step or abs(abs(coords[1]) - abs(coords[3])) > step:
                list_coords = divide_big_area(coords, step)
            else:
                list_coords = [coords]

            sentinel1.collect_image(list_coords, coords, time_interval, save_dir, filename)

            vv_vh_list, filenames = process_image(save_dir)

            image_final_list = normalize(vv_vh_list)

            png_conversion(image_final_list, filenames, save_dir)

        elif satellite == "sentinel2":
            # Finish image collection here for sentinel 2
            pass

    except Exception as e:
        print(e)
        print("Invalid input")
