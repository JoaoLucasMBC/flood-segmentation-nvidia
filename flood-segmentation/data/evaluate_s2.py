import os
from PIL import Image
import numpy as np

def find_all_black_images(main_folder):
    black_images = []
    
    for root, dirs, files in os.walk(main_folder):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg')):  # Add other image formats if needed
                image_path = os.path.join(root, file)
                image = Image.open(image_path)
                image_np = np.array(image)
                
                # Check if the image is all black (all pixel values are 0)
                if np.all(image_np == 0):
                    black_images.append(image_path)
    
    return len(black_images), black_images

# Example usage
main_folder_path = '/home/user/open-flood/flood-segmentation/data/output'
black_image_count, black_image_paths = find_all_black_images(main_folder_path)

print(f"Number of black images: {black_image_count}")
print("Paths of black images:")
for path in black_image_paths:
    print(path)