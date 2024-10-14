import os
import subprocess
from dotenv import load_dotenv
load_dotenv()

local_data_dir = os.environ['LOCAL_DATA_DIR']
local_project_dir = os.environ['LOCAL_PROJECT_DIR']
tao_specs_dir = os.environ['TAO_SPECS_DIR']
local_specs_dir = os.environ['LOCAL_SPECS_DIR']
tao_experiment_dir = os.environ['TAO_EXPERIMENT_DIR']
nvidia_api_key = os.environ['NVIDIA_API_KEY']

def set_country_spec_file(country:str):
    path = f'{local_specs_dir}/v{os.environ["VERSION"]}/resnet18/combined_config.txt'
    with open(path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if 'val_images_path' in line:
            lines[i] = f'  val_images_path:"/workspace/tao-experiments/data/images/val/{country}"\n'
        elif 'val_masks_path' in line:
            lines[i] = f'  val_masks_path:"/workspace/tao-experiments/data/masks/val/{country}"\n'

    with open(path, 'w') as file:
        file.writelines(lines)

for test_country in ['Bolivia', 'Ghana', 'India', 'Mekong', 'Nigeria', 'Paraguay', 'USA', 'Pakistan', 'Spain', 'Sri-Lanka', 'Somalia']:
    set_country_spec_file(test_country)

    command = [
            'tao', 'model', 'unet', 'evaluate',
            '-e', f'{tao_specs_dir}/resnet18/combined_config.txt',
            '-m', f'{tao_experiment_dir}/resnet18/{test_country}/weights/model.tlt',
            '-o', f'{tao_experiment_dir}/resnet18/{test_country}/',
            '-k', nvidia_api_key
        ]

    os.makedirs(f"{local_data_dir}/v{os.environ['VERSION']}/results", exist_ok=True)
    result_file = f"{local_data_dir}/v{os.environ['VERSION']}/results/result_{test_country.lower()}.txt"

    print(f"testing: {test_country}")
        
    with open(result_file, 'w') as output_file:
        subprocess.run(command, stdout=output_file, stderr=subprocess.STDOUT)

set_country_spec_file("")