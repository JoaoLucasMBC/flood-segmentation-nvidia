import json
import os
import shutil
from dotenv import load_dotenv

load_dotenv()

countries = {}
local_data_dir = os.environ['LOCAL_DATA_DIR']
file_list = os.listdir(f"{local_data_dir}/v1/ProcessedS1/")

for file in file_list:

    country = file.split('_')[0]
    if country not in countries:
        countries[country] = 0
    else:
        countries[country] += 1

    src_image = f"{local_data_dir}/v1/ProcessedS1/{file}"
    val_image_dir = f"{local_data_dir}/v{os.environ['VERSION']}/images/val/{country}"

    scr_mask = f"{local_data_dir}/v1/ProcessedLabelHand/{file}"
    mask_dir = f"{local_data_dir}/v{os.environ['VERSION']}/masks/val/{country}"

    if not os.path.exists(val_image_dir):
        os.makedirs(val_image_dir)

    if not os.path.exists(mask_dir):
        os.makedirs(mask_dir)
        
    shutil.copyfile(src_image, os.path.join(val_image_dir, file))
    shutil.copyfile(scr_mask, os.path.join(mask_dir, file))

    os.makedirs(f"{local_data_dir}/v{os.environ['VERSION']}/results", exist_ok=True)
    result_file = f"{local_data_dir}/v{os.environ['VERSION']}/results/data_distribution.json"

    with open(result_file, 'w') as output_file:
        json.dump(dict(sorted(countries.items(), key=lambda item: item[1])), output_file, indent=2)