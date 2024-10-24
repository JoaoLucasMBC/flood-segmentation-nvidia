import os
import cv2
import json
import numpy as np
from dotenv import load_dotenv
from pathlib import Path
from functools import reduce

load_dotenv(dotenv_path=Path('../../config/.env'))

local_data_dir = os.environ['LOCAL_DATA_DIR']

countries = ['Bolivia', 'Ghana', 'India', 'Mekong', 'Nigeria', 'Paraguay', 'USA', 'Pakistan', 'Spain', 'Sri-Lanka', 'Somalia']
threshold = 0.2 
results = dict()

def calculate_test_mean_water():
    for country in countries:
        file_path = f"{local_data_dir}/masks/val/{country}"
        country_result = { "amount_of_images": 0, "test_mean_water_proportion": 0, "little_water": 0, "a_lot_of_water": 0 }

        if not os.path.exists(file_path):
            print(f"Not Found: {file_path}")
            results[country] = None 
            continue

        masks = [os.path.join(file_path, mask) for mask in os.listdir(file_path)]
        total_water = 0

        for mask_path in masks:
            imagem = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

            if imagem is None:
                print(f"Error to read: {mask_path}")
                continue

            water_percentage = np.sum(imagem == 255) / imagem.size
            total_water += water_percentage

            country_result["little_water"] += water_percentage < threshold
            country_result["a_lot_of_water"] += water_percentage > (1 - threshold)
            country_result["amount_of_images"] += 1

        if country_result["amount_of_images"] > 0:
            country_result["test_mean_water_proportion"] = total_water / country_result["amount_of_images"]
            country_result["little_water"] /= country_result["amount_of_images"]
            country_result["a_lot_of_water"] /= country_result["amount_of_images"]

        results[country] = country_result if country_result["amount_of_images"] > 0 else None

def calculate_train_mean_water():    
    models_metrics_path = f"{local_data_dir}/results/models_metrics.json"
    with open(models_metrics_path, 'r') as file:
        models_metrics = json.load(file)
    
    if len(results) <= 1:
        raise ValueError("There must be more than one country in the results for this calculation.")
    
    country_mean_sum = reduce(lambda acc, data: acc + data["test_mean_water_proportion"], results.values(), 0)

    for country, data in results.items():
        if "Not_"+country in models_metrics:
            models_metrics["Not_"+country]["train_mean_water_proportion"] = (country_mean_sum - data["test_mean_water_proportion"]) / (len(results) - 1)
    
    with open(models_metrics_path, 'w', encoding='utf-8') as file:
        json.dump(models_metrics, file, ensure_ascii=False, indent=2)

def export_results():
    calculate_test_mean_water()
    calculate_train_mean_water()

    os.makedirs(f"{local_data_dir}/results", exist_ok=True)
    result_file = f"{local_data_dir}/results/test_datasets_metrics.json"

    with open(result_file, 'w') as output_file:
        json.dump(results, output_file, indent=2)
    
    print(f"Exported results: {result_file}")

if __name__ == '__main__':
    export_results()
