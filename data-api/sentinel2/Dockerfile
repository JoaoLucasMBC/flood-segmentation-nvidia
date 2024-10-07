FROM python:3.10.12-slim

WORKDIR /sentinel2-api

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

#ENV CLIENT_ID=
#ENV CLIENT_SECRET=


CMD ["python3", "main.py", "-c", "(-30.00, -51.20, -30.05, -51.15)", "-ev", "water", "-t", "('2024-04-26', '2024-05-26')", "-cr", "true", "-s", "/images"]
