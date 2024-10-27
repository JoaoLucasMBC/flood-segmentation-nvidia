import numpy as np
from PIL import Image
from skimage import io
import matplotlib.pyplot as plt
import os

## FLOOD MEAN VALUE

# Single image
def calc_flood_mean_value_of_image(flood_image, mask):
    water_mask = mask > 128
    water_pixels = flood_image[water_mask]
    return np.mean(water_pixels, axis=0)

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

# All images
def calc_flood_mean_value_whole_map(flood_images, masks, rows, cols):
    flood_means = []
    for i in range(rows):
        for j in range(cols):
            flood_image = flood_images[i][j]
            mask = masks[i][j]

            water_mask = mask > 128

            water_pixels = flood_image[water_mask]

            flood_means.append(np.mean(water_pixels, axis=0))

    flood_means = np.array(flood_means)
    return np.nanmean(flood_means, axis=0)

### IMPROVE MASK

# Only using mean with all images
def improve_mask(sentinel2_dir, masks_dir, save_dir, filename, rows, cols):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    flood_images = [[io.imread(f'./{sentinel2_dir}/{filename}_{i}_{j}.png') for j in range(cols)] for i in range(rows)]
    flood_masks = [[io.imread(f'./{masks_dir}/{filename}_{i}_{j}.png') for j in range(cols)] for i in range(rows)]
    
    flood_mean_rgb = calc_flood_mean_value_whole_map(sentinel2_dir, masks_dir, rows, cols)
    
    for i in range(rows):
        for j in range(cols):
            flood_image = flood_images[i][j]
            mask = flood_masks[i][j]
            water_mask = mask > 128
            
            flood_mask = np.all((flood_image >= flood_mean_rgb*0.85) & (flood_image <= flood_mean_rgb*1.15), axis=-1)
            inverse_flood_mask = np.logical_not(flood_mask)
            highlighted_flood_image = np.copy(flood_image)
            highlighted_flood_image[flood_mask] = [255, 255, 255]
            highlighted_flood_image[inverse_flood_mask] = [0, 0, 0]
            highlighted_flood_image[water_mask] = [255, 255, 255]

            io.imsave(f'./{save_dir}/{filename}_{i}_{j}.png', highlighted_flood_image)

# Using the difference between now and old image (mean value from all images)
def improve_mask_with_old_diff(sentinel2_dir, masks_dir, old_dir, save_dir, filename, rows, cols):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    flood_images = [[io.imread(f'./{sentinel2_dir}/{filename}_{i}_{j}.png') for j in range(cols)] for i in range(rows)]
    pre_flood_images = [[io.imread(f'./{old_dir}/{filename}_{i}_{j}.png') for j in range(cols)] for i in range(rows)]
    flood_masks = [[io.imread(f'./{masks_dir}/{filename}_{i}_{j}.png') for j in range(cols)] for i in range(rows)]

    
    flood_mean_rgb = calc_flood_mean_value_whole_map(sentinel2_dir, masks_dir, rows, cols)
    
    for i in range(rows):
        for j in range(cols):
            flood_image = flood_images[i][j]
            non_flood_image = pre_flood_images[i][j]
            mask = flood_masks[i][j]

            water_mask = mask > 128
            
            flood_mask = np.all((flood_image >= flood_mean_rgb*0.85) & (flood_image <= flood_mean_rgb*1.15), axis=-1)
            non_flood_mask = np.all((non_flood_image >= flood_mean_rgb*0.85) & (non_flood_image <= flood_mean_rgb*1.15), axis=-1)

            inverse_flood_mask = np.logical_not(flood_mask)
            highlighted_flood_image = np.copy(flood_image)
            highlighted_flood_image[flood_mask] = [255, 255, 255]
            highlighted_flood_image[inverse_flood_mask] = [0, 0, 0]
            highlighted_flood_image[non_flood_mask] = [0, 0, 0]
            highlighted_flood_image[water_mask] = [255, 255, 255]

            io.imsave(f'./{save_dir}/{filename}_{i}_{j}.png', highlighted_flood_image)
            
# Using the difference between now and surrounding images (mean value from surrounding images)
def improve_mask_with_old_diff_and_only_surrounding_mean_flood_value(sentinel2_dir, masks_dir, old_dir, save_dir, filename, rows, cols):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    non_flood_images = [[io.imread(f"./{old_dir}/{filename}_{i}_{j}.png") for j in range(cols)] for i in range(rows)]
    flood_images = [[io.imread(f'./{sentinel2_dir}/{filename}_{i}_{j}.png') for j in range(cols)] for i in range(rows)]
    masks = [[io.imread(f'./{masks_dir}/{filename}_{i}_{j}.png') for j in range(cols)] for i in range(rows)]

    for i in range(rows):
        for j in range(cols):
            flood_image = flood_images[i][j]
            non_flood_image = non_flood_images[i][j]
            mask = masks[i][j]
            flood_mean_rgb = flood_mean_value_surrounding(flood_images, masks, i, j)
            
            water_mask = mask > 128
            
            flood_mask = np.all((flood_image >= flood_mean_rgb*0.85) & (flood_image <= flood_mean_rgb*1.15), axis=-1)
            non_flood_mask = np.all((non_flood_image >= flood_mean_rgb*0.85) & (non_flood_image <= flood_mean_rgb*1.15), axis=-1)

            inverse_flood_mask = np.logical_not(flood_mask)
            highlighted_flood_image = np.copy(flood_image)
            highlighted_flood_image[flood_mask] = [255, 255, 255]
            highlighted_flood_image[inverse_flood_mask] = [0, 0, 0]
            highlighted_flood_image[non_flood_mask] = [0, 0, 0]
            highlighted_flood_image[water_mask] = [255, 255, 255]

            io.imsave(f'./{save_dir}/{filename}_{i}_{j}.png', highlighted_flood_image)
            
# Only using mean with own image and old diff
def improve_mask_with_only_own_mean(sentinel2_dir, masks_dir, old_dir, save_dir, filename, rows, cols):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    for i in range(rows):
        for j in range(cols):
            flood_image = io.imread(f'./{sentinel2_dir}/{filename}_{i}_{j}.png')
            non_flood_image = io.imread(f"./{old_dir}/{filename}_{i}_{j}.png")
            mask = io.imread(f'./{masks_dir}/{filename}_{i}_{j}.png')

            flood_mean_rgb = calc_flood_mean_value_of_image(flood_image, mask)

            water_mask = mask > 128
            
            flood_mask = np.all((flood_image >= flood_mean_rgb*0.85) & (flood_image <= flood_mean_rgb*1.15), axis=-1)
            non_flood_mask = np.all((non_flood_image >= flood_mean_rgb*0.85) & (non_flood_image <= flood_mean_rgb*1.15), axis=-1)

            inverse_flood_mask = np.logical_not(flood_mask)
            highlighted_flood_image = np.copy(flood_image)
            highlighted_flood_image[flood_mask] = [255, 255, 255]
            highlighted_flood_image[inverse_flood_mask] = [0, 0, 0]
            highlighted_flood_image[non_flood_mask] = [0, 0, 0]
            highlighted_flood_image[water_mask] = [255, 255, 255]

            io.imsave(f'./{save_dir}/{filename}_{i}_{j}.png', highlighted_flood_image)
            