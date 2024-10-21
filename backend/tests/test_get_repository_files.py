import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.get_repository_files import get_repository_files
import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_requests():
    with patch('scripts.get_repository_files.requests') as mock_req:
        yield mock_req

@pytest.fixture
def mock_image():
    with patch('scripts.get_repository_files.Image') as mock_img:
        yield mock_img

@pytest.fixture
def mock_markdown():
    with patch('scripts.get_repository_files.markdown') as mock_md:
        yield mock_md

def test_get_repository_files_success(mock_requests, mock_image, mock_markdown):
    mock_requests.get.return_value.status_code = 200
    mock_requests.get.return_value.json.return_value = [
        {'type': 'file', 'name': 'test.txt', 'size': 100, 'download_url': 'http://example.com/test.txt'},
        {'type': 'file', 'name': 'image.png', 'size': 1000, 'download_url': 'http://example.com/image.png'},
        {'type': 'file', 'name': 'README.md', 'size': 500, 'download_url': 'http://example.com/README.md'}
    ]
    mock_requests.get.return_value.text = '# Test README'
    mock_markdown.markdown.return_value = '<h1>Test README</h1>'

    mock_image.open.return_value.save.return_value = None

    result = get_repository_files('https://github.com/test/repo')

    assert 'files' in result
    assert len(result['files']) == 3
    assert result['files'][0]['name'] == 'test.txt'
    assert result['files'][1]['name'] == 'image.png'
    assert 'screenshot' in result['files'][1]
    assert result['files'][2]['name'] == 'README.md'
    assert result['readme'] == '<h1>Test README</h1>'

def test_get_repository_files_failure(mock_requests):
    mock_requests.get.return_value.status_code = 404

    result = get_repository_files('https://github.com/test/repo')

    assert 'error' in result
    assert 'Failed to fetch repository contents' in result['error']

def test_get_repository_files_no_readme(mock_requests, mock_image):
    mock_requests.get.return_value.status_code = 200
    mock_requests.get.return_value.json.return_value = [
        {'type': 'file', 'name': 'test.txt', 'size': 100, 'download_url': 'http://example.com/test.txt'}
    ]

    result = get_repository_files('https://github.com/test/repo')

    assert 'files' in result
    assert len(result['files']) == 1
    assert result['files'][0]['name'] == 'test.txt'
    assert 'readme' not in result
