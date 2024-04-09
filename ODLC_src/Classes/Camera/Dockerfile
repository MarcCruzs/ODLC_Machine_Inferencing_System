FROM python:3.11.0

# Add the user to the video group
RUN usermod -aG video root

# Install any necessary dependencies
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    && pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy your application code into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# RUN adduser -u 5678 --disabled-password --gecos "" appuser && \
#     adduser appuser video && \
#     chown -R appuser /app

# Switch to the non-root user
USER appuser

# Run the script to interact with the camera device when the container starts
# CMD ["python", "/app/Camera.py"]
