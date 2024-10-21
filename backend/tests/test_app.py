import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_repository_files(client):
    with patch('app.list_repository_files') as mock_list_files:
        mock_list_files.return_value = [{'name': 'file1.txt', 'size': 100}]
        response = client.get('/api/repository-files?repo=test/repo')
        assert response.status_code == 200
        assert response.json == {'files': [{'name': 'file1.txt', 'size': 100}]}

def test_get_repository_files_missing_param(client):
    response = client.get('/api/repository-files')
    assert response.status_code == 400
    assert 'error' in response.json

def test_get_readme(client):
    with patch('app.get_readme_content') as mock_get_readme:
        mock_get_readme.return_value = '# Test README'
        response = client.get('/api/readme?repo=test/repo')
        assert response.status_code == 200
        assert response.json == {'content': '# Test README'}

def test_get_readme_missing_param(client):
    response = client.get('/api/readme')
    assert response.status_code == 400
    assert 'error' in response.json

# Add more tests for other endpoints...
