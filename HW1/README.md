# Parking Lot Serverless API (HW1)

## What We've Done

This project implements a simple serverless parking lot management system using AWS SAM (Serverless Application Model). It provides two main HTTP API endpoints:

- **/entry**: Register a car's entry into a parking lot, generating a unique ticket ID.
- **/exit**: Register a car's exit, calculate the parking duration and charge, and remove the ticket from the system.

The backend is built with Python 3.12 AWS Lambda functions and uses DynamoDB for ticket storage. The infrastructure is defined in `parking-lot.template.yaml`.

## Homework Folder Structure

```
📁 HW1
├── 📁 src
│   ├── 📄 entry_handler.py     # Lambda for car entry (creates ticket)
│   ├── 📄 exit_handler.py      # Lambda for car exit (calculates charge, deletes ticket)
│   └── 📄 requirements.txt     # Python dependencies for Lambdas
├── 📄 parking-lot.template.yaml     # AWS SAM template (defines APIs, Lambdas, DynamoDB)
├── 📄 create-dynamo-table.sh   # Script to create DynamoDB table locally (for LocalStack)
└── 📁 tests
    └── 📄 manual.rest          # Example HTTP requests for manual testing
```

## How to Run Everything

### Prerequisites
- Docker (for local development)

### 1. Development Environment Setup

#### Option A: Local Development
1. Clone this repository
2. Open in VS Code with the Remote - Containers extension
3. When prompted, click "Reopen in Container" to start the development environment

#### Option B: Using GitHub Codespaces
Open this repository in GitHub Codespaces for a pre-configured development environment with all dependencies (including Docker) ready to use.

### 2. Start the Development Environment
Simply run: `task hw1:start`

### 3. Testing the API
- Use the sample requests in `tests/manual.rest` with a REST client (e.g., VSCode REST Client extension).
- Example entry:
  ```http
  POST http://localhost:3000/entry?plate=ABC-123&parkingLot=LotA
  ```
- Example exit:
  ```http
  POST http://localhost:3000/exit?ticketId=<your_ticket_id>
  ```

### 4. Deploy to AWS
To deploy the application to AWS:

1. Ensure you have AWS credentials configured

2. Run one of the following commands:
   ```bash
   # Deploy to AWS
   sam deploy -t HW1/parking-lot.template.yaml

   # Or deploy to LocalStack for testing
   samlocal deploy -t HW1/parking-lot.template.yaml
   ```
3. Follow the prompts to:
   - Choose a stack name
   - Select the AWS region
   - Confirm the changes

Note: The deployment will create:
- An HTTP API Gateway
- A DynamoDB table
- Lambda functions for entry and exit operations
- Required IAM roles and permissions
