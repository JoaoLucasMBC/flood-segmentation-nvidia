#!/bin/bash

# Add /model to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:/workspace/model

# Check if RUN_MODE is set to jupyter or inference
if [ "$RUN_MODE" = "jupyter" ]; then
  echo "Starting JupyterLab in /workspace..."
  jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --notebook-dir=/workspace
else
  echo "Running model inference..."
  python /workspace/model/model.py
fi