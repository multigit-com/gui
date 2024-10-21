const API_BASE_URL = window.API_BASE_URL || 'http://localhost:3001';

function fetchOrganizations() {
  fetch(`${API_BASE_URL}/api/organizations`)
    .then(response => {
      if (!response.ok) {
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
      showError('Failed to fetch organizations');
    });
}

function populateOrganizationSelects(organizations) {
  const selects = document.querySelectorAll('.org-select');
  selects.forEach(select => {
    select.innerHTML = '<option value="">Select an organization</option>';
    organizations.forEach(org => {
      const option = document.createElement('option');
      option.value = org.id;
      option.textContent = org.name;
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
    const repoBlock = createRepoBlock(repo);
    repoList.appendChild(repoBlock);
  });
  setupDragAndDrop();
}

function createRepoBlock(repo) {
  const repoBlock = document.createElement('div');
  repoBlock.className = 'repo-block';
  repoBlock.draggable = true;
  repoBlock.dataset.repoId = repo.id;
  repoBlock.dataset.repoName = repo.name;
  repoBlock.dataset.repoUrl = repo.html_url;
  
  const repoName = document.createElement('div');
  repoName.className = 'repo-name';
  repoName.textContent = repo.name;
  
  const repoUrl = document.createElement('div');
  repoUrl.className = 'repo-url';
  repoUrl.textContent = repo.html_url;

  const fileList = document.createElement('div');
  fileList.className = 'file-list';

  const readmePreview = document.createElement('div');
  readmePreview.className = 'readme-preview';

  repoBlock.appendChild(repoName);
  repoBlock.appendChild(repoUrl);
  repoBlock.appendChild(fileList);
  repoBlock.appendChild(readmePreview);

  repoBlock.addEventListener('mouseenter', () => {
    fetchRepoFiles(repo.name, fileList);
    fetchReadmePreview(repo.name, readmePreview);
  });

  repoBlock.addEventListener('mouseleave', () => {
    fileList.style.display = 'none';
    readmePreview.style.display = 'none';
  });

  repoBlock.addEventListener('click', () => {
    window.open(repo.html_url, '_blank');
  });

  return repoBlock;
}

function fetchRepoFiles(repoUrl, fileListElement) {
    const encodedRepoUrl = encodeURIComponent(repoUrl);
    fetch(`${API_BASE_URL}/api/repository-files?url=${encodedRepoUrl}`)
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
            fileListElement.innerHTML = '<h3>Files:</h3>';
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
            fileListElement.style.display = 'block';
        });
}

function fetchReadmePreview(repoUrl, readmeElement) {
    const encodedRepoUrl = encodeURIComponent(repoUrl);
    fetch(`${API_BASE_URL}/api/readme?url=${encodedRepoUrl}`)
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
                readmeElement.innerHTML = '<h3>README Preview:</h3>' + marked(data.content);
                readmeElement.style.display = 'block';
            } else {
                readmeElement.innerHTML = '<p>No README content available</p>';
                readmeElement.style.display = 'block';
            }
        })
        .catch(error => {
            console.error('Error fetching README:', error);
            readmeElement.innerHTML = `<p>Error fetching README: ${error.message}</p>`;
            readmeElement.style.display = 'block';
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

function moveRepository(repoData, repoBlock, targetOrgId, targetZone) {
  fetch(`${API_BASE_URL}/api/move-repository`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      repoId: repoData.repoId,
      sourceOrgId: repoData.sourceOrgId,
      targetOrgId: targetOrgId
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      targetZone.appendChild(repoBlock);
      console.log('Repository moved:', data);
    } else {
      console.error('Failed to move repository:', data.message);
      alert(`Failed to move repository: ${data.message}`);
    }
  })
  .catch(error => {
    console.error('Error moving repository:', error);
    alert('Error moving repository. Please try again.');
  });
}

function removeRepository(repoData, repoBlock) {
  const trashList = document.querySelector('#trash-column .repo-list');
  const removedRepo = document.createElement('div');
  removedRepo.className = 'removed-repo';
  removedRepo.textContent = `${repoData.repoName} (Removing...)`;
  trashList.appendChild(removedRepo);

  fetch(`${API_BASE_URL}/api/remove-repository`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ repoUrl: repoData.repoUrl })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      repoBlock.remove();
      removedRepo.textContent = `${repoData.repoName} (Removed: ${new Date().toLocaleString()})`;
      console.log('Repository removed:', data);
    } else {
      removedRepo.textContent = `${repoData.repoName} (Removal failed: ${data.message})`;
      console.error('Failed to remove repository:', data.message);
    }
  })
  .catch(error => {
    removedRepo.textContent = `${repoData.repoName} (Removal error)`;
    console.error('Error removing repository:', error);
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
