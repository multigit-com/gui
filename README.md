# GitHub Repository Manager

This project is a web application that allows users to manage GitHub repositories through a user-friendly interface. It consists of four main components: a React frontend, a Python Flask backend, a Node.js API, and a token updater service.

## Project Structure

- `frontend/`: React application for the user interface
- `backend/`: Python Flask application for executing GitHub-related scripts
- `api/`: Node.js API for listing available scripts
- `token-updater/`: Service for updating the GitHub token
- `docker-compose.yml`: Docker Compose configuration for running all services

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone this repository:   ```
   git clone https://github.com/your-username/github-repository-manager.git
   cd github-repository-manager   ```

2. Create a `.env` file in the root directory with your initial GitHub token:   ```
   GITHUB_TOKEN=your_initial_github_personal_access_token_here   ```

3. Build and start all services:   ```
   docker-compose up --build   ```

4. Access the main application:
   Open http://localhost:3000 in your web browser.

## Using the Application

### Managing GitHub Repositories

1. On the main page (http://localhost:3000), you'll see a dropdown menu with available GitHub management scripts.
2. Select a script from the dropdown (e.g., "remove_repository_from_github_by_url_repo" or "create_repository_on_github").
3. Enter the required input in the text field:
   - For repository removal: Enter the full GitHub repository URL
   - For repository creation: Enter the new repository name
4. Click "Execute" to perform the selected action.
5. The result of the operation will be displayed on the page.

### Updating the GitHub Token

If you need to update your GitHub token:

1. On the main page (http://localhost:3000), click the "Click here to open the Token Updater" link. This will open the Token Updater in a new tab.
2. In the new tab (http://localhost:3002), enter your new GitHub personal access token in the input field.
3. Click "Update Token".
4. You'll see a message confirming that the token has been updated.
5. Use the "Open GitHub Repository Manager" link on the Token Updater page to return to the main application in a new tab.

After updating the token, the backend service will automatically use the new token for subsequent operations. There's no need to restart the services.

## Development

To make changes to the project:

1. Stop the running Docker containers with `Ctrl+C`.
2. Make your changes to the relevant files.
3. Rebuild and restart the services:   ```
   docker-compose up --build   ```

## Troubleshooting

- If you encounter any issues with script execution, check the backend logs:  ```
  docker-compose logs backend  ```

- For frontend issues, check the frontend logs:  ```
  docker-compose logs frontend  ```

- If the token updater is not working, check its logs:  ```
  docker-compose logs token-updater  ```

## Security Note

The token updater service allows updating the GitHub token through a web interface. In a production environment, you should implement proper authentication and encryption to secure this process.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
