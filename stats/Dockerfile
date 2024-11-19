# Use the base python image
FROM python:3.10.12-slim

# Install system dependencies for GDAL and build tools
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    build-essential \
    gcc \
    g++ \
    && apt-get clean

# Set GDAL environment variables
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Copy the requirements file
COPY ./requirements.txt /

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install JupyterLab
RUN pip install jupyterlab

# Set the working directory
WORKDIR /

# Ensure Python recognizes it as a package
ENV PYTHONPATH="/"

# Expose port for JupyterLab
EXPOSE 8888

# Copy a script to decide what to run
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the default command to the script
CMD ["/entrypoint.sh"]