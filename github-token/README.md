# GitHub Token Updater Service

This service is part of the GitHub Repository Manager project. It provides a simple web interface for updating the GitHub token used by the main application.

## Purpose

The Token Updater Service allows users to update their GitHub personal access token without needing to modify the `.env` file directly or restart the application. This is particularly useful when tokens expire or need to be rotated for security reasons.

## Features

- Web interface for updating the GitHub token
- Automatic update of the `.env` file
- Seamless integration with the main GitHub Repository Manager application

## Setup

This service is typically run as part of the Docker Compose setup of the main project. However, if you need to run it standalone:

1. Ensure you have Node.js installed (version 14 or later recommended).
2. Navigate to the `token-updater` directory.
3. Install dependencies:
   ```
   npm install
   ```
4. Start the service:
   ```
   npm start
   ```

## Usage

1. Access the Token Updater interface at `http://localhost:3002` (or the appropriate host/port if modified).
2. Enter your new GitHub personal access token in the provided input field.
3. Click "Update Token" to save the new token.
4. You should see a confirmation message if the token was updated successfully.
5. Use the link provided to return to the main GitHub Repository Manager application.

## File Structure

- `server.js`: The main Node.js server file that handles token updates.
- `public/index.html`: The HTML file for the web interface.
- `Dockerfile`: Used for containerizing the service.
- `package.json`: Defines the project dependencies and scripts.

## Environment Variables

This service expects to find a `.env` file in the parent directory. It will update the `GITHUB_TOKEN` variable in this file.

## Security Considerations

- This service should only be exposed on trusted networks.
- In a production environment, additional authentication and encryption measures should be implemented.
- Ensure that the `.env` file has appropriate read/write permissions.

## Troubleshooting

If you encounter issues:

1. Check that the service has write permissions to the `.env` file.
2. Ensure the correct path to the `.env` file is set in `server.js`.
3. Verify that the service is running and accessible at the expected URL.

For more detailed logs, you can run the service with additional logging:

```
NODE_ENV=development node server.js
```
