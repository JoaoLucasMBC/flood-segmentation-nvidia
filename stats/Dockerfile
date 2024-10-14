FROM python:3.10.12-slim

# Copy the whole directory sentinel_downloader
COPY ./model /

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements_model.txt


# Set the working directory
WORKDIR /

# Ensure Python recognizes it as a package
ENV PYTHONPATH="/"

# Run the script as a module
CMD ["python", "model.py"]