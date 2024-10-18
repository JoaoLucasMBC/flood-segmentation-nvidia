# Use the base python image
FROM python:3.10.12-slim

# Copy the whole directory
COPY ./requirements.txt /

# Install dependencies
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