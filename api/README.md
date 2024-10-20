# GitHub Repository Manager API

This is the API service for the GitHub Repository Manager, built with Node.js and Express.

## Features

- Provides an endpoint to list available GitHub management scripts
- Serves as an intermediary between the frontend and the backend

## Getting Started

### Prerequisites

- Node.js (v14 or later)
- npm (comes with Node.js)

### Installation

1. Navigate to the `api` directory.
2. Run `npm install` to install dependencies.

### Running the Application

1. For development:
   - Run `npm run dev` (if you have nodemon installed)
   - Or run `node server.js`
2. The API will be available at `http://localhost:3001`

### Docker

The API is also configured to run in a Docker container. See the root `docker-compose.yml` file for details.

## API Endpoints

- `GET /api/scripts`: Returns a list of available GitHub management scripts

## Adding New Scripts

To add a new script:

1. Create a new Python script in the `backend/scripts/` directory.
2. The API will automatically detect and list the new script.
