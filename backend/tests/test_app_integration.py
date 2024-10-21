import unittest
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

BASE_URL = 'http://localhost:5000'  # Adjust if your app runs on a different port
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
TEST_REPO_URL = 'https://github.com/octocat/Hello-World'  # Use a public repo for testing

class TestAppIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Wait for the app to start
        max_retries = 5
        for _ in range(max_retries):
            try:
                requests.get(BASE_URL)
                break
            except requests.ConnectionError:
                time.sleep(1)
        else:
            raise Exception("Failed to connect to the application")

    def test_get_repository_files(self):
        response = requests.get(f'{BASE_URL}/api/repository-files?repoUrl={TEST_REPO_URL}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('files', data)
        self.assertIsInstance(data['files'], list)
        if 'readme' in data:
            self.assertIsInstance(data['readme'], str)

    def test_list_organizations(self):
        response = requests.get(f'{BASE_URL}/api/organizations')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('organizations', data)
        self.assertIsInstance(data['organizations'], list)

    def test_move_repository(self):
        # This test is a mock as we can't actually move repositories in a test environment
        response = requests.post(f'{BASE_URL}/api/move-repository', json={
            'repoId': '12345',
            'sourceOrgId': 'sourceOrg',
            'targetOrgId': 'targetOrg'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('success', data)

    def test_remove_repository(self):
        # This test is a mock as we can't actually remove repositories in a test environment
        response = requests.post(f'{BASE_URL}/api/remove-repository', json={
            'repoUrl': TEST_REPO_URL,
            'sourceOrgId': 'sourceOrg'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('success', data)

if __name__ == '__main__':
    unittest.main()
