# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       python3-dev \
       gcc \
       libc-dev \
       libjpeg-dev \
       zlib1g-dev \
       libpq-dev \
       && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the Django project files into the working directory
COPY .env /app/
COPY . /app/

# Collect static files
RUN python manage.py makemigrations && python manage.py migrate

# Expose port 8000 to the outside world
EXPOSE 8000

# Define the command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
