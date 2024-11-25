# Use the official Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 8000

# Run the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
