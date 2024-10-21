#!/bin/sh

# Copy the .env file from the parent directory
cp /.env ./.env

# Run the original command
exec "$@"
