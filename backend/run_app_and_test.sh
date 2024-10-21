#!/bin/bash

# Start the application in the background
python app.py &

# Store the PID of the app
APP_PID=$!

# Wait for the app to start (adjust the sleep time if needed)
sleep 5

# Run the integration tests
python -m unittest tests.test_app_integration

# Capture the exit code of the tests
TEST_EXIT_CODE=$?

# Kill the application
kill $APP_PID

# Exit with the test exit code
exit $TEST_EXIT_CODE
