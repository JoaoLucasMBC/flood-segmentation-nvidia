import os
import shutil
import subprocess
from dotenv import load_dotenv
from pathlib import Path
import onnxruntime as ort
import json

import importlib.util

# Get the absolute path to the module you want to import
module_path = os.path.abspath(os.path.join('..', '..', '..', 'stats', 'model', 'model.py'))

# Load the module dynamically
spec = importlib.util.spec_from_file_location("FloodModel", module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# Now you can use FloodModel from the module
FloodModel = module.FloodModel

load_dotenv(dotenv_path=Path('../../config/.env'))

data_dir = os.environ['DATA_DIR']
local_data_dir = os.environ['LOCAL_DATA_DIR']
local_project_dir = os.environ['LOCAL_PROJECT_DIR']
tao_specs_dir = os.environ['TAO_SPECS_DIR']
tao_experiment_dir = os.environ['TAO_EXPERIMENT_DIR']
nvidia_api_key = os.environ['NVIDIA_API_KEY']
local_commands_dir = os.environ['LOCAL_COMMANDS_DIR']

def set_country_export_file(country:str):
    path = f'{local_commands_dir}/export.sh'
    with open(path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if 'tao model unet export' in line:
            lines[i] = f'tao model unet export -m $TAO_EXPERIMENT_DIR/resnet18/{country}weights/model.tlt \\\n'

    with open(path, 'w') as file:
        file.writelines(lines)

countries = ['Bolivia', 'Ghana', 'India', 'Mekong', 'Nigeria', 'Paraguay', 'USA', 'Pakistan', 'Spain', 'Sri-Lanka', 'Somalia']

# set_country_export_file("USA/")
# subprocess.run(['bash', f'{local_commands_dir}/export.sh'])

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def compare_inferences(country_list, image):
    image_path = f'{local_data_dir}/ProcessedS1/{image}.png'
    mask_path = f'{local_data_dir}/ProcessedLabelHand/{image}.png'
    metrics_path = f"{local_data_dir}/results/country_metrics.json"

    metrics = load_json(metrics_path)

    os.makedirs(f"{local_data_dir}/results/images", exist_ok=True)

    for country in country_list:
        output_path = f'{local_data_dir}/results/images/{image}@IOU{metrics[country]["Mean IOU"]:.3f}.png'
        model_path = f'{local_project_dir}/unet/resnet18/{country}/weights/model.onnx'
        model = FloodModel(model_path, verbose=True)
        model.predict(image_path, output_path)

# image = "Paraguay_1029042"
# image = "Bolivia_314919"
image = "India_91379"
compare_inferences(['Ghana', 'USA'], image)

