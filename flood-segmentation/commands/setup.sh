# Install requirements
pip install -r ../requirements.txt

python ../config/configure_env.py

# Load the .env file
source ../config/.env

# Create mount
python ../config/create_mount.py

# User must have been Docker login

# Creating nvcr.io config
apikey=$NVIDIA_API_KEY
echo ";WARNING - This is a machine generated file.  Do not edit manually." > config
echo ";WARNING - To update local config settings, see \"ngc config set -h\"" >> config
echo "" >> config
echo "[CURRENT]" >> config
echo "apikey=${apikey}" >> config
echo "format_type=json" >> config
echo "org=nvidia" >> config

rm -rf ~/.ngc
mkdir -p ~/.ngc & mv config ~/.ngc/

# Login into NVIDIA ngc
docker login -u '$oauthtoken' -p $apikey nvcr.io

# Download NVIDIA container toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update

sudo apt-get install -y nvidia-container-toolkit

# THIS ASSUMES YOU ALREADY HAVE INSTALLED THE PROPER NVIDIA DRIVERS FOR YOUR GPU

# Creating folders
mkdir -p $LOCAL_PROJECT_DIR
mkdir -p $LOCAL_DATA_DIR/v$VERSION
mkdir -p $LOCAL_SPECS_DIR/v$VERSION
mkdir -p $LOCAL_PROJECT_DIR/v$VERSION

# Pulling the container image and testing
tao model unet --help