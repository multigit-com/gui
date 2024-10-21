# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Curl tests for API and backend endpoints
- New `curl-tests` service in Docker Compose
- Button in frontend to trigger curl tests
- Unit tests for backend (Flask app) using pytest
- Unit tests for API (Node.js app) using Jest
- New endpoints in backend for fetching repository files and README content
- Improved error handling and logging in backend and frontend
- Drag and drop functionality for moving repositories between organizations
- Trash column for removing repositories
- File list and README preview on repository hover

### Changed
- Updated Docker Compose configuration to include test services
- Modified frontend to handle potential errors more gracefully
- Refactored backend to use separate scripts for different functionalities
- Updated environment variables to include test-related configurations
- Improved API error responses and logging

### Fixed
- Issue with API URL not being properly set in frontend
- Error handling for missing or invalid data in API responses
- Repository move functionality to use the correct backend script

## [0.2.0] - 2023-05-21

### Added
- Drag-and-drop functionality for moving repositories between organizations
- Frontend tests using Jest and Puppeteer
- Backend unit tests for repository operations
- Pagination support for organization listing

### Changed
- Refactored frontend code for better modularity
- Updated API endpoints to support new features
- Improved error handling and logging in backend scripts

### Fixed
- Issues with GitHub token authentication
- Bug in repository listing for large organizations

## [0.1.0] - 2023-05-15

### Added
- Initial project setup
- Basic frontend for displaying organizations and repositories
- Backend API for interacting with GitHub
- Scripts for listing organizations and repositories
- Docker setup for easy deployment

### Changed
- N/A

### Fixed
- N/A
