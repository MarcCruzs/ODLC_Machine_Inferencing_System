#!/bin/bash

# Define an array of services
services=("shape_human" "color" "alphanumeric")

# Loop through each service and build the Docker image if it doesn't exist
for service in "${services[@]}"; do
  image_name="${service}-image"

  echo "Checking if Docker image for $service exists..."
  
  # Check if the Docker image already exists
  if [[ "$(docker images -q $image_name 2> /dev/null)" == "" ]]; then
    echo "Docker image for $service does not exist. Building the image..."
    
    # Navigate to the service directory
    cd $service

    # Build the Docker image
    docker build -t $image_name .

    # Check if the build was successful
    if [ $? -ne 0 ]; then
      echo "Failed to build Docker image for $service"
      exit 1
    fi

    # Navigate back to the root directory
    cd ..

    echo "Successfully built Docker image for $service"
  else
    echo "Docker image for $service already exists. Skipping build."
  fi
done

echo "All Docker images checked and built if necessary"

# Start the services using docker-compose
echo "Starting services with docker-compose..."
docker-compose up -d

# Check if docker-compose up was successful
if [ $? -ne 0 ]; then
  echo "Failed to start services with docker-compose"
  exit 1
fi

echo "Services started successfully with docker-compose"
