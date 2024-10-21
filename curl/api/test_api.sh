#!/bin/bash

API_URL="http://localhost:3001"
ORG_REPO="apicup/get"

echo "Testing API endpoints..."

# Test GET /api/repository-files
echo "Testing GET /api/repository-files"
curl -s -X GET "${API_URL}/api/repository-files?repo=${ORG_REPO}" | jq .

# Test GET /api/readme
echo "Testing GET /api/readme"
curl -s -X GET "${API_URL}/api/readme?repo=${ORG_REPO}" | jq .

echo "API tests completed."
