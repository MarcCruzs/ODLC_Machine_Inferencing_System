# Use the official Python 3.11 image as a base
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/app

# Copy the requirements.txt file into the container at /usr/app
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the working directory contents into the container at /usr/app
COPY . .

RUN chmod +x /usr/app/src/entrypoint.sh

# Define the entrypoint command
ENTRYPOINT ["/usr/app/src/entrypoint.sh"]

# CMD can be overridden by docker-compose command
CMD ["--camera_device", "0"]
