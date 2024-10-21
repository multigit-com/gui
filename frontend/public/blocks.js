const API_BASE_URL = window.API_BASE_URL || 'http://localhost:3001';

function fetchOrganizations() {
  fetch(`${API_BASE_URL}/api/organizations`)
    .then(response => {
      if (!response.ok) {
        if (response.status === 429) {
          throw new Error('Rate limit exceeded. Please try again later.');
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      console.log('Organizations fetched successfully:', data);
      populateOrganizationSelects(data.organizations);
    })
    .catch(error => {
      console.error('Error fetching organizations:', error);
      showError(error.message || 'Failed to fetch organizations');
    });
}

function populateOrganizationSelects(organizations) {
  const selects = document.querySelectorAll('.org-select');
  selects.forEach(select => {
    select.innerHTML = '<option value="">Select an organization</option>';
    organizations.forEach(org => {
      const option = document.createElement('option');
      option.value = org.id;
      option.textContent = `${org.name} (Repos: ${org.public_repos}, Forks: ${org.forks_count})`;
      select.appendChild(option);
    });

    select.addEventListener('change', (event) => {
      const selectedOrg = event.target.value;
      if (selectedOrg) {
        const column = event.target.closest('.column');
        fetchRepositories(selectedOrg, column);
      }
    });
  });
}

function fetchRepositories(org, column) {
  fetch(`${API_BASE_URL}/api/repositories?org=${org}`)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      console.log('Repositories fetched successfully:', data);
      displayRepositories(data, column);
    })
    .catch(error => {
      console.error('Error fetching repositories:', error);
      showError('Failed to fetch repositories');
    });
}

function displayRepositories(repositories, column) {
  const repoList = column.querySelector('.repo-list');
  repoList.innerHTML = '';
  repositories.forEach(repo => {
    repo.name = getRepoNameFromUrl(repo.html_url);
    repo.org = getOrgNameFromUrl(repo.html_url);
    const repoBlock = createRepoBlock(repo);
    repoList.appendChild(repoBlock);
    fetchRepoDetails(repo.org, repo.name, repoBlock);
  });
  setupDragAndDrop();
}

function createRepoBlock(repo) {
  const repoBlock = document.createElement('div');
  repoBlock.className = 'repo-block';
  repoBlock.draggable = true;
  repoBlock.dataset.repoId = repo.id;
  repoBlock.dataset.repoName = repo.name;
  repoBlock.dataset.orgName = repo.org;
  repoBlock.dataset.repoUrl = repo.html_url;

  const repoHeader = document.createElement('div');
  repoHeader.className = 'repo-header';

  const repoName = document.createElement('a');  // Changed to anchor tag
  repoName.className = 'repo-name';
  repoName.textContent = repo.name;
  repoName.href = repo.html_url;  // Set the href to the repo URL
  repoName.target = '_blank';  // Open in new tab
  repoName.rel = 'noopener noreferrer';  // Security best practice for links opening in new tabs

  const removeButton = document.createElement('button');
  removeButton.className = 'remove-repo-btn';
  removeButton.textContent = '[-]';
  removeButton.addEventListener('click', (e) => {
    e.stopPropagation(); // Prevent triggering the repo block click event
    removeRepository(repo);
  });

  repoHeader.appendChild(repoName);
  repoHeader.appendChild(removeButton);

  const repoUrl = document.createElement('div');
  repoUrl.className = 'repo-url';
  repoUrl.textContent = repo.html_url;

  const fileList = document.createElement('div');
  fileList.className = 'file-list';

  const readmePreview = document.createElement('div');
  readmePreview.className = 'readme-preview';

  repoBlock.appendChild(repoHeader);
  repoBlock.appendChild(repoUrl);
  repoBlock.appendChild(fileList);
  repoBlock.appendChild(readmePreview);

  repoBlock.addEventListener('click', (e) => {
    // Only toggle expansion if the click is not on the repo name link
    if (!e.target.classList.contains('repo-name')) {
      repoBlock.classList.toggle('expanded');
    }
  });

  return repoBlock;
}

function fetchRepoDetails(orgName, repoName, repoBlock) {
  fetchRepoFiles(orgName, repoName, repoBlock.querySelector('.file-list'));
  fetchReadmePreview(orgName, repoName, repoBlock.querySelector('.readme-preview'));
}

function fetchRepoFiles(orgName, repoName, fileListElement) {
  fetch(`${API_BASE_URL}/api/repository-files?org=${orgName}&repo=${repoName}`)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      if (data.error) {
        throw new Error(data.error);
      }
      if (!data.files) {
        throw new Error('No files data received');
      }
      // fileListElement.innerHTML = '<h3>Files:</h3>';
      fileListElement.innerHTML = '';
      const ul = document.createElement('ul');
      data.files.forEach(file => {
        const li = document.createElement('li');
        li.textContent = `${file.name} (${formatFileSize(file.size)})`;
        ul.appendChild(li);
      });
      fileListElement.appendChild(ul);
      fileListElement.style.display = 'block';
    })
    .catch(error => {
      console.error('Error fetching repository files:', error);
      fileListElement.innerHTML = `<p>Error fetching files: ${error.message}</p>`;
    });
}

