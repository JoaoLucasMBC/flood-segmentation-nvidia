from argparse import ArgumentParser
from sentinel_downloader.sentinel1 import Sentinel1
from sentinel_downloader.sentinel2 import Sentinel2
from sentinel_downloader.utils import divide_big_area, create_dir, load_evalscript
from sentinel_downloader.error_handler import *
from sentinel_downloader.image_processing import process_image, normalize, png_conversion
import ast
from datetime import datetime
import shutil

class CLI():
    def __init__(self, cli_args):
        self.cli_args = cli_args
        self.args = self.parse_args()

    def parse_args(self):
        parser = ArgumentParser(description="Sentinel-Downloader API")
        # Choose between sentinel 1 and sentinel 2
        parser.add_argument("-s", "--satellite", type=str, required=True)

        # All satellites
        parser.add_argument("-c", "--coords", type=str, required=True)
        parser.add_argument("-t", "--time-interval", type=str, required=True)
        parser.add_argument("-r", "--resolution", type=int, required=False, default=512)
        parser.add_argument("-sd", "--save-dir", type=str, required=False, default=f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}")
        parser.add_argument("-f", "--filename", type=str, required=False, default="file")

        # Only for sentinel 2
        parser.add_argument("-ev", "--evalscript", type=str, required=False, default="rgb")
        parser.add_argument("-cr", "--cloud-removal", type=bool, required=False, default=False)

        return parser.parse_args(self.cli_args)

    def run(self):
        save_dir_created = False

        try:
            # Error handling
            satellite = satellite_error_handling(self.args.satellite)

            coords = ast.literal_eval(self.args.coords)
            coordinate_error_handling(coords)
            coords = (coords[1], coords[0], coords[3], coords[2])

            time_interval = ast.literal_eval(self.args.time_interval)
            time_interval_error_handling(time_interval)

            resolution_error_handling(self.args.resolution, satellite)
            resolution = (self.args.resolution, self.args.resolution)
            step = 0.0459937425 * self.args.resolution / 512

            save_dir_error_handling(self.args.save_dir)
            save_dir = f"./output/{self.args.save_dir}"
            create_dir(save_dir, satellite)
            save_dir_created = True

            filename_error_handling(self.args.filename)
            filename = self.args.filename

            if satellite == "sentinel2" or satellite == "both":
                evalscript = self.args.evalscript
                evalscript_error_handling(evalscript)
                evalscript = load_evalscript(evalscript)

                cloud_removal = self.args.cloud_removal
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
    cli = CLI(sys.argv[1:])
    cli.run()