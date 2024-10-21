# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

### Changed
- Removed 'original_name' and 'custom_name' columns from the organizations table in the database
- Updated organization listing and caching functions to reflect the removed columns
- Modified database schema for organizations table

### Added
- Sorting functionality for organizations by name in the database query

### Fixed
- Issues with multiple API requests for the same data
- Improved handling of GitHub API rate limits
- Resolved issue with database column mismatch in organization caching
- Updated database schema to match current organization data structure


## [0.8.0] - 2024-10-25

### Added
- Enhanced organization information in API response, including original name and custom name
- Environment variable support for custom organization names
- Updated SQLite schema to store additional organization information
- Enhanced organization information in select lists, including counts for public, private, forked, and total repositories
- Updated frontend to display detailed repository counts for each organization
- Environment variables for database configuration and cache duration
- Implemented a 5-minute cache refresh mechanism for repository and organization data
- Added timestamp tracking for cached data in SQLite database
- SQLite caching for organization and repository data
- Fallback to cached data when GitHub API requests fail
- New rename.html page for renaming organizations and repositories
- API endpoints for renaming organizations and repositories
- Scripts for handling organization and repository renaming
- Clickable links for organization and repository names in rename.html
- Error handling and display in rename.html
- Ability to view repositories for a selected organization in rename.html
- Implemented exponential backoff for API rate limit handling
- Improved error handling for rate limit errors

### Changed
- Modified API endpoints to check cache age before making new requests
- Updated UI to show more repository details in blocks.html
- Improved error handling and user feedback across the application
- Enhanced the move repository functionality to prevent multiple simultaneous requests
- Refactored API server (server.js) to use proxy requests for all endpoints
- Removed confirmation prompt when deleting a repository for a more streamlined user experience
- Moved database and cache configuration to environment variables

### Fixed
- Issue with drag and drop functionality for moving repositories
- Error related to repository transfer API usage
- Various minor bug fixes and performance improvements

### Changed
- Refactored backend code to separate utility functions into `utils/database.py` and `utils/github_api.py`
- Refactored API server code to separate proxy request function into `utils/proxyRequest.js`
- Improved code organization and maintainability



## [0.7.0] - 2024-10-25

### Added
- New rename.html page for renaming organizations and repositories
- API endpoints for renaming organizations and repositories
- Clickable links for organization and repository names in rename.html
- Error handling and display in rename.html
- Ability to view repositories for a selected organization in rename.html

### Changed
- Updated frontend code to use 'name' instead of 'login' for organization display and operations
- Modified database queries to use 'name' column instead of 'login' for organization/user name from GitHub
- Updated sorting of organizations to use the 'name' column in the database query
- Improved error handling and user feedback across the application

### Fixed
- Issues with multiple API requests for the same data
- Improved handling of GitHub API rate limits
- Resolved issue with database column mismatch in organization caching
- Updated database schema to match current organization data structure

## [0.6.0] - 2024-10-24

### Added
- Comprehensive TEST.md guide for running all types of tests
- New `run_all_tests.sh` bash script to execute all tests in sequence
- Detailed descriptions of unit tests, integration tests, API tests, curl tests, and end-to-end tests in TEST.md
- Instructions for running individual test types and all tests together
- Guidance on adding new tests and troubleshooting in TEST.md
- Information about continuous integration, performance testing, security testing, and accessibility testing in TEST.md

### Changed
- Updated testing procedures to include new test types and methodologies
- Improved error handling and logging in test scripts
- Enhanced documentation for testing processes

### Fixed
- Issues with test script paths in `run_all_tests.sh`
- Inconsistencies in test environment setup instructions

## [0.5.0] - 2024-10-23

### Added
- SQLite caching for organization and repository data
- Environment variables for database configuration and cache duration
- Implemented a 5-minute cache refresh mechanism for repository and organization data
- Added timestamp tracking for cached data in SQLite database
- Fallback to cached data when GitHub API requests fail
- Implemented exponential backoff for API rate limit handling

### Changed
- Modified API endpoints to check cache age before making new requests
- Improved error handling and user feedback across the application
- Moved database and cache configuration to environment variables
- Updated UI to show more detailed organization information in select lists

### Fixed
- Resolved issues with multiple API requests for the same data
- Improved handling of GitHub API rate limits

## [0.4.0] - 2024-10-22

### Added
- New rename.html page for renaming organizations and repositories
- API endpoints for renaming organizations and repositories
- Scripts for handling organization and repository renaming
- Clickable links for organization and repository names in rename.html
- Error handling and display in rename.html
- Ability to view repositories for a selected organization in rename.html

### Changed
- Updated UI to show more repository details in blocks.html
- Improved error handling and user feedback across the application
- Enhanced the move repository functionality to prevent multiple simultaneous requests
- Refactored API server (server.js) to use proxy requests for all endpoints

### Fixed
- Issue with drag and drop functionality for moving repositories
- Error related to repository transfer API usage
- Various minor bug fixes and performance improvements

## [0.3.0] - 2024-10-21

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

## [0.2.0] - 2024-10-21

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





