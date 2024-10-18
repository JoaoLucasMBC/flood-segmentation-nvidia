from sentinel_downloader.sentinel import Sentinel
from sentinel_downloader.image_processing import scale_and_clip_image, count_obstructed_pixels
from sentinel_downloader.utils import load_evalscript
from sentinelhub import DataCollection, MimeType, SentinelHubRequest, SHConfig, BBox, CRS
import os
from PIL import Image
from dotenv import load_dotenv
from datetime import datetime, timedelta
from tqdm import tqdm

class Sentinel2(Sentinel):

    def __init__(self):
        load_dotenv()
        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET = os.getenv("CLIENT_SECRET")
        self.config = SHConfig()
        if CLIENT_ID and CLIENT_SECRET:
            self.config.sh_client_id = CLIENT_ID
            self.config.sh_client_secret = CLIENT_SECRET

    def sentinelhub_request(self, evalscript, data_collection, time_interval, bbox, resolution):
        request = SentinelHubRequest(
            evalscript=evalscript,
            input_data=[
                SentinelHubRequest.input_data(
                    data_collection=data_collection,
                    time_interval=time_interval
                )
            ],
            responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
            bbox=bbox,
            size=resolution,
            config=self.config
        )
        return request.get_data()[0]

    def collect_image(self, list_coordinates, evalscript, time_interval, resolution, output_folder, filename):

        with tqdm(total=len(list_coordinates) * len(list_coordinates[0]), desc="Downloading Sentinel2 Tiles", dynamic_ncols=True) as pbar:
            for i, coords in enumerate(list_coordinates):
                for j, coord in enumerate(coords): 
                    image = self.sentinelhub_request(evalscript, DataCollection.SENTINEL2_L2A, time_interval, BBox(coord, CRS.WGS84), resolution)
                    image = scale_and_clip_image(image)
                    output_filename = os.path.join(f"{output_folder}/sentinel2", f'{filename}_{i}_{j}.png')
                    Image.fromarray(image).save(output_filename)

                    pbar.update(1)
    
    def collect_best_image(self, list_coordinates, evalscript, time_interval, resolution, output_folder, filename):
        time_interval = (datetime.strptime(time_interval[0], "%Y-%m-%d"), datetime.strptime(time_interval[1], "%Y-%m-%d"))

        date_list = [(time_interval[0] + timedelta(days=x)).strftime('%Y-%m-%d') for x in range(0, (time_interval[1] - time_interval[0]).days + 1, 5)]
        
        cloud_evalscript = load_evalscript("cloud")

        with tqdm(total=len(list_coordinates) * len(list_coordinates[0]), desc="Downloading Sentinel2 Tiles", dynamic_ncols=True) as pbar:
            for i, coords in enumerate(list_coordinates):

                best_time_interval = None
                best_cloud_pixels = float("inf")

                for j, coord in enumerate(coords): 
                    for d in range(len(date_list) - 1):
                        
                        time_interval = (date_list[d], date_list[d + 1])

                        image = self.sentinelhub_request(cloud_evalscript, DataCollection.SENTINEL2_L2A, time_interval, BBox(coord, CRS.WGS84), (512,512))
                        obstructed_pixels = count_obstructed_pixels(image)

                        if obstructed_pixels < best_cloud_pixels:
                            best_time_interval = time_interval
                            best_cloud_pixels = obstructed_pixels
                            
                        if best_cloud_pixels == 0:
                            break

                    image = self.sentinelhub_request(evalscript, DataCollection.SENTINEL2_L2A, best_time_interval, BBox(coord, CRS.WGS84), resolution)
                    image = scale_and_clip_image(image)
                    output_filename = os.path.join(f"{output_folder}/sentinel2", f'{filename}_{i}_{j}.png')
                    Image.fromarray(image).save(output_filename)

                    pbar.update(1)