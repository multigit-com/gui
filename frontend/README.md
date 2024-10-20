# GitHub Repository Manager Frontend

This is the frontend application for the GitHub Repository Manager, built with React.

## Features

- Displays a list of available GitHub management scripts
- Allows users to select a script and provide input
- Sends requests to the backend to execute selected scripts
- Displays the results of script execution

## Getting Started

### Prerequisites

- Node.js (v14 or later)
- npm (comes with Node.js)

### Installation

1. Navigate to the `frontend` directory.
2. Run `npm install` to install dependencies.

### Running the Application

1. For development:
   - Run `npm start`
   - The application will be available at `http://localhost:3000`

2. For production build:
   - Run `npm run build`
   - Serve the `build` directory with a static file server

### Docker

The frontend is also configured to run in a Docker container. See the root `docker-compose.yml` file for details.

## Environment Variables

- `REACT_APP_API_URL`: URL of the Node.js API (default: `http://localhost:3001`)
- `REACT_APP_BACKEND_URL`: URL of the Python backend (default: `http://localhost:5000`)

These are set in the `docker-compose.yml` file for the Docker setup.
