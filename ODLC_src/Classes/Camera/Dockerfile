# Use the official Python image from Docker Hub
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Install any necessary dependencies
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx 

# Install Python dependencies
RUN pip install opencv-python   

# Create a non-root user with UID 5678 and add it to the video group
RUN adduser -u 5678 --disabled-password --gecos "" appuser && \
    adduser appuser video

# Copy your application code into the container
COPY . /app

# Change the ownership of the app directory to the non-root user
RUN chown -R appuser /app

# Switch to the non-root user
USER appuser

# Run the script to interact with the camera device when the container starts
CMD ["python", "/app/Camera.py"]
