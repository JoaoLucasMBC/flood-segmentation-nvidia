# **Steps to Run the Model Inference Docker Container**

1. Configure environment variables

In the `docker-compose.yaml` file, you can find the `MODEL_PATH`, `/INPUT_FOLDER`, and `OUTPUT_FOLDER` variables. They are used to create volumes that map the model and the respective input images to be used for prediction. Make sure to set these local variables or create a `.env` filee with the correct paths on your local system.

    - `/model`: This volume must contain your model in `.onnx` format.
    - `/input`: This volume should contain the folder with your input images to be processed by the model.
    - `/output`: This volume will store the prediction results.

Also, the user can alter the **RUN_MODE** variable to use the container for *2 different tasks*:

* `inference` - Run a quick inference of the model (as shown above);

* `jupyter` - Run a Jupyter Lab session for data analysis with the model data (more info on the necessary files in the next session).


2. Simply build and run the Docker container with Docker Compose the following command:

    ```sh
    docker compose up
    ```
**Now, you can follow the steps to process the images and generate your predictions!**

# **Steps to Run the Statistics Testing Notebook**

1. Make sure the appropriate data is inserted in the `/data` folder. You will always need 4 folders:  
    1. Images with flooding to be predicted by the model;
    2. Images without flooding to be used to subtract pluvial areas;
    3. An empty folder for the prediction of the flooding;
    4. An empty folder for the prediction of the no-flooding.

2. All images in the folders mentioned above **must be in the following format**:

```sh
/data/example_flood/tile_i_j.png
```

They all must contain the respective rows and columns so you are able to reconstruct the tiles into one full image of the affected region.

*OBS: there is a sample notebook that can be used to collect Sentinel-1 imagery using our own `sentinel-downloader` API. Feel free to use it if you do not have imagees of your own!*

3. Download a **population density map**

The notebook contain an example of the usage of a map from [World Pop](https://hub.worldpop.org/geodata/summary?id=44876). You must download your own and leave in the `/data` folder.

4. Export your model as `.onnx` file

The model used for segmentation in this case is exported and loaded as a `onnx`. Make sure to place your model file in the root `/stats` and insert the appropriate path in the notebook.

5. Install all dependencies from `requirements.txt` (if you want to run it locally)

**Now, you can follow the instructions in the `model_testing.ipynb` notebook and create your analysis!**

6. Build and Run the docker container for a configured Jupyter notebook

If you don't want to install all dependencies, you can simply run the docker container and the Jupyter Lab URL to run the testing. The entire `/stats` folder will be a volume inside of the container.