import os
import cv2
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path('../../config/.env'))

data_dir = os.environ['DATA_DIR']
local_data_dir = os.environ['LOCAL_DATA_DIR']

image = 'Sri-Lanka_916628'
iou = '0.826'

def load_image_as_array(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Failed to load image from path: {image_path}")
    return img

def create_confusion_matrix():
    mask_path = f'{local_data_dir}/results/images/{image}/mask.png'
    inference_path = f'{local_data_dir}/results/images/{image}/inferece_from_{iou}IOU_model.png'

    mask = load_image_as_array(mask_path)
    inference = load_image_as_array(inference_path)

    inference_flat = inference.ravel()
    mask_flat = mask.ravel()

    conf_matrix = confusion_matrix(mask_flat, inference_flat)

    fig, axs = plt.subplots(1, 3, figsize=(18, 6))

    axs[0].imshow(inference, cmap='gray')
    axs[0].set_title('Inference Image')
    axs[0].axis('off')  

    axs[1].imshow(mask, cmap='gray')
    axs[1].set_title('Mask Image (Ground Truth)')
    axs[1].axis('off')  

    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', ax=axs[2])
    axs[2].set_title('Confusion Matrix')
    axs[2].set_xlabel('Predicted')
    axs[2].set_ylabel('True')

    plt.tight_layout()

    output_image_path = f'{local_data_dir}/results/images/{image}/confusion_matrix_{iou}IOU_model.png'
    plt.savefig(output_image_path)

    plt.show()

    print(f"Combined image, mask, and confusion matrix saved at: {output_image_path}")

if __name__ == '__main__':
    create_confusion_matrix()
