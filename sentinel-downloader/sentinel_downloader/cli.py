from sentinel_downloader.sentinel1 import Sentinel1
from sentinel_downloader.sentinel2 import Sentinel2
from sentinel_downloader.utils import divide_big_area, create_dir, load_evalscript
from sentinel_downloader.error_handler import *
from sentinel_downloader.image_processing import process_image, normalize, png_conversion
import ast
from datetime import datetime
import shutil
import signal
from argparse import ArgumentParser
import os

class CLI():
    def __init__(self, cli_args=None):
        self.cli_args = cli_args
        self.args = self.parse_args()
        self.save_dir_created = False
        self.save_dir = None
        signal.signal(signal.SIGINT, self.cleanup_on_interrupt)

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
    
    def cleanup_on_interrupt(self, signum, frame):
        """Handle SIGINT"""
        if self.save_dir_created and os.path.exists(self.save_dir):
            shutil.rmtree(self.save_dir)
            print(f"\nDirectory {self.save_dir} has been removed due to interruption.")
        print("Process interrupted.")
        exit(0)

    def run(self):

        try:
            # Error handling
            satellite = satellite_error_handling(self.args.satellite)

            coords = ast.literal_eval(self.args.coords)
            coordinate_error_handling(coords)
            final_cords = coords
            coords = (coords[1], coords[2], coords[3], coords[0])

            time_interval = ast.literal_eval(self.args.time_interval)
            time_interval_error_handling(time_interval)

            resolution_error_handling(self.args.resolution, satellite)
            resolution = (self.args.resolution, self.args.resolution)
            step = 0.0459937425 * self.args.resolution / 512

            save_dir_error_handling(self.args.save_dir)
            self.save_dir = f"./output/{self.args.save_dir}"
            create_dir(self.save_dir, satellite)
            self.save_dir_created = True

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
                    list_coords, final_cords = divide_big_area(coords, step)
                    list_coords = list(reversed(list_coords))
                else:
                    list_coords = [[coords]]

                if cloud_removal:
                    sentinel2.collect_best_image(list_coords, evalscript, time_interval, resolution, self.save_dir, filename)
                else:
                    sentinel2.collect_image(list_coords, evalscript, time_interval, resolution, self.save_dir, filename)

            if satellite == "sentinel1" or satellite == "both":
                sentinel1 = Sentinel1()

                if abs(abs(coords[0]) - abs(coords[2])) > step or abs(abs(coords[1]) - abs(coords[3])) > step:
                    list_coords, final_cords = divide_big_area(coords, step)
                    list_coords = list(reversed(list_coords))
                else:
                    list_coords = [[coords]]

                sentinel1.collect_image(list_coords, coords, time_interval, self.save_dir, filename)

                vv_vh_list, filenames = process_image(self.save_dir)
                image_final_list = normalize(vv_vh_list)
                png_conversion(image_final_list, filenames, self.save_dir, resolution[0])
                
            with open(os.path.join(self.save_dir, "info.txt"), "w") as f:
                f.write(f"Satellite: {satellite}\n")
                f.write(f"Coordinates: {final_cords}\n")
                f.write(f"Time Interval: {time_interval}\n")
                f.write(f"Resolution: {resolution}\n")
                f.write(f"Save Directory: {self.save_dir}\n")
                f.write(f"Filename: {filename}\n")
                f.write(f"Evalscript: {evalscript}\n")
                f.write(f"Cloud Removal: {cloud_removal}\n")

        except Exception as e:
            if self.save_dir_created:
                shutil.rmtree(self.save_dir)
            print(e)

def main():
    cli = CLI()  
    cli.run()    

if __name__ == "__main__":
    main()