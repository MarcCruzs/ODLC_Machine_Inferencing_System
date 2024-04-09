# Use the official Python image from Docker Hub
FROM python:3.11

# Install any necessary dependencies
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx  

# Install Python dependencies
RUN pip install opencv-python   

# Set the working directory in the container
WORKDIR /app

# Copy your application code into the container
COPY . /app

# Run the script to interact with the camera device when the container starts
CMD ["python", "/app/Camera.py"]
