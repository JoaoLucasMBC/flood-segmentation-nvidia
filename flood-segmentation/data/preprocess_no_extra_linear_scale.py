import os
import numpy as np
import rasterio
from PIL import Image

from dotenv import load_dotenv
from pathlib import Path


def convert_band_to_linear(band):
    linear_band = 10 ** (band / 10)
    return (255 * linear_band).astype(np.uint8)


def preprocess_image(image_path, output_dir):
    """
    Preprocess the image at image_path and save the preprocessed bands
    to the output_dir.
    """
    
    with rasterio.open(image_path) as src:
        vv = src.read(1)
        vh = src.read(2)
    
    # Normalize the bands
    vv_norm = convert_band_to_linear(vv)
    vh_norm = convert_band_to_linear(vh)
    extra_band = convert_band_to_linear(vv - vh)

    # Make RGB image
    rgb_image = np.stack([vv_norm, vh_norm, extra_band], axis=-1)

    # Save the rgb image in the output_dir
    image_name = '_'.join(os.path.splitext(os.path.basename(image_path))[0].split("_")[0:2])

    output_path = os.path.join(output_dir, f"{image_name}.png")

    Image.fromarray(rgb_image).save(output_path)
    print(f"Saved image to {output_path}")


def main():
    load_dotenv(dotenv_path=Path('../config/.env'))

    # Preprocess the images in the 'data' directory
    data_dir = os.path.join(".", f"v{os.environ['VERSION']}", "S1Hand")
    output_dir = os.path.join(".", f"v{os.environ['VERSION']}", "ProcessedS1")

    os.makedirs(output_dir, exist_ok=True)

    for image_name in os.listdir(data_dir):
        image_path = os.path.join(data_dir, image_name)
        preprocess_image(image_path, output_dir)


if __name__ == "__main__":
    main()
