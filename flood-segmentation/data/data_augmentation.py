import albumentations as A
import cv2
import os
from albumentations.pytorch import ToTensorV2

from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path('../config/.env'))

# Directories for images and masks
image_dir = os.path.join(os.environ['LOCAL_DATA_DIR'], 'images', 'train')
mask_dir = os.path.join(os.environ['LOCAL_DATA_DIR'], 'masks', 'train')

output_image_dir = os.path.join(os.environ['LOCAL_DATA_DIR'], 'images', 'augmented_train')
output_mask_dir = os.path.join(os.environ['LOCAL_DATA_DIR'], 'masks', 'augmented_train')
os.makedirs(output_image_dir, exist_ok=True)
os.makedirs(output_mask_dir, exist_ok=True)

# Define augmentation pipeline
transform = A.Compose([
    A.Rotate(limit=15, p=0.8),
    A.RandomBrightnessContrast(p=0.8),
    A.HueSaturationValue(hue_shift_limit=15, sat_shift_limit=20, val_shift_limit=15, p=0.8),
    A.GaussianBlur(blur_limit=5, p=0.5),
    A.GaussNoise(var_limit=(10.0, 50.0), p=0.5),
    A.ElasticTransform(p=0.3),
    ToTensorV2()
])

# Number of augmented versions per image
num_augmented_versions = 3  # You can increase this number to generate more data

# Loop over image and mask pairs
# Copy original images and masks to the output directories
for filename in os.listdir(image_dir):
    if filename.endswith(".png"):  # or other image formats
        image_path = os.path.join(image_dir, filename)
        mask_path = os.path.join(mask_dir, filename)

        # Copy original image and mask
        original_image = cv2.imread(image_path)
        original_mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

        # Save original image and mask
        cv2.imwrite(os.path.join(output_image_dir, filename), original_image)
        cv2.imwrite(os.path.join(output_mask_dir, filename), original_mask)

        # Apply augmentations
        for i in range(num_augmented_versions):
            augmented = transform(image=original_image, mask=original_mask)
            augmented_image = augmented['image']
            augmented_mask = augmented['mask']

            augmented_filename = f"{filename.split('.')[0]}_aug_{i}.png"
            cv2.imwrite(os.path.join(output_image_dir, augmented_filename), augmented_image.numpy().transpose(1, 2, 0))
            cv2.imwrite(os.path.join(output_mask_dir, augmented_filename), augmented_mask.cpu().numpy())
