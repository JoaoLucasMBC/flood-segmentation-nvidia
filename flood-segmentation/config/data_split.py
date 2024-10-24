from random import sample
import shutil
from dotenv import load_dotenv
import os

load_dotenv()

# define split ratio
split=0.75

# get all images
file_list=os.listdir(f"{os.environ['LOCAL_DATA_DIR']}/ProcessedS1")
image_count=len(file_list)
train_image_list=sample(file_list, int(image_count*split))
val_image_list=[file for file in file_list if file not in train_image_list]

os.makedirs(os.path.join(os.environ['LOCAL_DATA_DIR'], 'images', 'train'))
os.makedirs(os.path.join(os.environ['LOCAL_DATA_DIR'], 'images', 'val'))
os.makedirs(os.path.join(os.environ['LOCAL_DATA_DIR'], 'masks', 'train'))
os.makedirs(os.path.join(os.environ['LOCAL_DATA_DIR'], 'masks', 'val'))

# move all training images to train directory
for each_file in train_image_list: 
    if each_file.split('.')[-1]=='png': 
        shutil.copyfile(f"{os.environ['LOCAL_DATA_DIR']}/ProcessedS1/{each_file}", f"{os.environ['LOCAL_DATA_DIR']}/images/train/{each_file}")
        shutil.copyfile(f"{os.environ['LOCAL_DATA_DIR']}/ProcessedLabelHand/{each_file}", f"{os.environ['LOCAL_DATA_DIR']}/masks/train/{each_file}")

# move all validation images to val directory
for each_file in val_image_list: 
    if each_file.split('.')[-1]=='png': 
        shutil.copyfile(f"{os.environ['LOCAL_DATA_DIR']}/ProcessedS1/{each_file}", f"{os.environ['LOCAL_DATA_DIR']}/images/val/{each_file}")
        shutil.copyfile(f"{os.environ['LOCAL_DATA_DIR']}/ProcessedLabelHand/{each_file}", f"{os.environ['LOCAL_DATA_DIR']}/masks/val/{each_file}")
