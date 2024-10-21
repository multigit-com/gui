#!/bin/bash

API_URL="http://localhost:3001"

echo "Testing API endpoints..."

# Test GET /api/repository-files
echo "Testing GET /api/repository-files"
curl -s -X GET "${API_URL}/api/repository-files?repo=test/repo" | jq .

# Test GET /api/readme
echo "Testing GET /api/readme"
curl -s -X GET "${API_URL}/api/readme?repo=test/repo" | jq .

# Test POST /api/move-repository
echo "Testing POST /api/move-repository"
curl -s -X POST "${API_URL}/api/move-repository" \
     -H "Content-Type: application/json" \
     -d '{"repoId":"123","sourceOrgId":"org1","targetOrgId":"org2"}' | jq .

echo "API tests completed."
