# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set workspace directory in container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

# Copy project files
COPY . /app/

# Run collectstatic to compile static files
RUN python manage.py collectstatic --noinput

# Expose Django port
EXPOSE 8000

# Start Gunicorn server in production, running migrations first
CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 job.wsgi:application"]
