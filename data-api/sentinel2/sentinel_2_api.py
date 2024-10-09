import os
import numpy as np
from datetime import datetime, timedelta

from sentinelhub import DataCollection, MimeType, SentinelHubRequest

class Sentinel2Api:

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
            raise ValueError(f"Invalid evalscript name: {script_name}.\n Please make sure the evalscript exists in the 'evalscripts' folder.")
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


            while next_image_se[1] <= full_area_se[1]:

                coordinates.append((next_image_nw[0], next_image_nw[1], next_image_se[0], next_image_se[1]))

                next_image_nw = (next_image_nw[0], round(next_image_nw[1] + longitude_step, 4))
                next_image_se = (next_image_se[0], round(next_image_se[1] + longitude_step, 4))

            next_image_nw = (round(next_image_nw[0] + latitude_step, 4), full_area_nw[1])
            next_image_se = (round(next_image_se[0] + latitude_step, 4), round(full_area_nw[1]+longitude_step, 4))

            i+=1
        return coordinates
    
    @staticmethod
    def scale_and_clip_image(image, factor=3.5 / 255, clip_range=(0, 1)):
        rgb = image[..., :3]
        alpha = image[..., 3:]
        
        scaled_rgb = np.clip(rgb * factor, *clip_range)
        scaled_rgb = (scaled_rgb * 255).astype(np.uint8)
        
        return np.concatenate([scaled_rgb, alpha], axis=-1)
    
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

        date_list = [(time_interval[0] + timedelta(days=x)).isoformat() for x in range(0, (time_interval[1] - time_interval[0]).days + 1, 5)]
        
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