function fetchReadmePreview(org, repoName, readmeElement) {
  fetch(`${API_BASE_URL}/api/readme?org=${org}&repo=${repoName}`)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      if (data.error) {
        throw new Error(data.error);
      }
      if (data.content) {
        const readmeContent = marked(data.content);
        readmeElement.innerHTML =
            // '<h3>README Preview:</h3>' +
          `<div class="readme-content">${readmeContent}</div>`;
      } else {
        readmeElement.innerHTML = '<p>No README content available</p>';
      }
      readmeElement.style.display = 'block';
    })
    .catch(error => {
      console.error('Error fetching README:', error);
      readmeElement.innerHTML = `<p>Error fetching README: ${error.message}</p>`;
    });
}

function formatFileSize(bytes) {
  if (bytes < 1024) return bytes + ' B';
  else if (bytes < 1048576) return (bytes / 1024).toFixed(2) + ' KB';
  else if (bytes < 1073741824) return (bytes / 1048576).toFixed(2) + ' MB';
  else return (bytes / 1073741824).toFixed(2) + ' GB';
}

function setupDragAndDrop() {
  const draggables = document.querySelectorAll('.repo-block');
  const dropZones = document.querySelectorAll('.repo-list');
  const trashZone = document.querySelector('#trash-column .repo-list');

  draggables.forEach(draggable => {
    draggable.addEventListener('dragstart', (e) => {
      e.dataTransfer.setData('text/plain', JSON.stringify({
        repoId: draggable.dataset.repoId,
        repoName: draggable.dataset.repoName,
        repoUrl: draggable.dataset.repoUrl,
        sourceOrgId: draggable.closest('.column').querySelector('.org-select').value
      }));
      draggable.classList.add('dragging');
    });

    draggable.addEventListener('dragend', () => {
      draggable.classList.remove('dragging');
    });
  });

  dropZones.forEach(zone => {
    zone.addEventListener('dragover', e => {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'move';
    });

    zone.addEventListener('drop', e => {
      e.preventDefault();
      const data = JSON.parse(e.dataTransfer.getData('text/plain'));
      const draggable = document.querySelector(`.repo-block[data-repo-id="${data.repoId}"]`);
      const sourceColumn = draggable.closest('.column');
      const targetColumn = zone.closest('.column');

      if (sourceColumn !== targetColumn) {
        if (targetColumn.id === 'trash-column') {
          removeRepository(data, draggable);
        } else {
          const targetOrgId = targetColumn.querySelector('.org-select').value;
          moveRepository(data, draggable, targetOrgId, zone);
        }
      }
    });
  });
}

function moveRepository(data, draggable, targetOrgId, zone) {
    if (draggable.dataset.isMoving === 'true') {
        console.log('Repository is already being moved');
        return;
    }
    
    draggable.dataset.isMoving = 'true';
    const sourceOrgId = data.sourceOrgId;
    const repoId = data.repoId;
    const repoName = data.repoName;

    fetch(`${API_BASE_URL}/api/move-repository`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            repoId: repoId,
            repoName: repoName,
            sourceOrgId: sourceOrgId,
            targetOrgId: targetOrgId
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            console.log('Repository moved:', result);
            zone.appendChild(draggable);
            draggable.dataset.orgId = targetOrgId;
        } else {
            console.error('Failed to move repository:', result.error);
            alert(`Failed to move repository: ${result.error}`);
        }
    })
    .catch(error => {
        console.error('Error moving repository:', error);
        alert('Error moving repository. Please try again.');
    })
    .finally(() => {
        draggable.dataset.isMoving = 'false';
    });
}

function removeRepository(repo) {
  fetch(`${API_BASE_URL}/api/remove-repository`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ repoUrl: repo.html_url, sourceOrgId: repo.org })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      const repoBlock = document.querySelector(`.repo-block[data-repo-id="${repo.id}"]`);
      repoBlock.remove();
      console.log('Repository removed:', data);
    } else {
      console.error('Failed to remove repository:', data.message);
      alert(`Failed to remove repository: ${data.message}`);
    }
  })
  .catch(error => {
    console.error('Error removing repository:', error);
    alert('Error removing repository. Please try again.');
  });
}

function showError(message) {
  const errorElement = document.getElementById('error-message');
  errorElement.textContent = message;
  errorElement.style.display = 'block';
}

function runCurlTests() {
    fetch(`${API_BASE_URL}/run-curl-tests`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        console.log('Curl tests results:', data);
        alert('Curl tests completed. Check the console for results.');
    })
    .catch(error => {
        console.error('Error running curl tests:', error);
        alert('Error running curl tests. Check the console for details.');
    });
}

function runAnsibleTests() {
    fetch(`${API_BASE_URL}/run-ansible-tests`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        console.log('Ansible tests results:', data);
        alert('Ansible tests completed. Check the console for results.');
    })
    .catch(error => {
        console.error('Error running Ansible tests:', error);
        alert('Error running Ansible tests. Check the console for details.');
    });
}

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
  fetchOrganizations();
  setupDragAndDrop();
});
