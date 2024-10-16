import os
import cv2
import json
import numpy as np
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path('../../config/.env'))

local_data_dir = os.environ['LOCAL_DATA_DIR']

countries = ['Bolivia', 'Ghana', 'India', 'Mekong', 'Nigeria', 'Paraguay', 'USA', 'Pakistan', 'Spain', 'Sri-Lanka', 'Somalia']
threshold = 0.2 

p = {}
for country in countries:

    file_path = f"{local_data_dir}/masks/val/{country}"

    if not os.path.exists(file_path):
        print(f"Not Found: {file_path}")
        break

    country_result = {
        "amount_of_images": 0,
        "mean_water_proportion": 0,
        "little_water": 0,
        "a_lot_of_water": 0
    }

    total_water = 0
    for mask in os.listdir(file_path):
        mask_path = os.path.join(file_path, mask)
        imagem = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        
        if imagem is None:
            print(f"Error to read: {mask_path}")
            continue

        white_pixels = np.sum(imagem == 255)
        total_pixels = imagem.size
        water_percentage = white_pixels / total_pixels
        total_water += water_percentage

        if water_percentage < threshold:
            country_result["little_water"] += 1
        elif water_percentage > (1 - threshold):
            country_result["a_lot_of_water"] += 1

        country_result["amount_of_images"] += 1

    if country_result["amount_of_images"] > 0:
        country_result['mean_water_proportion'] = total_water / country_result['amount_of_images']
        country_result['little_water'] /= country_result['amount_of_images']
        country_result['a_lot_of_water'] /= country_result['amount_of_images']
        p[country] = country_result
    else:
        p[country] = None
        print(f"Nenhuma máscara válida encontrada para {country}")

os.makedirs(f"{local_data_dir}/results", exist_ok=True)
result_file = f"{local_data_dir}/results/mask_distribution.json"

with open(result_file, 'w') as output_file:
    json.dump(p, output_file, indent=2)
