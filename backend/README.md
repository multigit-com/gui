# GitHub Repository Manager Backend

This is the backend application for the GitHub Repository Manager, built with Python and Flask.

## Features

- Executes Python scripts for GitHub repository management
- Provides an API endpoint for script execution
- Handles CORS for frontend communication

## Getting Started

### Prerequisites

- Python 3.9 or later
- pip (Python package manager)

### Installation

1. Navigate to the `backend` directory.
2. (Optional) Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running the Application

1. Set the `GITHUB_TOKEN` environment variable with your GitHub personal access token.
2. Run the application:
   ```
   python app.py
   ```
3. The backend will be available at `http://localhost:5000`

### Docker

The backend is also configured to run in a Docker container. See the root `docker-compose.yml` file for details.

## API Endpoints

- `POST /api/execute`: Executes a specified GitHub management script
  - Request body: `{ "command": "script_name", "input": "script_input" }`
  - Response: JSON object with script execution results

## Scripts

Python scripts for GitHub operations are located in the `scripts/` directory. To add a new operation:

1. Create a new Python script in the `scripts/` directory.
2. The script should accept command-line arguments for input.
3. The script will be automatically available for execution through the API.
