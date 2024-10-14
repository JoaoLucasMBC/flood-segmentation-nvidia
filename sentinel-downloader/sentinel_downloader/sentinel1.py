import ee
import os
import geemap
from dotenv import load_dotenv
from sentinel_downloader.sentinel import Sentinel
from sentinel_downloader.utils import SuppressPrints

class Sentinel1(Sentinel):

    def __init__(self):
        load_dotenv()
        if os.getenv("KEY_FILE"):
            key_file = os.getenv("KEY_FILE")
        else:
            raise ValueError("Please set the environment variable KEY_FILE, it should be the JSON from your google API project that has the Earth Engine API enabled")

        credentials = ee.ServiceAccountCredentials(None, key_file)
        ee.Initialize(credentials)

    def collect_image(self, bbox_list, bbox_coords, time_interval, output_folder, filename):
        start_date = time_interval[0]
        end_date = time_interval[1]

        # Load the Sentinel-1 ImageCollection
        sentinel_1 = ee.ImageCollection('COPERNICUS/S1_GRD') \
            .filterBounds(ee.Geometry.Rectangle(bbox_coords)) \
            .filterDate(start_date, end_date) \
            .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \
            .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH')) \
            .filter(ee.Filter.eq('instrumentMode', 'IW')) \
            .mosaic()

        try:
            row = 0
            for column_ in bbox_list:
                col = 0
                for row_ in column_:
                    output_filename = os.path.join(f"{output_folder}/sentinel1/tif", f'{filename}_{row}_{col}.tif')
                    col += 1
                    tile_geom = ee.Geometry.Rectangle(row_)

                    
                    with SuppressPrints():
                        geemap.ee_export_image(
                            sentinel_1,
                            filename=output_filename,
                            scale=10,  
                            region=tile_geom,
                            file_per_band=False
                        )

                    if not os.path.exists(output_filename):
                        raise ValueError(f"Error downloading tile {row}, {col}: {e}")
                        
                row += 1
        except Exception as e:
            raise ValueError(f"Error downloading images from Sentinel 1, problems could include no available data for the given coordinates or time interval.")