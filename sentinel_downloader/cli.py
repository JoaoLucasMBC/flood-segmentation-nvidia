from argparse import ArgumentParser
from sentinel_downloader.sentinel1 import Sentinel1
from sentinel_downloader.utils import divide_big_area, create_dir
from sentinel_downloader.errors import Sentinel1ErrorHandler
from sentinel_downloader.image_processing import process_image, normalize, png_conversion
import os
import ast
from datetime import datetime

def main():
    parser = ArgumentParser(description="Sentinel-1 API")
    parser.add_argument("-c", "--coords", type=str, required=True)
    parser.add_argument("-t", "--time-interval", type=str, required=True)

    parser.add_argument("-s", "--save_dir", type=str, required=False, default=f"{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    parser.add_argument("-n", "--name", type=str, required=False, default="file")
    parser.add_argument("-st", "--step", type=float, required=False, default=0.0459937425)
    args = parser.parse_args()

    try:
        coords = ast.literal_eval(args.coords)
        Sentinel1ErrorHandler.coordinate_error_handling(coords, args.step)

        time_interval = ast.literal_eval(args.time_interval)
        Sentinel1ErrorHandler.time_interval_error_handling(time_interval)

        # create /data directory if it does not exist
        if not os.path.isdir("./data"):
            os.makedirs("./data")

        # create directory inside data if it does not exist, if exists return error
        save_dir = f"/data/{args.save_dir}"

        create_dir(save_dir)
    
        sentinel1 = Sentinel1()

        if abs(abs(coords[0]) - abs(coords[2])) > 0.046 or abs(abs(coords[1]) - abs(coords[3])) > 0.046:
            list_coords = divide_big_area(coords, args.step)
        else:
            list_coords = [coords]

        sentinel1.collect_image(list_coords, coords, time_interval, save_dir)

        vv_vh_list, filenames = process_image(save_dir)

        image_final_list = normalize(vv_vh_list)

        png_conversion(image_final_list, filenames, save_dir)


        # Finish image collection here...

    except Exception as e:
        print(e)
        print("Invalid input")
