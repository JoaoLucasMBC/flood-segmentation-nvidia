import numpy as np
import os
import rasterio
import matplotlib.pyplot as plt

def normalize_band(band, min_val=-30, max_val=0):
    """
    Normalize the band values to the range [0, 255].
    Any value below min_val is clipped to min_val, and
    any value above max_val is clipped to max_val.
    """
    band = np.clip(band, min_val, max_val)
    band = (band - min_val) / (max_val - min_val)  # Scale to [0, 1]
    return (band * 255).astype(np.uint8)  # Scale to [0, 255]

def process_image(output_folder):
    # Initialize lists to hold VV and VH data for all files
    vv_vh_list = []
    filenames = []

    # Loop through all files in the output folder
    for filename in os.listdir(f"{output_folder}/sentinel1/tif"):
        if filename.endswith('.tif'):  # Check if the file is a .tif file
            tiff_file = os.path.join(f"{output_folder}/sentinel1/tif", filename)
            
            # Open the .tif file
            with rasterio.open(tiff_file) as dataset:
                # Read the VV (band 1) and VH (band 2) data
                vv_data = dataset.read(1)  # Band 1: VV
                vh_data = dataset.read(2)  # Band 2: VH
                
                # Append the data to the respective lists
                vv_vh_list.append([vv_data, vh_data])
                filenames.append(filename)

    return vv_vh_list, filenames

def normalize(vv_vh_list):
    image_final_list = []

    for i, (vv_data, vh_data) in enumerate(vv_vh_list):
        # Normalize the VV and VH bands
        vv_normalized = normalize_band(vv_data)
        vh_normalized = normalize_band(vh_data)

        # Calculate the difference between VV and VH bands
        difference_band = normalize_band(vv_data - vh_data)

        # Combine the normalized bands into an RGB image
        rgb_img = np.stack([vv_normalized, vh_normalized, difference_band], axis=-1)

        image_final_list.append(rgb_img)
    
    return image_final_list


def png_conversion(image_final_list, filenames, output_folder, crop_size):
    png_folder = f"{output_folder}/sentinel1"

    for i, image in enumerate(image_final_list):
        cropped_img = image[:crop_size, :crop_size]
        filename_without_extension = os.path.splitext(filenames[i])[0]
        output_path = os.path.join(f"{png_folder}", f"{filename_without_extension}.png")

        plt.imsave(output_path, cropped_img)

    tif_folder = f"{output_folder}/sentinel1/tif"
    for file in os.listdir(tif_folder):
        file_path = os.path.join(tif_folder, file)
        os.remove(file_path)
    os.rmdir(tif_folder)
    
def scale_and_clip_image(image, factor=3.5 / 255, clip_range=(0, 1)):
        rgb = image[..., :3]
        alpha = image[..., 3:]
        
        scaled_rgb = np.clip(rgb * factor, *clip_range)
        scaled_rgb = (scaled_rgb * 255).astype(np.uint8)
        
        return np.concatenate([scaled_rgb, alpha], axis=-1)

def count_obstructed_pixels(image):
        cloud_pixels = np.all(image == 255, axis=-1)
        black_pixels = np.all(image == 0, axis=-1)
        return np.sum(cloud_pixels) + np.sum(black_pixels)
