#!/bin/bash

# Exit on the first error
set -e

# Configuration
IMAGE_NAME="events-backend-app"
CONTAINER_NAME="events-backend-app-container"
export EVENTS_VOLUME_PATH="/home/hassan/events/" # Change this to your own path of the events images volume
# Check if the Docker image exists
check_image() {
    echo "Checking Docker image..."
    if ["$(docker images -q $IMAGE_NAME 2> /dev/null)" == ""]; then
        return 1
    else
        return 0
    fi
}

# Build the Docker image
build_image() {
    echo "Building Docker image..."
    docker build -t $IMAGE_NAME .
}

# Check if the Docker container is running
check_container() {
    echo "Checking Docker container..."
    if ["$(docker ps -q -f name=$CONTAINER_NAME 2> /dev/null)" == ""]; then
        return 1
    else
        return 0
    fi
}

# Run the Docker container # Must use 8000 as external port otherwise images won't load
run_container() {
    echo "Running Docker container..."
    docker run -d --name $CONTAINER_NAME -p 8000:8000 -v $EVENTS_VOLUME_PATH:/code/integreat_cms/media/global $IMAGE_NAME
}

# Main script
main() {
    if ! check_image; then
        build_image
    fi
    if ! check_container; then
        run_container
    fi
}

# Run the main script
main
