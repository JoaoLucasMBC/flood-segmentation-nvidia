import os
import shutil
import subprocess
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path('../../config/.env'))

countries = ['Bolivia', 'Ghana', 'India', 'Mekong', 'Nigeria', 'Paraguay', 'USA', 'Pakistan', 'Spain', 'Sri-Lanka', 'Somalia']

data_dir = os.environ['DATA_DIR']
local_data_dir = os.environ['LOCAL_DATA_DIR']
local_project_dir = os.environ['LOCAL_PROJECT_DIR']
tao_specs_dir = os.environ['TAO_SPECS_DIR']
tao_experiment_dir = os.environ['TAO_EXPERIMENT_DIR']
nvidia_api_key = os.environ['NVIDIA_API_KEY']

file_list = os.listdir(f"{local_data_dir}/ProcessedS1/")

def split_and_train():
    for test_country in countries:
        print(f"Country test: {test_country}")
        
        train_image_dir = f"{local_data_dir}/images/train/"
        train_mask_dir = f"{local_data_dir}/masks/train/"

        os.makedirs(train_image_dir, exist_ok=True)
        os.makedirs(train_mask_dir, exist_ok=True)

        test_image_dir = f"{local_data_dir}/images/test/"
        test_mask_dir = f"{local_data_dir}/masks/test/"
        
        os.makedirs(test_image_dir, exist_ok=True)
        os.makedirs(test_mask_dir, exist_ok=True)

        # Clear the train and test directories
        for directory in [train_image_dir, train_mask_dir, test_image_dir, test_mask_dir]:
            for item in os.listdir(directory):
                os.remove(os.path.join(directory, item))

        # Distribute files to train and test directories
        for file in file_list:
            if file.split('.')[-1] == 'png':
                src_image = f"{local_data_dir}/ProcessedS1/{file}"
                src_mask = f"{local_data_dir}/ProcessedLabelHand/{file}"
                dest_image = train_image_dir if file.split('_')[0] != test_country else test_image_dir
                dest_mask = train_mask_dir if file.split('_')[0] != test_country else test_mask_dir

                shutil.copyfile(src_image, os.path.join(dest_image, file))
                shutil.copyfile(src_mask, os.path.join(dest_mask, file))

        # Run training
        print(f"Training model for test country: {test_country}")

        train_command = [
            'tao', 'model', 'unet', 'train',
            '-e', f'{tao_specs_dir}/resnet18/combined_config.txt',
            '-r', f'{tao_experiment_dir}/resnet18/{test_country}/',
            '-m', f'{tao_experiment_dir}/pretrained/resnet18/pretrained_semantic_segmentation_vresnet18/resnet_18.hdf5',
            '-k', nvidia_api_key
        ]

        subprocess.run(train_command, check=True)

    for directory in [train_image_dir, train_mask_dir, test_image_dir, test_mask_dir]:
        for item in os.listdir(directory):
            os.remove(os.path.join(directory, item))
    
if __name__ == '__main__':
    split_and_train()
