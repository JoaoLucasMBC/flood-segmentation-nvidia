import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

from sentinel import Sentinel
from sentinelhub import DataCollection, MimeType, SentinelHubRequest, SHConfig

class Sentinel2Api(Sentinel):

    def __init__(self):
        load_dotenv()
        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET = os.getenv("CLIENT_SECRET")
        config = SHConfig()
        if CLIENT_ID and CLIENT_SECRET:
            config.sh_client_id = CLIENT_ID
            config.sh_client_secret = CLIENT_SECRET

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