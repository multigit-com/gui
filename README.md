# GitHub Repository Manager

This project is a web application that allows users to manage GitHub repositories through a user-friendly interface. It consists of three main components: a React frontend, a Python Flask backend, and a Node.js API.

## Project Structure

- `frontend/`: React application for the user interface
- `backend/`: Python Flask application for executing GitHub-related scripts
- `api/`: Node.js API for listing available scripts
- `docker-compose.yml`: Docker Compose configuration for running all services

## Getting Started

1. Ensure you have Docker and Docker Compose installed on your system.
2. Clone this repository.
3. Create a `.env` file in the root directory and add your GitHub token:   ```
   GITHUB_TOKEN=your_github_personal_access_token_here   ```
4. Run `docker-compose up --build` to start all services.
5. Access the application at `http://localhost:3000` in your web browser.

For more detailed information about each component, please refer to the README files in their respective directories.

```
project/
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── public/
│   └── src/
│       ├── App.js
│       └── index.js
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py
│   └── scripts/
│       ├── remove_repository_from_github_by_url_repo.py
│       └── create_repository_on_github.py
├── api/
│   ├── Dockerfile
│   ├── package.json
│   └── server.js
├── docker-compose.yml
└── .env
