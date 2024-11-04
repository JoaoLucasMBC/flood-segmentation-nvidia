import numpy as np
from PIL import Image
from skimage import io
import matplotlib.pyplot as plt
import os

def make_map(image_folder, filename, rows, cols):
    tiles = []

    for i in range(rows):
        col_tiles = []
        for j in range(cols):
            file = f"{filename}_{i}_{j}.png"
            img = Image.open(os.path.join(image_folder, file))
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

    full_image_np = np.array(full_image)

    plt.figure(figsize=(10, 10))
    plt.imshow(full_image_np)
    plt.axis('off')
    plt.show()