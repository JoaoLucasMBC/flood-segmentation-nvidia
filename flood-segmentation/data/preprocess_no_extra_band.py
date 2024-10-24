import os
import numpy as np
import rasterio
from PIL import Image

from dotenv import load_dotenv
from pathlib import Path


def normalize_band(band, min_val=-30, max_val=0):
    """
    Normalize the band values to the range [0, 255].
    Any value below min_val is clipped to min_val, and
    any value above max_val is clipped to max_val.
    """
    band = np.clip(band, min_val, max_val)
    band = (band - min_val) / (max_val - min_val)  # Scale to [0, 1]
    return (255 * band).astype(np.uint8)


def preprocess_image(image_path, output_dir):
    """
    Preprocess the image at image_path and save the preprocessed bands
    to the output_dir.
    """
    
    with rasterio.open(image_path) as src:
        vv = src.read(1)
        vh = src.read(2)
    
    # Normalize the bands
    vv_norm = normalize_band(vv)
    vh_norm = normalize_band(vh)

    # Make RGB image
    rgb_image = np.stack([vv_norm, vh_norm, np.zeros_like(vv_norm)], axis=-1)

    # Save the rgb image in the output_dir
    image_name = '_'.join(os.path.splitext(os.path.basename(image_path))[0].split("_")[0:2])

    output_path = os.path.join(output_dir, f"{image_name}.png")

    Image.fromarray(rgb_image).save(output_path)
    print(f"Saved image to {output_path}")


def main():
    load_dotenv(dotenv_path=Path('../config/.env'))

    # Preprocess the images in the 'data' directory
    data_dir = os.path.join(".", "S1Hand")
    output_dir = os.path.join(os.environ['LOCAL_DATA_DIR'], "ProcessedS1")

    os.makedirs(output_dir, exist_ok=True)

    for image_name in os.listdir(data_dir):
        image_path = os.path.join(data_dir, image_name)
        preprocess_image(image_path, output_dir)


if __name__ == "__main__":
    main()
