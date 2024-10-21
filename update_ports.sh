#!/bin/bash

CONFIG_FILE="frontend/public/config.json"

# Function to update or add a key-value pair in .env file
update_env() {
    key=$1
    value=$2
    if grep -q "^$key=" .env; then
        sed -i "s|^$key=.*|$key=$value|" .env
    else
        echo "$key=$value" >> .env
    fi
}

# Update Frontend port
if [ ! -z "$1" ]; then
    update_env "FRONTEND_PORT" $1
fi

# Update API port
if [ ! -z "$2" ]; then
    update_env "API_PORT" $2
    update_env "REACT_APP_API_URL" "http://\${API_HOSTNAME}:$2"
fi

# Update Backend port
if [ ! -z "$3" ]; then
    update_env "BACKEND_PORT" $3
    update_env "API_BACKEND_URL" "http://\${BACKEND_HOSTNAME}:$3"
fi

# Update curl test configuration
if [ ! -z "${CURL_TEST_ENABLED}" ]; then
    update_env "CURL_TEST_ENABLED" ${CURL_TEST_ENABLED}
fi

# Update Ansible configuration
if [ ! -z "${ANSIBLE_ENABLED}" ]; then
    update_env "ANSIBLE_ENABLED" ${ANSIBLE_ENABLED}
fi

echo "Ports updated in .env file"
