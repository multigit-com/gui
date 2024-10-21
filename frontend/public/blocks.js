document.addEventListener('DOMContentLoaded', () => {
    const columns = document.querySelectorAll('.column');
    const orgSelects = document.querySelectorAll('select');
    const errorContainer = document.createElement('div');
    errorContainer.id = 'error-container';
    errorContainer.style.color = 'red';
    errorContainer.style.marginBottom = '10px';
    document.body.insertBefore(errorContainer, document.body.firstChild);

    function showError(message) {
        errorContainer.textContent = message;
        errorContainer.style.display = 'block';
    }

    function clearError() {
        errorContainer.textContent = '';
        errorContainer.style.display = 'none';
    }

    function fetchAllOrganizations() {
        clearError();
        fetch('http://localhost:3001/api/organizations')
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
                const { organizations } = data;
                if (organizations.length === 0) {
                    showError('No organizations found for your account. Please check your GitHub token and permissions.');
                }

                orgSelects.forEach(select => {
                    select.innerHTML = '<option value="">Select an organization</option>';
                    organizations.forEach(org => {
                        const option = document.createElement('option');
                        option.value = org.id;
                        option.textContent = org.name;
                        select.appendChild(option);
                    });
                });
            })
            .catch(error => {
                console.error('Error fetching organizations:', error);
                showError(`Failed to load organizations: ${error.message}`);
            });
    }

    fetchAllOrganizations();

    orgSelects.forEach(select => {
        select.addEventListener('change', (event) => {
            const selectedValue = event.target.value;
            if (selectedValue) {
                const column = event.target.closest('.column');
                loadRepositories(selectedValue, column);
            }
        });
    });

    function loadRepositories(orgId, column) {
        clearError();
        fetch(`http://localhost:3001/api/repositories?org=${orgId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(repositories => {
                if (repositories.error) {
                    throw new Error(repositories.error);
                }
                const repoList = column.querySelector('.repo-list');
                repoList.innerHTML = '';
                repositories.forEach(repo => {
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
                    
                    repoBlock.appendChild(repoName);
                    repoBlock.appendChild(repoUrl);
                    repoList.appendChild(repoBlock);
                });
                setupDragAndDrop();
            })
            .catch(error => {
                console.error('Error fetching repositories:', error);
                showError(`Failed to load repositories: ${error.message}`);
            });
    }

    function setupDragAndDrop() {
        const draggables = document.querySelectorAll('.repo-block');
        const dropZones = document.querySelectorAll('.repo-list');

        draggables.forEach(draggable => {
            draggable.addEventListener('dragstart', () => {
                draggable.classList.add('dragging');
            });

            draggable.addEventListener('dragend', () => {
                draggable.classList.remove('dragging');
            });
        });

        dropZones.forEach(zone => {
            zone.addEventListener('dragover', e => {
                e.preventDefault();
                const afterElement = getDragAfterElement(zone, e.clientY);
                const draggable = document.querySelector('.dragging');
                if (afterElement == null) {
                    zone.appendChild(draggable);
                } else {
                    zone.insertBefore(draggable, afterElement);
                }
            });

            zone.addEventListener('drop', e => {
                e.preventDefault();
                const draggable = document.querySelector('.dragging');
                const sourceColumn = draggable.closest('.column');
                const targetColumn = zone.closest('.column');
                
                if (sourceColumn !== targetColumn) {
                    const repoId = draggable.dataset.repoId;
                    const sourceOrgId = sourceColumn.querySelector('select').value;
                    const targetOrgId = targetColumn.querySelector('select').value;
                    moveRepository(repoId, sourceOrgId, targetOrgId);
                }
            });
        });
    }

    function getDragAfterElement(container, y) {
        const draggableElements = [...container.querySelectorAll('.repo-block:not(.dragging)')];

        return draggableElements.reduce((closest, child) => {
            const box = child.getBoundingClientRect();
            const offset = y - box.top - box.height / 2;
            if (offset < 0 && offset > closest.offset) {
                return { offset: offset, element: child };
            } else {
                return closest;
            }
        }, { offset: Number.NEGATIVE_INFINITY }).element;
    }

    function moveRepository(repoId, sourceOrgId, targetOrgId) {
        clearError();
        fetch('http://localhost:3001/api/move-repository', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                repoId: repoId,
                sourceOrgId: sourceOrgId,
                targetOrgId: targetOrgId
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(result => {
            if (result.success) {
                console.log('Repository moved successfully');
                // Refresh the repository lists for both source and target organizations
                loadRepositories(sourceOrgId, document.querySelector(`select[value="${sourceOrgId}"]`).closest('.column'));
                loadRepositories(targetOrgId, document.querySelector(`select[value="${targetOrgId}"]`).closest('.column'));
            } else {
                throw new Error(result.message || 'Failed to move repository');
            }
        })
        .catch(error => {
            console.error('Error moving repository:', error);
            showError(`Failed to move repository: ${error.message}`);
        });
    }
});
