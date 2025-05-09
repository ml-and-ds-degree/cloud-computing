#!/bin/bash

# Start LocalStack in the background
echo "Starting LocalStack..."
localstack -p localstack start -d

# Wait for LocalStack to be ready
echo "Waiting for LocalStack to be ready..."
localstack wait -t 30

echo "Setup complete! LocalStack is running."
