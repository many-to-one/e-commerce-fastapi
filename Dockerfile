FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# RUN python generate_secret_key.py

COPY . .
RUN chmod +x entrypoint.sh