# Use an official Python runtime as a parent image
FROM python:3.12-slim

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

# Make ports 80 and 443 available to the world outside this container
EXPOSE 80 443

# Run the application
CMD ["gunicorn", "-b", "0.0.0.0:8000", "HPGameApi.wsgi:application"]
