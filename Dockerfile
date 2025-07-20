# Use a lightweight Python base image
FROM python:3.9-slim

# Set the platform to ensure AMD64 compatibility
PLATFORM linux/amd64

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Command to run the main script when the container starts
CMD ["python", "main.py"]