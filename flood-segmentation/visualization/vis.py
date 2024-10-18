import matplotlib.pyplot as plt
import random
import os
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path


# define simple grid visualizer
def visualize_images(num_images=10):
    overlay_path=os.path.join(os.environ['LOCAL_PROJECT_DIR'], 'tao_infer_testing', 'vis_overlay_tlt')
    inference_path=os.path.join(os.environ['LOCAL_PROJECT_DIR'], 'tao_infer_testing', 'mask_labels_tlt')
    actual_path=os.path.join(os.environ['LOCAL_DATA_DIR'], 'masks', 'val')
    inference_images_path=os.path.join(os.environ['LOCAL_DATA_DIR'], 'images', 'val')
        
    fig_dim=4
    fig, ax_arr=plt.subplots(num_images, 4, figsize=[4*fig_dim, num_images*fig_dim], sharex=True, sharey=True)
    ax_arr[0, 0].set_title('Overlay')
    ax_arr[0, 1].set_title('Input')
    ax_arr[0, 2].set_title('Inference')
    ax_arr[0, 3].set_title('Actual')
    ax_arr[0, 0].set_xticks([])
    ax_arr[0, 0].set_yticks([])
    
    for idx, img_name in enumerate(random.sample(os.listdir(actual_path), num_images)):
        ax_arr[idx, 0].imshow(plt.imread(overlay_path+'/'+img_name))
        ax_arr[idx, 0].set_ylabel(img_name)
        ax_arr[idx, 1].imshow(plt.imread(inference_images_path+'/'+img_name))
        ax_arr[idx, 2].imshow(plt.imread(inference_path+'/'+img_name), cmap='gray')
        ax_arr[idx, 3].imshow(plt.imread(actual_path+'/'+img_name), cmap='gray')
    fig.tight_layout()

    # Save the figure with a unique timestamp in the filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = os.path.join(os.getcwd(), f"visualization_{timestamp}.png")
    fig.savefig(output_path)
    plt.close(fig)

    print(f"Image saved as {output_path}")

if __name__ == "__main__":
    load_dotenv(dotenv_path=Path('../config/.env'))
    visualize_images()
