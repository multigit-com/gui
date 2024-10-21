const API_BASE_URL = 'http://localhost:3001';

function fetchOrganizations() {
    fetch(`${API_BASE_URL}/api/organizations`)
        .then(response => response.json())
        .then(data => {
            console.log('Fetched organizations:', data);
            const orgList = document.getElementById('org-list');
            orgList.innerHTML = '';
            if (Array.isArray(data.organizations)) {
                data.organizations.forEach(org => {
                    const orgItem = createOrgItem(org);
                    orgList.appendChild(orgItem);
                });
            } else {
                console.error('Unexpected data structure for organizations:', data);
                showError('Failed to load organizations. Unexpected data structure.');
            }
        })
        .catch(error => {
            console.error('Error fetching organizations:', error);
            showError('Failed to fetch organizations');
        });
}

function createOrgItem(org) {
    const orgItem = document.createElement('div');
    orgItem.className = 'org-item';

    const orgLink = document.createElement('a');
    orgLink.href = `https://github.com/${org.login}`;
    orgLink.textContent = org.login || 'Unknown';
    orgLink.target = '_blank';
    orgLink.rel = 'noopener noreferrer';
    orgItem.appendChild(orgLink);

    const input = document.createElement('input');
    input.value = org.login || 'Unknown';
    input.dataset.originalName = org.login || 'Unknown';
    input.dataset.orgId = org.id || '';

    const renameButton = document.createElement('button');
    renameButton.textContent = 'Rename';
    renameButton.onclick = () => renameOrganization(input.dataset.orgId, input.value);

    const showReposButton = document.createElement('button');
    showReposButton.textContent = 'Show Repos';
    showReposButton.onclick = () => fetchRepositories(input.dataset.originalName);

    orgItem.appendChild(document.createElement('br'));
    orgItem.appendChild(input);
    orgItem.appendChild(renameButton);
    orgItem.appendChild(showReposButton);

    return orgItem;
}

function renameOrganization(orgId, newName) {
    if (!orgId) {
        console.error('Organization ID is missing');
        showError('Cannot rename organization: ID is missing');
        return;
    }
    fetch(`${API_BASE_URL}/api/rename-organization`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ orgId, newName })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Organization renamed successfully');
            fetchOrganizations();
        } else {
            console.error('Failed to rename organization:', data.error);
            showError(`Failed to rename organization: ${data.error}`);
        }
    })
    .catch(error => {
        console.error('Error renaming organization:', error);
        showError('Error renaming organization. Please try again.');
    });
}

function fetchRepositories(orgName) {
    fetch(`${API_BASE_URL}/api/repositories?org=${orgName}`)
        .then(response => response.json())
        .then(data => {
            console.log('Fetched repositories:', data);
            const repoList = document.getElementById('repo-list');
            repoList.innerHTML = '';
            if (Array.isArray(data)) {
                data.forEach(repo => {
                    const repoItem = createRepoItem(repo, orgName);
                    repoList.appendChild(repoItem);
                });
            } else {
                console.error('Unexpected data structure for repositories:', data);
                showError('Failed to load repositories. Unexpected data structure.');
            }
        })
        .catch(error => {
            console.error('Error fetching repositories:', error);
            showError('Failed to fetch repositories');
        });
}

function createRepoItem(repo, orgName) {
    const repoItem = document.createElement('div');
    repoItem.className = 'repo-item';

    const repoLink = document.createElement('a');
    repoLink.href = repo.html_url || `https://github.com/${orgName}/${repo.name}`;
    repoLink.textContent = repo.name || 'Unknown';
    repoLink.target = '_blank';
    repoLink.rel = 'noopener noreferrer';
    repoItem.appendChild(repoLink);

    const input = document.createElement('input');
    input.value = repo.name || 'Unknown';
    input.dataset.originalName = repo.name || 'Unknown';

    const renameButton = document.createElement('button');
    renameButton.textContent = 'Rename';
    renameButton.onclick = () => renameRepository(orgName, input.dataset.originalName, input.value);

    repoItem.appendChild(document.createElement('br'));
    repoItem.appendChild(input);
    repoItem.appendChild(renameButton);

    return repoItem;
}

function renameRepository(orgName, oldName, newName) {
    fetch(`${API_BASE_URL}/api/rename-repository`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ orgName, oldName, newName })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Repository renamed successfully');
            fetchRepositories(orgName);
        } else {
            console.error('Failed to rename repository:', data.error);
            showError(`Failed to rename repository: ${data.error}`);
        }
    })
    .catch(error => {
        console.error('Error renaming repository:', error);
        showError('Error renaming repository. Please try again.');
    });
}

function showError(message) {
    const errorElement = document.createElement('div');
    errorElement.className = 'error-message';
    errorElement.textContent = message;
    document.body.insertBefore(errorElement, document.body.firstChild);
    setTimeout(() => errorElement.remove(), 5000);
}

// Initialize the page
document.addEventListener('DOMContentLoaded', fetchOrganizations);
