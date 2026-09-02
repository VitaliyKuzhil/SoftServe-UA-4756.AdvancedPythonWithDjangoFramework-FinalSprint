# syntax=docker/dockerfile:1

# Set root image
FROM python:3.10.12-alpine

# Set image author
LABEL authors="Vitalii Kuzhil"

# Set image version
LABEL version="1.0"

# Set work directory for container
WORKDIR /app

# Set settings environments
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy only requirements to docker cache
COPY requirements.txt .

# Run command into container (Install dependencies)
RUN pip install -r requirements.txt

# Copy project (. - current position) into WORKDIR
COPY . .

# Set inside port
EXPOSE ${DJANGO_LISTEN_PORT}