#!/bin/bash

# Check if RUN_MODE is set to jupyter or inference
if [ "$RUN_MODE" = "jupyter" ]; then
  echo "Starting JupyterLab..."
  jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
else
  echo "Running model inference..."
  python model.py
fi