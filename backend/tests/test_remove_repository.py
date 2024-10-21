import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.remove_repository_from_github_by_url_repo import remove_repository_from_github_by_url_repo
import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_requests():
    with patch('scripts.remove_repository_from_github_by_url_repo.requests') as mock_req:
        yield mock_req

@pytest.fixture
def mock_subprocess():
    with patch('scripts.remove_repository_from_github_by_url_repo.subprocess') as mock_sub:
        yield mock_sub

def test_remove_repository_success(mock_requests, mock_subprocess):
    mock_requests.delete.return_value.status_code = 204

    result = remove_repository_from_github_by_url_repo('https://github.com/owner/repo', 'source-org')
    assert result['success'] == True
    assert 'has been deleted' in result['message']
    mock_subprocess.run.assert_called_once()

def test_remove_repository_failure(mock_requests):
    mock_requests.delete.return_value.status_code = 403

    result = remove_repository_from_github_by_url_repo('https://github.com/owner/repo', 'source-org')
    assert result['success'] == False
    assert 'Failed to delete repository' in result['message']
