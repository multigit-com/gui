#!/bin/bash

echo "Starting curl tests..."

# Run API tests
echo "Running API tests..."
bash ./api/test_api.sh

echo ""

# Run Backend tests
echo "Running Backend tests..."
bash ./backend/test_backend.sh

echo "All curl tests completed."
