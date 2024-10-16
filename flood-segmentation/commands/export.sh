python ../config/configure_env.py
source ../config/.env
python ../../config/create_mount.py
tao model unet export -m $TAO_EXPERIMENT_DIR/resnet18/USA/weights/model.tlt \
                 -e $TAO_SPECS_DIR/resnet18/combined_config.txt \
                 -k $NVIDIA_API_TOKEN \
                 --engine_file $TAO_EXPERIMENT_DIR/export/sample_resnet18.engine \
                 --gen_ds_config
