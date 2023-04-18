FROM python:3.10

WORKDIR /app

# Copy over contents from local directory to the path in Docker container
COPY . /app/

# Install python requirements from requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /app/api

# Start uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]