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

# Copy the start script
COPY start_telemetry.sh /usr/app/start_telemetry.sh
RUN chmod +x /usr/app/start_telemetry.sh

# Start the telemetry services
CMD ["/usr/app/start_telemetry.sh"]
