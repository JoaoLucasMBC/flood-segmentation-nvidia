import json
import os
import shutil
import subprocess
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path('../../config/.env'))

local_data_dir = os.environ['LOCAL_DATA_DIR']

countries = {}
file_list = os.listdir(f"{local_data_dir}/ProcessedS1/")

def separate_val_images():
    for file in file_list:

        country = file.split('_')[0]
        if country not in countries:
            countries[country] = 1
        else:
            countries[country] += 1

        src_image = f"{local_data_dir}/ProcessedS1/{file}"
        val_image_dir = f"{local_data_dir}/images/val/{country}"

        scr_mask = f"{local_data_dir}/ProcessedLabelHand/{file}"
        mask_dir = f"{local_data_dir}/masks/val/{country}"

        if not os.path.exists(val_image_dir):
            os.makedirs(val_image_dir)

        if not os.path.exists(mask_dir):
            os.makedirs(mask_dir)
            
        shutil.copyfile(src_image, os.path.join(val_image_dir, file))
        shutil.copyfile(scr_mask, os.path.join(mask_dir, file))

        os.makedirs(f"{local_data_dir}/results", exist_ok=True)
        result_file = f"{local_data_dir}/results/data_distribution.json"

        # create data_distribution.json
        with open(result_file, 'w') as output_file:
            json.dump(dict(sorted(countries.items(), key=lambda item: item[1])), output_file, indent=2)

if __name__ == '__main__':
    separate_val_images()