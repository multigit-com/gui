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
