FROM python:3.10.12-slim 

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the whole directory sentinel_downloader
COPY ./sentinel_downloader /sentinel_downloader

# Set the working directory
WORKDIR /sentinel_downloader

# Run the script
CMD ["python", "json_runner.py"]