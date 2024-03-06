# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

RUN pip install --no-cache-dir fastapi pymongo uvicorn
RUN pip install Flask-Swagger-UI

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
