import os
import shutil
import subprocess

# country_list
countries = ['Bolivia', 'Ghana', 'India', 'Mekong', 'Nigeria', 'Paraguay', 'USA', 'Spain', 'Ski-lanka', 'Somalia']

local_data_dir = os.environ['LOCAL_DATA_DIR']
tao_specs_dir = os.environ['TAO_SPECS_DIR']
tao_experiment_dir = os.environ['TAO_EXPERIMENT_DIR']
nvidia_api_key = os.environ['NVIDIA_API_KEY']

# get all images
file_list = os.listdir(f"{local_data_dir}/ProcessedS1/")

# set eact country as test_country
for test_country in countries:
    print(f"Country test: {test_country}")
    
    train_image_dir = f"{local_data_dir}/images/train/"
    train_mask_dir = f"{local_data_dir}/masks/train/"

    for each_file in file_list:
        if each_file.split('.')[-1] == 'png':
            src_image = f"{local_data_dir}/ProcessedS1/{each_file}"
            src_mask = f"{local_data_dir}/ProcessedLabelHand/{each_file}"

            if each_file.split('_')[0] == test_country:
                shutil.copyfile(f"{os.environ['LOCAL_DATA_DIR']}/ProcessedS1/{each_file}", f"{os.environ['LOCAL_DATA_DIR']}/images/train/{each_file}")
                shutil.copyfile(f"{os.environ['LOCAL_DATA_DIR']}/ProcessedLabelHand/{each_file}", f"{os.environ['LOCAL_DATA_DIR']}/masks/train/{each_file}")
            else:
                shutil.copyfile(f"{os.environ['LOCAL_DATA_DIR']}/ProcessedS1/{each_file}", f"{os.environ['LOCAL_DATA_DIR']}/images/train/{each_file}")
                shutil.copyfile(f"{os.environ['LOCAL_DATA_DIR']}/ProcessedLabelHand/{each_file}", f"{os.environ['LOCAL_DATA_DIR']}/masks/train/{each_file}")

    command = [
        'tao', 'model', 'unet', 'evaluate',
        '-e', f'{tao_specs_dir}/resnet18/combined_config.txt',
        '-m', f'{tao_experiment_dir}/resnet18/weights/resnet18.tlt',
        '-o', f'{tao_experiment_dir}/resnet18/',
        '-k', nvidia_api_key
    ]

    print(f"testing: {test_country}")
    
    result_file = f"{tao_experiment_dir}/resnet18/results_{test_country}.txt"
    
    with open(result_file, 'w') as output_file:
        subprocess.run(command, stdout=output_file, stderr=subprocess.STDOUT)

    print(f"Results: {result_file}")
