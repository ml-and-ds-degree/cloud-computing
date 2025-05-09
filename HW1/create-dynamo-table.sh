#!/bin/bash

# Exit on any uncaught error
set -e

TABLE_NAME="Tickets"

# Check if the table already exists
if awslocal dynamodb describe-table --table-name "${TABLE_NAME}" >/dev/null 2>&1; then
    echo "✅ DynamoDB table '${TABLE_NAME}' already exists. Exiting."
    exit 0
fi

# Create DynamoDB table
echo "Creating DynamoDB table '${TABLE_NAME}'..."
awslocal dynamodb create-table \
    --table-name "${TABLE_NAME}" \
    --attribute-definitions AttributeName=ticketId,AttributeType=S \
    --key-schema AttributeName=ticketId,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --no-cli-pager \
    || { echo "❌ Error creating DynamoDB table '${TABLE_NAME}'"; exit 1; }

# Wait until the table becomes active (optional but more robust)
echo "Waiting for table to become ACTIVE..."
awslocal dynamodb wait table-exists --table-name "${TABLE_NAME}" \
    || { echo "❌ Table '${TABLE_NAME}' did not become ACTIVE in time"; exit 1; }

echo "🎉 Setup complete! The '${TABLE_NAME}' table has been created and is ACTIVE."
