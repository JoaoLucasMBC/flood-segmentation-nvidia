import os
import ast
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from argparse import ArgumentParser

from PIL import Image
from dotenv import load_dotenv
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
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'evalscripts', script_name + ".js"))
        with open(script_path, 'r') as file:
            evalscript = file.read()
        return evalscript
    
    @staticmethod
    def divide_big_area(full_area_nw, full_area_se, latitude_step, longitude_step):
        next_image_nw, next_image_se = full_area_nw, (round(full_area_nw[0] + latitude_step, 4), round(full_area_nw[1] + longitude_step, 4), full_area_nw[2])
        coordinates = []
        i = 0
        while next_image_se[0] >= full_area_se[0]:
            coordinates.append([])
            while next_image_se[1] <= full_area_se[1]:
                coordinates[i].append((next_image_nw, next_image_se)) 
                next_image_nw = (next_image_nw[0], round(next_image_nw[1] + longitude_step, 4), next_image_nw[2])
                next_image_se = (next_image_se[0], round(next_image_se[1] + longitude_step, 4), next_image_se[2])
            i+=1
            next_image_nw = (round(next_image_nw[0] + latitude_step, 4), full_area_nw[1], next_image_nw[2])
            next_image_se = (round(next_image_se[0] + latitude_step, 4), round(full_area_nw[1]+longitude_step, 4), next_image_se[2])
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

    
def main():
    parser = ArgumentParser(description="Sentinel-2 API")
    
    parser.add_argument("-c", "--coords", type=str, required=True)
    parser.add_argument("-ev", "--evalscript", type=str, required=True)
    parser.add_argument("-t", "--time-interval", type=str, required=True)

    parser.add_argument("-res", "--resolution", type=int, required=False)
    parser.add_argument("-s", "--save", type=str, required=False)
    parser.add_argument("-n", "--name", type=str, required=False)
    
    args = parser.parse_args()

    coords = ast.literal_eval(args.coords)
    bbox = BBox(coords, crs=CRS.WGS84)

    evalscript = Sentinel2Api.load_evalscript(args.evalscript)

    time_interval = ast.literal_eval(args.time_interval)

    name = args.name if args.name else f"{bbox.min_x}_{bbox.max_y}_{bbox.max_x}_{bbox.min_y}.png"

    resolution = (args.resolution, args.resolution) if args.resolution else (512, 512)
    save = args.save if args.save else ""

    sentinel2 = Sentinel2Api()
    image = sentinel2.collect_image(bbox, evalscript, time_interval, resolution, sentinel2.config)
    Image.fromarray(image).save(f".{save}/{name}")


if __name__ == "__main__":
    main()