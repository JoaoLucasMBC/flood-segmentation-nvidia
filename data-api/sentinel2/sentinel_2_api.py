import os
import ast
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from datetime import datetime, timedelta

from PIL import Image
from dotenv import load_dotenv
from sentinel_2_error_handling import Sentinel2ErrorHandler
from sentinelhub import DataCollection, CRS, BBox, MimeType, SentinelHubRequest, SHConfig

class Sentinel2Api:

    def __init__(self):

        load_dotenv()

        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET = os.getenv("CLIENT_SECRET")

        self.config = SHConfig()
        if CLIENT_ID and CLIENT_SECRET:
            self.config.sh_client_id = CLIENT_ID
            self.config.sh_client_secret = CLIENT_SECRET

    @staticmethod
    def count_cloud_pixels(image):
        cloud_pixels = np.all(image == 255, axis=-1)
        return np.sum(cloud_pixels)
    
    @staticmethod
    def scale_and_clip_image(image, factor=3.5 / 255, clip_range=(0, 1)):
        rgb = image[..., :3]
        alpha = image[..., 3:]
        
        scaled_rgb = np.clip(rgb * factor, *clip_range)
        scaled_rgb = (scaled_rgb * 255).astype(np.uint8)
        
        return np.concatenate([scaled_rgb, alpha], axis=-1)
    
    @staticmethod
    def load_evalscript(script_name):
        try:
            script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'evalscripts', script_name + ".js"))
            with open(script_path, 'r') as file:
                evalscript = file.read()
        except:
            raise ValueError(f"Invalid evalscript name: {script_name}.\n 
                             Please make sure the evalscript exists in the 'evalscripts' folder.")
        return evalscript
    
    @staticmethod
    def divide_big_area(full_area_nw, full_area_se, latitude_step, longitude_step):

        latitude_direction = 1 if full_area_nw[0] < full_area_se[0] else -1
        longitude_direction = 1 if full_area_nw[1] < full_area_se[1] else -1

        latitude_step *= latitude_direction
        longitude_step *= longitude_direction

        next_image_nw, next_image_se = full_area_nw, (round(full_area_nw[0] + latitude_step, 4), round(full_area_nw[1] + longitude_step, 4))

        coordinates = []
        i = 0

        while next_image_se[0] >= full_area_se[0]:

            coordinates.append([])

            while next_image_se[1] <= full_area_se[1]:

                coordinates[i].append((next_image_nw[0], next_image_nw[1], next_image_se[0], next_image_se[1]))

                next_image_nw = (next_image_nw[0], round(next_image_nw[1] + longitude_step, 4))
                next_image_se = (next_image_se[0], round(next_image_se[1] + longitude_step, 4))

            next_image_nw = (round(next_image_nw[0] + latitude_step, 4), full_area_nw[1])
            next_image_se = (round(next_image_se[0] + latitude_step, 4), round(full_area_nw[1]+longitude_step, 4))

            i+=1
        return coordinates
    
    @staticmethod
    def collect_image(bbox, evalscript, time_interval, resolution, config):
        request = SentinelHubRequest(
            evalscript=evalscript,
            input_data=[
                SentinelHubRequest.input_data(
                    data_collection=DataCollection.SENTINEL2_L2A,
                    time_interval=time_interval
                )
            ],
            responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
            bbox=bbox,
            size=resolution,
            config=config
        )
        return request.get_data()[0]
    
    @staticmethod
    def collect_best_image(bbox, evalscript, time_interval, resolution, config):
        time_interval = (datetime.strptime(time_interval[0], "%Y-%m-%d"), datetime.strptime(time_interval[1], "%Y-%m-%d"))

        date_list = [(time_interval[0] + timedelta(days=x)).isoformat() for x in range(0, (time_interval[1] - time_interval[0]).days + 1, 2)]
        
        best_time_interval = None
        best_cloud_pixels = float("inf")

        cloud_evalscript = Sentinel2Api.load_evalscript("cloud")

        for i in range(len(date_list) - 1):
            time_interval = (date_list[i], date_list[i + 1])

            image = Sentinel2Api.collect_image(bbox, cloud_evalscript, time_interval, resolution, config)
            cloud_pixels = Sentinel2Api.count_cloud_pixels(image)

            if cloud_pixels < best_cloud_pixels:
                best_time_interval = time_interval
                best_cloud_pixels = cloud_pixels

            if best_cloud_pixels == 0:
                break
        
        return Sentinel2Api.collect_image(bbox, evalscript, best_time_interval, resolution, config)

    
def main():
    parser = ArgumentParser(description="Sentinel-2 API")
    
    parser.add_argument("-c", "--coords", type=str, required=True)
    parser.add_argument("-ev", "--evalscript", type=str, required=True)
    parser.add_argument("-t", "--time-interval", type=str, required=True)

    parser.add_argument("-res", "--resolution", type=int, required=False, default=512)
    parser.add_argument("-s", "--save_dir", type=str, required=False, default="")
    parser.add_argument("-n", "--name", type=str, required=False)
    parser.add_argument("-st", "--step", type=float, required=False, default=0.05)
    parser.add_argument("-cr", "--cloud-removal", type=bool, required=False, default=False)
    
    args = parser.parse_args()

    try:
        coords = ast.literal_eval(args.coords)
        Sentinel2ErrorHandler.coordinate_error_handling(coords, args.step)

        evalscript = Sentinel2Api.load_evalscript(args.evalscript)

        time_interval = ast.literal_eval(args.time_interval)
        Sentinel2ErrorHandler.time_interval_error_handling(time_interval)

        if args.resolution <= 128 or args.resolution > 2048:
            raise ValueError("Invalid resolution, it must be between 1 and 2048.")
        resolution = (args.resolution, args.resolution)

        name = ""
        if args.name:
            name = args.name
            if name[-4] != ".png":
                name += ".png" 

        save_dir = args.save_dir
        if save_dir and save_dir[-1] != "/":
            save_dir += "/"
        if not os.path.isdir(f".{save_dir}"):
            os.makedirs(f".{save_dir}")

        sentinel2 = Sentinel2Api()
        if abs(abs(coords[0]) - abs(coords[2])) > 0.15:
            coords = sentinel2.divide_big_area((coords[0], coords[1]), (coords[1], coords[2]), args.step, args.step)
        else :
            coords = [coords]

        if not args.cloud_removal:
            for coord in coords:
                image = sentinel2.collect_image(BBox(coord, crs=CRS.WGS84), evalscript, time_interval, resolution, sentinel2.config)
                if len(coords) == 1:
                    Image.fromarray(image).save(f".{save_dir}/{args.name}")
                else: Image.fromarray(image).save(f".{save_dir}/{coords[0]}_{coords[1]}_{coords[2]}_{coords[3]}.png")
        else:
            for coord in coords:
                image = sentinel2.collect_best_image(BBox(coord, crs=CRS.WGS84), evalscript, time_interval, resolution, sentinel2.config)
                if len(coords) == 1:
                    Image.fromarray(image).save(f".{save_dir}/{args.name}")
                else: Image.fromarray(image).save(f".{save_dir}/{coords[0]}_{coords[1]}_{coords[2]}_{coords[3]}.png")

    except Exception as e:

        print(e)
        print("Invalid input")


if __name__ == "__main__":
    main()