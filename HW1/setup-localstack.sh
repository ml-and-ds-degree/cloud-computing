#!/bin/bash

# Start LocalStack in the background
echo "Starting LocalStack..."
localstack -p localstack start -d

# Wait for LocalStack to be ready
echo "Waiting for LocalStack to be ready..."
localstack wait -t 30

# Create DynamoDB table
echo "Creating DynamoDB table..."
awslocal dynamodb create-table \
    --table-name Tickets \
    --attribute-definitions AttributeName=ticketId,AttributeType=S \
    --key-schema AttributeName=ticketId,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST

# Verify table creation
echo "Verifying table creation..."
awslocal dynamodb list-tables

echo "Setup complete! LocalStack is running and the Tickets table has been created." 