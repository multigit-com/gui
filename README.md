# GitHub Repository Manager

This application allows users to manage GitHub repositories across different organizations.

## Features

- View repositories from multiple GitHub organizations
- Move repositories between organizations
- Remove repositories
- View repository details including file list and README content

## Setup

1. Clone the repository
2. Install dependencies:   ```
   npm install   ```
3. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add your GitHub token: `GITHUB_TOKEN=your_token_here`

## Running the Application

1. Start the backend server:   ```
   python backend/app.py   ```
2. Start the frontend server:   ```
   npm start   ```
3. Open your browser and navigate to `http://localhost:3000`

## Testing

Run the tests with:
