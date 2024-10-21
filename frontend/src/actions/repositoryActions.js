// Fetch repository files
export const fetchRepositoryFiles = (org, repo) => async (dispatch) => {
  try {
    dispatch({ type: 'FETCH_REPOSITORY_FILES_START' });
    const response = await fetch(`/api/repository-files?org=${org}&repo=${repo}`);
    const data = await response.json();
    console.log('API response:', data);
    if (response.ok) {
      dispatch({ type: 'FETCH_REPOSITORY_FILES_SUCCESS', payload: data.files });
    } else {
      throw new Error(data.error || 'Failed to fetch repository files');
    }
  } catch (error) {
    console.error('Error fetching repository files:', error);
    dispatch({ type: 'FETCH_REPOSITORY_FILES_FAILURE', payload: error.message });
  }
};

// Fetch README content
export const fetchReadme = (org, repo) => async (dispatch) => {
  try {
    const response = await fetch(`/api/readme?org=${org}&repo=${repo}`);
    const data = await response.json();
    dispatch({ type: 'SET_README', payload: data.content });
  } catch (error) {
    console.error('Error fetching README:', error);
  }
};

// Set current repository
export const setCurrentRepository = (org, repo) => async (dispatch) => {
  try {
    const response = await fetch('/api/repo', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ org, repo }),
    });
    if (response.ok) {
      dispatch({ type: 'SET_CURRENT_REPOSITORY', payload: { org, repo } });
    }
  } catch (error) {
    console.error('Error setting current repository:', error);
  }
};
