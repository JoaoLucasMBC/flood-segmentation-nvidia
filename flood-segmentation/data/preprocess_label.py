import os
import numpy as np
import rasterio
from PIL import Image

from dotenv import load_dotenv
from pathlib import Path


def preprocess_image(image_path, output_dir):
    """
    Preprocess the image at image_path and save the preprocessed bands
    to the output_dir.
    """
    
    with rasterio.open(image_path) as src:
        label = src.read()
    
    # Clip the label to 0 and 1
    label = np.clip(label, 0, 1) * 255

    # Save the label in the output_dir
    image_name = os.path.splitext(os.path.basename(image_path))[0]

    output_path = os.path.join(output_dir, f"{image_name.split('_LabelHand')[0]}.png")

    Image.fromarray(label[0].astype(np.uint8)).save(output_path)
    print(f"Saved image to {output_path}")


def main():
    load_dotenv(dotenv_path=Path('../config/.env'))

    # Preprocess the images in the 'data' directory
    data_dir = "./LabelHand"
    output_dir = os.path.join(os.environ["LOCAL_DATA_DIR"], "ProcessedLabelHand")

    os.makedirs(output_dir, exist_ok=True)

    for image_name in os.listdir(data_dir):
        image_path = os.path.join(data_dir, image_name)
        preprocess_image(image_path, output_dir)


if __name__ == "__main__":
    main()
