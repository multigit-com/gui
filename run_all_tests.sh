#!/bin/bash

# Set the base directory to the script's location
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Function to run tests and check result
run_test() {
    echo "Running $1..."
    if eval "$2"; then
        echo "$1 passed"
        return 0
    else
        echo "$1 failed"
        return 1
    fi
}

# Initialize counters
PASSED=0
FAILED=0

# Backend unit tests
if run_test "Backend unit tests" "cd ${BASE_DIR}/backend && python -m pytest"; then
    ((PASSED++))
else
    ((FAILED++))
fi

# Frontend unit tests
if run_test "Frontend unit tests" "cd ${BASE_DIR}/frontend && npm test"; then
    ((PASSED++))
else
    ((FAILED++))
fi

# API tests
if run_test "API tests" "cd ${BASE_DIR}/ansible && ansible-playbook api_tests.yml"; then
    ((PASSED++))
else
    ((FAILED++))
fi

# Curl tests
if run_test "Curl tests" "cd ${BASE_DIR}/curl/backend && ./curl_tests.sh"; then
    ((PASSED++))
else
    ((FAILED++))
fi

# Ansible tests
if run_test "Ansible tests" "cd ${BASE_DIR}/ansible && ansible-playbook run_tests.yml"; then
    ((PASSED++))
else
    ((FAILED++))
fi

# Print summary
echo "Test Summary:"
echo "Passed: $PASSED"
echo "Failed: $FAILED"

# Exit with status code 1 if any tests failed
if [ $FAILED -gt 0 ]; then
    exit 1
else
    exit 0
fi
