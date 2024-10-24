from sentinel_downloader import SentinelDownloader
import os
import json
import datetime
from dotenv import load_dotenv

def download_task(link, data, initial_date, final_date):
    s = SentinelDownloader(mode="cli", cli_args=["-s", "sen2", 
                                                    "-c", f"({data['bbox'][3]}, {data['bbox'][0]}, {data['bbox'][1]}, {data['bbox'][2]})", 
                                                    "-t", f"('{initial_date.strftime('%Y-%m-%d')}', '{final_date.strftime('%Y-%m-%d')}')",
                                                    "-cr", "true",
                                                    "-sd", link.split("/")[-1].split(".")[0]])
    s.run()

# Define the root directory
root_dir = "./catalog"

load_dotenv()

with open("./catalog/sen1floods11_hand_labeled_source/collection.json", "r") as f:
    data = json.load(f)

links = []

for link in data["links"]:
    if link["rel"] not in ["root", "parent"]:
        links.append(os.path.join("./catalog/sen1floods11_hand_labeled_source", link["href"][2:]))

for link in links:
    with open(link, 'r') as f:
        data = json.load(f)

    initial_date = datetime.datetime.strptime(data["properties"]["datetime"][:10], "%Y-%m-%d") - datetime.timedelta(days=2)
    final_date = initial_date + datetime.timedelta(days=30)

    download_task(link, data, initial_date, final_date)