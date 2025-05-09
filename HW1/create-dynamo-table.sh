#!/bin/bash

# Exit on any error
set -e

# Create DynamoDB table
echo "Creating DynamoDB table..."
if ! awslocal dynamodb create-table \
    --table-name Tickets \
    --attribute-definitions AttributeName=ticketId,AttributeType=S \
    --key-schema AttributeName=ticketId,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --no-cli-pager; then
    echo "Error creating DynamoDB table"
    exit 1
fi

# Verify table creation
echo "Verifying table creation..."
if ! awslocal dynamodb list-tables; then
    echo "Error verifying table creation"
    exit 1
fi

echo "Setup complete! The Tickets table has been created."
