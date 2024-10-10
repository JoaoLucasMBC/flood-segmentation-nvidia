# **Steps to Run the Statistics Testing**

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

3. Download a **population density map**

The notebook contain an example of the usage of a map from [World Pop](https://hub.worldpop.org/geodata/summary?id=44876). You must download your own and leave in the `/data` folder.

4. Export your model as `.onnx` file

The model used for segmentation in this case is exported and loaded as a `onnx`. Make sure to place your model file in the root `/stats` and insert the appropriate path in the notebook.

5. Install all dependencies from `requirements.txt`

**Now, you can follow the instructions in the `model_testing.ipynb` notebook and create your analysis!**