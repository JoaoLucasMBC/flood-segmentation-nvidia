import os
import ast
from argparse import ArgumentParser

from PIL import Image
from dotenv import load_dotenv
from sentinel_2_api import Sentinel2Api
from sentinel_2_error_handling import Sentinel2ErrorHandler
from sentinelhub import CRS, BBox, SHConfig


def main():
    load_dotenv()
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    config = SHConfig()
    if CLIENT_ID and CLIENT_SECRET:
        config.sh_client_id = CLIENT_ID
        config.sh_client_secret = CLIENT_SECRET
    
    parser = ArgumentParser(description="Sentinel-2 API")
    parser.add_argument("-c", "--coords", type=str, required=True)
    parser.add_argument("-ev", "--evalscript", type=str, required=True)
    parser.add_argument("-t", "--time-interval", type=str, required=True)

    parser.add_argument("-res", "--resolution", type=int, required=False, default=512)
    parser.add_argument("-s", "--save_dir", type=str, required=False, default="/")
    parser.add_argument("-n", "--name", type=str, required=False)
    parser.add_argument("-st", "--step", type=float, required=False, default=0.05)
    parser.add_argument("-cr", "--cloud-removal", type=bool, required=False, default=False)

    
    args = parser.parse_args()

    try:
        # Error Handling and Input Validation
        coords = ast.literal_eval(args.coords)
        Sentinel2ErrorHandler.coordinate_error_handling(coords, args.step)
        print(f"Coordinate format valid: {coords}")

        evalscript = Sentinel2Api.load_evalscript(args.evalscript)
        print(f"Evalscript loaded: {args.evalscript}")

        time_interval = ast.literal_eval(args.time_interval)
        Sentinel2ErrorHandler.time_interval_error_handling(time_interval)
        print(f"Time interval valid: {time_interval}")

        if args.resolution <= 128 or args.resolution > 2048:
            raise ValueError("Invalid resolution, it must be between 128 and 2048.")
        resolution = (args.resolution, args.resolution)
        print(f"Resolution valid: {resolution}")

        name = ""
        if args.name:
            name = args.name
            if name[-4] != ".png":
                name += ".png" 
            print(f"Filename valid: {name}")

        save_dir = args.save_dir
        if not os.path.isdir(f".{save_dir}"):
            os.makedirs(f".{save_dir}")
        print(f"Save directory valid: {save_dir}")

        # Coordinate Processing
        sentinel2 = Sentinel2Api()
        if abs(abs(coords[0]) - abs(coords[2])) > 0.15:
            coords = sentinel2.divide_big_area((coords[0], coords[1]), (coords[2], coords[3]), args.step, args.step)        
        else:
            coords = [coords]
        print(f"Images to be captured: {len(coords)}")

        if len(coords) > 1 and abs(abs(coords[0][1]) - abs(coords[0][3])) < 0.05:
            raise ValueError("Invalid step value, the result of the division is too small.")

        # Image Collection
        if not args.cloud_removal:
            for coord in coords:
                image = sentinel2.collect_image(BBox([coord[1], coord[0], coord[3], coord[2]], crs=CRS.WGS84), evalscript, time_interval, resolution, config)
                if len(coords) == 1 and args.name:
                    Image.fromarray(image).save(f".{save_dir}/{args.name}")
                else: Image.fromarray(image).save(f".{save_dir}/{coord[0]}_{coord[1]}_{coord[2]}_{coord[3]}.png")
        else:
            for coord in coords:
                image = sentinel2.collect_best_image(BBox([coord[1], coord[0], coord[3], coord[2]], crs=CRS.WGS84), evalscript, time_interval, resolution, config)
                if len(coords) == 1 and args.name:
                    Image.fromarray(image).save(f".{save_dir}/{args.name}")
                else: Image.fromarray(image).save(f".{save_dir}/{coord[0]}_{coord[1]}_{coord[2]}_{coord[3]}.png")

    except Exception as e:
        print(e)
        print("Invalid input")


if __name__ == "__main__":
    main()