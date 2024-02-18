# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /usr/src/app

COPY . /usr/src/app/
# Install dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip install --upgrade pip
RUN pip install  -r requirements.txt

# Copy project

# Run the application
CMD ["gunicorn", "-b", "0.0.0.0:8000", "HPGameApi.wsgi:application"]
