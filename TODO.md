create service with docker and docker compose with frontend and backend for run python scripts on backend api  
from frontend based on selectlist where is list of commands and input. 
First example at backend is a function remove_repository_from_gurhub_by_url_repo 
at frontend is input I should put:@https://github.com/apicup/namecheap the result shoopuld be removed repository on github, token and other VARIABLES should be in .env file 

Value from remove_repository_from_github_by_url_repo at selectlist should be loaded from nodejs api,
The api function should list all scripts from scripts folder
Create that script remove_repository_from_github_by_url_repo.py there
get token from .env
and run on frontend with post data input urlfrom input
create another function to create repository in the same way


Enhance the GitHub Repository Manager with a new visual interface for repository management across organizations:

1. Create a new file `blocks.html` in the `frontend/public` directory:
    - Implement a columnar layout with draggable repository blocks.
    - Each column represents a different organization.
    - Add a select list at the top of each column to choose an organization.

2. Update the backend API:
    - Create a new endpoint `/api/organizations` to list all available organizations.
    - Modify the existing `/api/scripts` endpoint to include repository listing functionality.
    - Implement filtering capabilities for organizations and repositories.

3. Enhance the frontend JavaScript:
    - Fetch and populate the organization select lists.
    - Load repositories for selected organizations.
    - Implement drag-and-drop functionality for moving repositories between columns.
    - Use the existing `move_repository` function when a repository is dropped in a new column.

4. Styling and UX:
    - Style the columns, repository blocks, and select lists for a clean, modern look.
    - Implement smooth animations for dragging and dropping.
    - Add loading indicators and error handling.

5. Integration:
    - Ensure the new interface works seamlessly with the existing backend.
    - Update the audit logging to record repository moves initiated from this new interface.

6. Testing:
    - Add unit tests for new backend functionality.
    - Implement integration tests for the drag-and-drop feature.



Create list of files with size of files and show screenshot on hover mouse event for each repo block in columns
render markdown README.md from repository in popup on hover too


handle moving draggable event to another organisation such backend/scripts/move_repository.py
