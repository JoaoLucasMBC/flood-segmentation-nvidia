import os
import subprocess
from dotenv import load_dotenv
from pathlib import Path
import json
from functools import reduce

load_dotenv(dotenv_path=Path('../../config/.env'))

local_data_dir = os.environ['LOCAL_DATA_DIR']
local_project_dir = os.environ['LOCAL_PROJECT_DIR']
tao_specs_dir = os.environ['TAO_SPECS_DIR']
local_specs_dir = os.environ['LOCAL_SPECS_DIR']
tao_experiment_dir = os.environ['TAO_EXPERIMENT_DIR']
nvidia_api_key = os.environ['NVIDIA_API_KEY']

countries = ['Bolivia', 'Ghana', 'India', 'Mekong', 'Nigeria', 'Paraguay', 'USA', 'Pakistan', 'Spain', 'Sri-Lanka', 'Somalia']
metrics = ['Recall', 'Precision', 'F1 score', 'Mean IOU'] 

def set_country_spec_file(country:str):
    path = f'{local_specs_dir}/resnet18/combined_config.txt'
    with open(path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if 'val_images_path' in line:
            lines[i] = f'  val_images_path:"/workspace/tao-experiments/data/images/val/{country}"\n'
        elif 'val_masks_path' in line:
            lines[i] = f'  val_masks_path:"/workspace/tao-experiments/data/masks/val/{country}"\n'

    with open(path, 'w') as file:
        file.writelines(lines)

def model_evaluate():
    for test_country in countries:
        set_country_spec_file(test_country)

        command = [
                'tao', 'model', 'unet', 'evaluate',
                '-e', f'{tao_specs_dir}/resnet18/combined_config.txt',
                '-m', f'{tao_experiment_dir}/resnet18/{test_country}/weights/model.tlt',
                '-o', f'{tao_experiment_dir}/resnet18/{test_country}/',
                '-k', nvidia_api_key
            ]

        os.makedirs(f"{local_data_dir}/results", exist_ok=True)
        result_file = f"{local_data_dir}/results/result_{test_country.lower()}.txt"

        print(f"testing: {test_country}")
            
        with open(result_file, 'w') as output_file:
            subprocess.run(command, stdout=output_file, stderr=subprocess.STDOUT)

    set_country_spec_file("")

def set_amount_of_images(results):
    data_distribuition_path = f"{local_data_dir}/results/data_distribution.json"
    with open(data_distribuition_path, 'r') as file:
        data_distribuition = json.load(file)
    
    image_total_amount = reduce(lambda acc, x: x+acc, data_distribuition.values(), 0)
    for country, data in results.items():
        data["train_amount_of_images"] = image_total_amount - data_distribuition[country.split("_")[1]]

def create_country_metrics_json():
    results = {}

    for country in countries:
        path = f"{local_data_dir}/results/result_{country.lower()}.txt"

        try:
            with open(path, 'r') as file:
                lines = file.readlines()
        except:
            continue
        
        metrics_dict = {}
        for line in reversed(lines):
            for metric in metrics:
                if metric in line:
                    value = float(line.split(':')[-1].strip())
                    metrics_dict[metric] = value

                    if len(metrics_dict) == len(metrics):
                        break

            if len(metrics_dict) == len(metrics):
                break

        results["Not_"+country] = metrics_dict
    
    set_amount_of_images(results)

    os.makedirs(f"{local_data_dir}/results", exist_ok=True)
    result_file = f"{local_data_dir}/results/models_metrics.json"

    with open(result_file, 'w') as output_file:
        json.dump(results, output_file, indent=2)    

if __name__ == '__main__':
    # model_evaluate()
    create_country_metrics_json()