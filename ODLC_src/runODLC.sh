#!/bin/bash

images=("shape_human", "color", "alphanumeric")

# Loop through each service and build the Docker image
for images in "${images[@]}"; do
  echo "Building Docker image for $service..."
  
  # Navigate to the service directory
  cd $service

  # Build the Docker image
  docker build -t "$service-image" .

  # Check if the build was successful
  if [ $? -ne 0 ]; then
    echo "Failed to build Docker image for $service"
    exit 1
  fi

  # Navigate back to the root directory
  cd ..

  echo "Successfully built Docker image for $service"
done

echo "All Docker images built successfully"

# Start the services using docker-compose
echo "Starting services with docker-compose..."
docker-compose up -d

# Check if docker-compose up was successful
if [ $? -ne 0 ]; then
  echo "Failed to start services with docker-compose"
  exit 1
fi

echo "Services started successfully with docker-compose"