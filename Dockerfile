# Use a slim Python image
FROM python:3.11-slim

# Prevents Python from writing pyc files & buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies for GeoDjango + PostgreSQL + build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# GDAL environment variables (needed for compilation sometimes)
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Default command: run migrations then start server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
