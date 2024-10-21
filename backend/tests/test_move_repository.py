import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.move_repository import move_repository
import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_requests():
    with patch('scripts.move_repository.requests') as mock_req:
        yield mock_req

@pytest.fixture
def mock_subprocess():
    with patch('scripts.move_repository.subprocess') as mock_sub:
        yield mock_sub

def test_move_repository_success(mock_requests, mock_subprocess):
    mock_requests.get.return_value.status_code = 200
    mock_requests.get.return_value.json.return_value = {'name': 'test-repo'}
    mock_requests.post.return_value.status_code = 202
    mock_requests.get.return_value.status_code = 200

    result = move_repository('123', 'source-org', 'target-org')
    assert result['success'] == True
    assert 'moved successfully' in result['message']
    mock_subprocess.run.assert_called_once()

def test_move_repository_failure_fetch(mock_requests):
    mock_requests.get.return_value.status_code = 404

    result = move_repository('123', 'source-org', 'target-org')
    assert result['success'] == False
    assert 'Failed to fetch repository details' in result['message']

def test_move_repository_failure_transfer(mock_requests):
    mock_requests.get.return_value.status_code = 200
    mock_requests.get.return_value.json.return_value = {'name': 'test-repo'}
    mock_requests.post.return_value.status_code = 403

    result = move_repository('123', 'source-org', 'target-org')
    assert result['success'] == False
    assert 'Failed to move repository' in result['message']

def test_move_repository_transfer_timeout(mock_requests):
    mock_requests.get.return_value.status_code = 200
    mock_requests.get.return_value.json.return_value = {'name': 'test-repo'}
    mock_requests.post.return_value.status_code = 202
    mock_requests.get.side_effect = [
        MagicMock(status_code=404),
        MagicMock(status_code=404),
        MagicMock(status_code=404),
    ]

    result = move_repository('123', 'source-org', 'target-org')
    assert result['success'] == False
    assert 'Repository transfer initiated but not completed in time' in result['message']
