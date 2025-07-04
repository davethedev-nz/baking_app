# Base image with Python 3.12
FROM python:3.12-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies (needed for psycopg2, WeasyPrint, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libjpeg-dev \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libfreetype6 \
    libharfbuzz0b \
    libfribidi0 \
    fonts-liberation \
    curl \
    wkhtmltopdf \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the project code
COPY . .

# Collect static files (optional, depends on your use case)
# RUN python manage.py collectstatic --noinput

# Run the Django app with Gunicorn
CMD ["gunicorn", "member_management.wsgi:application", "--bind", "0.0.0.0:8000"]

