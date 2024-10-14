import os
import cv2
import json
import numpy as np
from dotenv import load_dotenv

load_dotenv()

local_data_dir = os.environ['LOCAL_DATA_DIR']

countries = ['Bolivia', 'Ghana', 'India', 'Mekong', 'Nigeria', 'Paraguay', 'USA', 'Pakistan', 'Spain', 'Sri-Lanka', 'Somalia']
metrics = ['Recall', 'Precision', 'F1 score', 'Mean IOU'] 

p = {}

for country in countries:
    path = f"{local_data_dir}/v{os.environ['VERSION']}/results/result_{country.lower()}.txt"

    try:
        with open(path, 'r') as file:
            lines = file.readlines()
    except Exception as e:
        continue
    
    result_dict = {}
    for line in reversed(lines):
        for metric in metrics:
            if metric in line:
                value = float(line.split(':')[-1].strip())
                result_dict[metric] = value

                if len(result_dict) == len(metrics):
                    break

        if len(result_dict) == len(metrics):
                break

    p[country] = result_dict

os.makedirs(f"{local_data_dir}/v{os.environ['VERSION']}/results", exist_ok=True)
result_file = f"{local_data_dir}/v{os.environ['VERSION']}/results/country_metrics.json"

with open(result_file, 'w') as output_file:
    json.dump(p, output_file, indent=2)     

    
