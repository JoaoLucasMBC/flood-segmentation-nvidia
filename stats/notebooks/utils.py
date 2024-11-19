import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from skimage import io, color, measure, morphology

# Single image
def calc_flood_mean_value_of_image(flood_image, mask):
    # Create the water mask with the condition
    water_mask = (mask > 128) & (np.all(flood_image != [255, 255, 255], axis=-1))
    
    # Apply the mask to the flood image
    water_pixels = flood_image[water_mask]
    
    # Calculate the mean, handling cases with no water pixels
    return np.mean(water_pixels, axis=0) if water_pixels.size > 0 else np.array([np.nan, np.nan, np.nan])

# Only surrounding images
def flood_mean_value_surrounding(flood_images, masks, row, col):
    flood_means = []
    for i in range(row+1):
        for j in range(col+1):
            flood_means.append(calc_flood_mean_value_of_image(flood_images[i][j], masks[i][j]))

    if row < len(flood_images)-1:
        flood_means.append(calc_flood_mean_value_of_image(flood_images[i+1][j], masks[i+1][j]))
        if col > 1:
            flood_means.append(calc_flood_mean_value_of_image(flood_images[i+1][j-1], masks[i+1][j-1]))
    
    if col < len(flood_images[0])-1:
        flood_means.append(calc_flood_mean_value_of_image(flood_images[i][j+1], masks[i][j+1]))

        if row > 1:
            flood_means.append(calc_flood_mean_value_of_image(flood_images[i-1][j+1], masks[i-1][j+1]))

    if col < len(flood_images[0])-1 and row < len(flood_images)-1:
        flood_means.append(calc_flood_mean_value_of_image(flood_images[i+1][j+1], masks[i+1][j+1]))

    return np.nanmean(np.array(flood_means), axis=0)

# Using the difference between now and surrounding images (mean value from surrounding images)
def improve_mask(sentinel2_dir, natural_water_masks_dir, flood_masks_dir, old_dir, save_dir, filename, rows, cols):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    non_flood_images = [[io.imread(f"./{old_dir}/{filename}_{i}_{j}.png") for j in range(cols)] for i in range(rows)]
    flood_images = [[io.imread(f'./{sentinel2_dir}/{filename}_{i}_{j}.png') for j in range(cols)] for i in range(rows)]

    for i in range(len(flood_images)):
        for j in range(len(flood_images[0])):
            # Determine if the image has an alpha channel
            if flood_images[i][j].shape[-1] == 4:
                # Exclude the alpha channel
                flood_images[i][j] = flood_images[i][j][..., :3]

            # Determine if the image has an alpha channel
            if non_flood_images[i][j].shape[-1] == 4:
                # Exclude the alpha channel
                non_flood_images[i][j] = non_flood_images[i][j][..., :3]
    
    flood_masks = [[io.imread(f'./{flood_masks_dir}/{filename}_{i}_{j}.png') for j in range(cols)] for i in range(rows)]
    natural_water_masks = [[io.imread(f'./{natural_water_masks_dir}/{filename}_{i}_{j}.png') for j in range(cols)] for i in range(rows)]

    for i in range(rows):
        for j in range(cols):
            flood_image = flood_images[i][j]
            non_flood_image = non_flood_images[i][j]
            mask = flood_masks[i][j]
            natural_water_mask = natural_water_masks[i][j]

            natural_water_mask = natural_water_mask > 128
            mask[natural_water_mask] = 0

            water_mask = mask > 128
            
            white_pixel_count = np.sum(water_mask)
            total_pixel_count = water_mask.size
            white_pixel_percentage = (white_pixel_count / total_pixel_count) * 100

            if white_pixel_percentage <= 0.5:
                io.imsave(f'{save_dir}/{filename}_{i}_{j}.png', mask)
                continue

            flood_mean_rgb = flood_mean_value_surrounding(flood_images, flood_masks, i, j)
                        
            flood_mask = np.all((flood_image >= flood_mean_rgb*0.85) & (flood_image <= flood_mean_rgb*1.15), axis=-1)
            non_flood_mask = np.all((non_flood_image >= flood_mean_rgb*0.85) & (non_flood_image <= flood_mean_rgb*1.15), axis=-1)

            inverse_flood_mask = np.logical_not(flood_mask)

            highlighted_flood_image = np.copy(flood_image)
            
            highlighted_flood_image[flood_mask] = [255, 255, 255]
            highlighted_flood_image[inverse_flood_mask] = [0, 0, 0]
            highlighted_flood_image[non_flood_mask] = [0, 0, 0]
            highlighted_flood_image[water_mask] = [255, 255, 255]

            io.imsave(f'{save_dir}/{filename}_{i}_{j}.png', highlighted_flood_image)

def clean_image(image, min_area=5):
    binary = image > 0.5

    labeled_image, num_labels = measure.label(binary, return_num=True, connectivity=2)

    cleaned_image = morphology.remove_small_objects(labeled_image, min_size=min_area)

    # Convert the cleaned image back to binary (True for white pixels, False for black)
    binary_cleaned = cleaned_image > 0
    return binary_cleaned

def close_image(image, disk_size=5):
    selem = morphology.disk(disk_size)
    closed_image = morphology.closing(image, selem)
    return closed_image


def make_map(image_folders, filename, rows, cols):
    maps = []

    for folder in image_folders:
        tiles = []
        for i in range(rows):
            col_tiles = []
            for j in range(cols):
                file = f"{filename}_{i}_{j}.png"
                img = Image.open(os.path.join(folder, file))
                col_tiles.append(img)
            tiles.append(col_tiles)

        tile_width, tile_height = tiles[0][0].size
        full_width = cols * tile_width
        full_height = rows * tile_height

        full_image = Image.new('RGB', (full_width, full_height))

        y_offset = 0
        for col_list in tiles:
            x_offset = 0
            for sing_img in col_list:
                full_image.paste(sing_img, (x_offset, y_offset))
                x_offset += tile_width
            y_offset += tile_height

        maps.append(full_image)

    # Combine all maps side by side
    map_width = maps[0].size[0]
    map_height = maps[0].size[1]
    total_width = len(maps) * map_width
    combined_map = Image.new('RGB', (total_width, map_height))

    x_offset = 0
    for map_image in maps:
        combined_map.paste(map_image, (x_offset, 0))
        x_offset += map_width

    combined_map_np = np.array(combined_map)

    plt.figure(figsize=(10, 10))
    plt.imshow(combined_map_np)
    plt.axis('off')
    plt.show()


# Function to load images into a grid
def load_tiles(folder_path, rows, cols, file_pattern):
    tiles = []
    for i in range(cols):  # Assuming col represents the number of columns
        col_tiles = []
        for j in range(rows):  # Assuming row represents the number of rows
            filename = f"{file_pattern}_{j}_{i}.png"
            img = Image.open(os.path.join(folder_path, filename))
            col_tiles.append(img)
        tiles.append(col_tiles)
    return tiles

# Function to stitch the images into a full grid
def stitch_images(tiles, rows, cols):
    tile_width, tile_height = tiles[0][0].size
    full_width = cols * tile_width
    full_height = rows * tile_height
    full_image = Image.new('RGB', (full_width, full_height))
    
    x_offset = 0
    for row_list in tiles:
        y_offset = 0
        for sing_img in row_list:
            full_image.paste(sing_img, (x_offset, y_offset))
            y_offset += tile_width
        x_offset += tile_height
    return np.array(full_image)