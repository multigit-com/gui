#!/bin/bash

BACKEND_URL="http://localhost:5000"
ORG_REPO="apicup/get"

echo "Testing Backend endpoints..."

# Test GET /api/repository-files
echo "Testing GET /api/repository-files"
curl -s -X GET "${BACKEND_URL}/api/repository-files?repo=${ORG_REPO}" | jq .

# Test GET /api/readme
echo "Testing GET /api/readme"
curl -s -X GET "${BACKEND_URL}/api/readme?repo=${ORG_REPO}" | jq .

echo "Backend tests completed."
