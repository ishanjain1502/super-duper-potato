FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install Redis server
RUN apt-get update && apt-get install -y redis-server

# Install dependencies
COPY requirements.txt .
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2 \
    && apt-get install -y redis-server
RUN pip install redis
RUN pip install --no-cache-dir -r requirements.txt

# Copy FastAPI code from root directory
COPY main.py .
COPY utils/ ./utils/

# Start Redis in the background and FastAPI using uvicorn
CMD redis-server --daemonize yes && uvicorn main:app --host 0.0.0.0 --port 8000
