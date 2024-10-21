document.addEventListener('DOMContentLoaded', () => {
    const columns = document.querySelectorAll('.column');
    const orgSelects = document.querySelectorAll('select');

    // Fetch organizations and populate select lists
    fetch('/api/organizations')
        .then(response => response.json())
        .then(organizations => {
            orgSelects.forEach(select => {
                organizations.forEach(org => {
                    const option = document.createElement('option');
                    option.value = org.id;
                    option.textContent = org.name;
                    select.appendChild(option);
                });
            });
        });

    // Load repositories when an organization is selected
    orgSelects.forEach(select => {
        select.addEventListener('change', (event) => {
            const orgId = event.target.value;
            const column = event.target.closest('.column');
            loadRepositories(orgId, column);
        });
    });

    function loadRepositories(orgId, column) {
        fetch(`/api/repositories?org=${orgId}`)
            .then(response => response.json())
            .then(repositories => {
                const repoList = column.querySelector('.repo-list');
                repoList.innerHTML = '';
                repositories.forEach(repo => {
                    const repoBlock = document.createElement('div');
                    repoBlock.className = 'repo-block';
                    repoBlock.textContent = repo.name;
                    repoBlock.draggable = true;
                    repoBlock.dataset.repoId = repo.id;
                    repoList.appendChild(repoBlock);
                });
            });
    }

    // Implement drag and drop
    columns.forEach(column => {
        column.addEventListener('dragover', (e) => {
            e.preventDefault();
        });

        column.addEventListener('drop', (e) => {
            e.preventDefault();
            const repoId = e.dataTransfer.getData('text/plain');
            const sourceColumn = document.querySelector(`[data-repo-id="${repoId}"]`).closest('.column');
            const targetColumn = e.target.closest('.column');

            if (sourceColumn !== targetColumn) {
                moveRepository(repoId, sourceColumn.querySelector('select').value, targetColumn.querySelector('select').value);
            }
        });
    });

    document.addEventListener('dragstart', (e) => {
        if (e.target.classList.contains('repo-block')) {
            e.dataTransfer.setData('text/plain', e.target.dataset.repoId);
        }
    });

    function moveRepository(repoId, sourceOrgId, targetOrgId) {
        fetch('/api/move-repository', {
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
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                // Refresh repository lists
                loadRepositories(sourceOrgId, document.querySelector(`select[value="${sourceOrgId}"]`).closest('.column'));
                loadRepositories(targetOrgId, document.querySelector(`select[value="${targetOrgId}"]`).closest('.column'));
            } else {
                alert('Failed to move repository: ' + result.message);
            }
        });
    }
});
