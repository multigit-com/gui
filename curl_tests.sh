#!/bin/bash

API_URL="http://localhost:3001"
GITHUB_TOKEN="your_github_token_here"

# Function to run a test
run_test() {
    echo "Running test: $1"
    eval "$2"
    echo "------------------------"
}

# Test GET /api/organizations
run_test "Get Organizations" "curl -s -H 'Authorization: token $GITHUB_TOKEN' $API_URL/api/organizations"

# Test GET /api/repositories
run_test "Get Repositories" "curl -s -H 'Authorization: token $GITHUB_TOKEN' $API_URL/api/repositories?org=your_org_name"

# Test GET /api/repository-files
run_test "Get Repository Files" "curl -s -H 'Authorization: token $GITHUB_TOKEN' $API_URL/api/repository-files?org=your_org_name&repo=your_repo_name"

# Test GET /api/readme
run_test "Get README" "curl -s -H 'Authorization: token $GITHUB_TOKEN' $API_URL/api/readme?org=your_org_name&repo=your_repo_name"

# Test POST /api/move-repository
run_test "Move Repository" "curl -s -X POST -H 'Content-Type: application/json' -H 'Authorization: token $GITHUB_TOKEN' -d '{\"repoId\":\"repo_id\",\"repoName\":\"repo_name\",\"sourceOrgId\":\"source_org\",\"targetOrgId\":\"target_org\"}' $API_URL/api/move-repository"

# Test POST /api/remove-repository
run_test "Remove Repository" "curl -s -X POST -H 'Content-Type: application/json' -H 'Authorization: token $GITHUB_TOKEN' -d '{\"repoUrl\":\"https://github.com/org/repo\",\"sourceOrgId\":\"org_name\"}' $API_URL/api/remove-repository"

# Test POST /api/rename-organization
run_test "Rename Organization" "curl -s -X POST -H 'Content-Type: application/json' -H 'Authorization: token $GITHUB_TOKEN' -d '{\"orgId\":\"org_id\",\"newName\":\"new_org_name\"}' $API_URL/api/rename-organization"

# Test POST /api/rename-repository
run_test "Rename Repository" "curl -s -X POST -H 'Content-Type: application/json' -H 'Authorization: token $GITHUB_TOKEN' -d '{\"orgName\":\"org_name\",\"oldName\":\"old_repo_name\",\"newName\":\"new_repo_name\"}' $API_URL/api/rename-repository"

# Test POST /api/remove-organization
run_test "Remove Organization" "curl -s -X POST -H 'Content-Type: application/json' -H 'Authorization: token $GITHUB_TOKEN' -d '{\"orgId\":\"org_id\"}' $API_URL/api/remove-organization"
