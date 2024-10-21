#!/bin/bash

# Load environment variables
source .env

# Function to run a test
run_test() {
    echo "Running test: $1"
    eval "$2"
    echo "------------------------"
}

# Test GET /api/organizations
run_test "Get Organizations" "curl -s -H 'Authorization: token $GITHUB_TOKEN' $API_URL/api/organizations"

# Test GET /api/repositories
run_test "Get Repositories" "curl -s -H 'Authorization: token $GITHUB_TOKEN' $API_URL/api/repositories?org=$TEST_ORG"

# Test GET /api/repository-files
run_test "Get Repository Files" "curl -s -H 'Authorization: token $GITHUB_TOKEN' $API_URL/api/repository-files?org=$TEST_ORG&repo=$TEST_REPO"

# Test GET /api/readme
run_test "Get README" "curl -s -H 'Authorization: token $GITHUB_TOKEN' $API_URL/api/readme?org=$TEST_ORG&repo=$TEST_REPO"

# Test POST /api/move-repository
run_test "Move Repository" "curl -s -X POST -H 'Content-Type: application/json' -H 'Authorization: token $GITHUB_TOKEN' -d '{\"repoId\":\"$TEST_REPO_ID\",\"repoName\":\"$TEST_REPO\",\"sourceOrgId\":\"$TEST_SOURCE_ORG\",\"targetOrgId\":\"$TEST_TARGET_ORG\"}' $API_URL/api/move-repository"

# Test POST /api/remove-repository
run_test "Remove Repository" "curl -s -X POST -H 'Content-Type: application/json' -H 'Authorization: token $GITHUB_TOKEN' -d '{\"repoUrl\":\"$TEST_REPO_URL\",\"sourceOrgId\":\"$TEST_ORG\"}' $API_URL/api/remove-repository"

# Test POST /api/rename-organization
run_test "Rename Organization" "curl -s -X POST -H 'Content-Type: application/json' -H 'Authorization: token $GITHUB_TOKEN' -d '{\"orgId\":\"$TEST_ORG_ID\",\"newName\":\"$TEST_NEW_ORG_NAME\"}' $API_URL/api/rename-organization"

# Test POST /api/rename-repository
run_test "Rename Repository" "curl -s -X POST -H 'Content-Type: application/json' -H 'Authorization: token $GITHUB_TOKEN' -d '{\"orgName\":\"$TEST_ORG\",\"oldName\":\"$TEST_REPO\",\"newName\":\"$TEST_NEW_REPO_NAME\"}' $API_URL/api/rename-repository"

# Test POST /api/remove-organization
run_test "Remove Organization" "curl -s -X POST -H 'Content-Type: application/json' -H 'Authorization: token $GITHUB_TOKEN' -d '{\"orgId\":\"$TEST_ORG_ID\"}' $API_URL/api/remove-organization"
