# Sentinel Downloader
A Python API for downloading and processing Sentinel satellite images efficiently. **It can be used both as a python package and through Docker**.

![sentinel-downloader](https://badge.fury.io/py/sentinel-downloader.svg)

## Table of Contents
1. [Package Installation](#package-installation)
2. [Docker Setup](#docker-setup)
3. [Credential Setup](#credential-setup)
4. [Usage and Features](#usage-and-features)
5. [API Reference](#api-reference)
6. [Contributing](#contributing)
7. [License](#license)

## Package Installation
This section explains how to setup Sentinel Downloader as a python package. If you would rather setup to use it with Docker, go [here](#docker-setup)

Before using the `sentinel-downloader` package, follow these steps to set up a Python environment and install the package.

### 1. Set Up a Virtual Environment (Recommended)
It’s a good practice to create an isolated environment for your project to avoid conflicts with other packages. Here’s how you can do it using `venv` or `mamba`/`conda`:

#### Using `venv` (Python's built-in virtual environment):
```bash
# Create a virtual environment (python3 for Unix-like systems, python for Windows)
python3 -m venv sentinel-downloader-env

# Activate the environment:
# On macOS/Linux:
source sentinel-downloader-env/bin/activate
# On Windows:
sentinel-downloader-env\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```
#### Using `mamba` or `conda`:
```bash
# Create a new environment with Python 3.x
mamba create -n sentinel-downloader-env python=3.x
# or use conda if you're not using mamba:
# conda create -n sentinel-downloader-env python=3.x

# Activate the environment
mamba activate sentinel-downloader-env
```

### 2. Install the `sentinel-downloader` Package:
After setting up your virtual environment, install the sentinel-downloader package using pip:
```bash:
pip install sentinel-downloader
```

## Docker Setup
This section explains how to setup Sentinel Downloader with Docker. If you would rather setup to use it as a package, go [here](#package-installation)

**You need to have [docker](https://docs.docker.com/get-started/get-docker/) installed to use Sentinel Downloader with Docker**.

### 1. Build the Docker Image
First, clone the repository:
```bash
# Clone the repository
git clone git@github.com:JoaoLucasMBC/open-flood.git
```

Once in the root of the cloned repository, navigate to the directory containing the Dockerfile, and then create the docker image:
```bash
cd sentinel-downloader

docker build -t sentinel-downloader:latest .
```

## Credential Setup
Sentinel Downloader improves upon two existing Sentinel Satellite Imagery collecting APIs: sentinelhub-py and earth-engine, 
and therefore you will need to obtain the credentials needed to make requests using these APIs to use it.

### Sentinel 1 - Earth Engine
If you only want to collect Sentinel 1 imagery, you only need to follow the steps described in this section.

-- TODO: ee credentials

### Sentinel 2 - SentinelHub
If you only want to collect Sentinel 1 imagery, you only need to follow the steps described in this section.

-- TODO: sentinelhub credentials

## Usage and Features
Once tou have all setup, you can use Sentinel Downloader by creating a `config.json` file on the same 
directory of the Dockerfile (if you are using it with Docker) or the same file where you will import the package, where you will input the arguments for the image downloading.

### Arguments received by the API
This `config.json` contains the arguments for image downloading. The arguments are as follows:

#### `satellite`
- **Description**: The satellite choosen for image downloading.
- **Type**: `string` in `[sentinel1, sen1, s1]` for only Sentinel 1 images, in `[sentinel2, sen2, s2]` for only Sentinel 2 images, or `both` for both satellites.
- **Required**: Yes
- **Example**: `"both"`

#### `coords`
- **Description**: The bounding box of coordinates that define the area from which you want to download images. If the bounding box is to big, it will be divided automatically
  into images of the size defined in `resolution`.
- **Type**: `tuple` of format `"(nw-lat, nw-lon, se-lat, se-lon)"`.
- **Required**: Yes
- **Example**: `"(-29.971442, -51.245041, -29.8334607725, -51.1070597725)"`

#### `time_interval`
- **Description**: The start and end dates for the interval in which images will be collected.
- **Type**: `tuple` of format `'("YYYY-MM-DD", "YYYY-MM-DD")'` where the first date is the starting date of the interval, and the second, the end date.
- **Required**: Yes
- **Example**: `"('2024-04-30', '2024-05-10')"`

#### `resolution`
- **Description**: The size of the images in pixels.
- **Type**: `integer` in `[128, 256, 512]` for Sentinel 1 or `[128, 256, 512, 1024, 2048]` for Sentinel 2. If you are collecting images from both satellites at the same time, the 
  resolution must fit both satellites, which means only the avaiable resolutions for Sentinel 1 are valid.
- **Required**: No
- **Default**: `512`
- **Example**: `512`

#### `save_dir`
- **Description**: The name of the directory created inside `output` to save the images.
- **Type**: any `string`.
- **Required**: No
- **Default**: The exact timestamp when the code was ran.
- **Example**: `canoas-images`

#### `filename`
- **Description**: The prefix of all files saved by Sentinel Downloader. It will be used to save images by their tiles (e.g. <filename>_0_0.png, <filename>_3_3.png)
- **Type**: any `string`.
- **Required**: No
- **Default**: `"file"`
- **Example**: `"canoas_images"`

#### `evalscript` (EXCLUSIVE TO SENTINEL 2)
- **Description**: Custom scripts to highlight specific pixels based on classifications provided by sentinelhub. The pixels are then painted with a representative color.
- **Type**: `string` in `["rgb", "water", "vegetation", "urban", "water"]`.
- **Required**: No
- **Default**: `"rgb"`
- **Example**: `"rgb"`

The evalscript paints over the classified pixels to highlight them:

--TODO: put images of evalscript being used


#### `cloud_removal` (EXCLUSIVE TO SENTINEL 2)
- **Description**: Usage of a script developed for Sentinel Downloader that chooses the least cloud obstructed image in the time interval selected.
- **Type**: `boolean` between `true`or `false`
- **Required**: No
- **Default**: `false`
- **Example**: `true`

The difference between the image returned by the API with and without the cloud removal script:

--TODO: put comparision of cloud obstructed image and clear image

### Example config.json file
An example of how your config.json file should look like is as follows:
```json
{
    "satellite": "both",
    "coords": "(-29.8334607725, -51.245041, -29.971442, -51.1070597725)",
    "time_interval": "('2024-04-30', '2024-05-10')",
    "save_dire": "canoas",
    "filename": "canoas_image",
    "evalscript": "vegetation",
    "cloud_removal": true
}
```

