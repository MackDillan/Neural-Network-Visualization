# Use the official Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the database initialization script into the container
COPY ./init /app/init

# Install pymongo (MongoDB client for Python)
RUN pip install pymongo

# Expose the application port (default for Django)
EXPOSE 8000

# Run MongoDB initialization script and then start Django server
CMD ["sh", "-c", "python /app/init/init_db.py && python manage.py runserver 0.0.0.0:8000"]

