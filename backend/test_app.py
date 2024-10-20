import unittest
import json
from unittest.mock import patch, MagicMock
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('subprocess.run')
    def test_create_repository(self, mock_run):
        # Mock the subprocess.run to return a successful result
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = json.dumps({
            "name": "test-repo",
            "owner": {"login": "test-owner"},
            "html_url": "https://github.com/test-owner/test-repo"
        })

        response = self.app.post('/api/execute', json={
            'command': 'create_repository_on_github',
            'input': 'test-owner test-repo'
        })

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('test-repo', data['output'])
        self.assertIn('test-owner', data['output'])

    @patch('subprocess.run')
    def test_remove_repository(self, mock_run):
        # Mock the subprocess.run to return a successful result
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = json.dumps({
            "success": True,
            "message": "Repository test-owner/test-repo has been deleted."
        })

        response = self.app.post('/api/execute', json={
            'command': 'remove_repository_from_github_by_url_repo',
            'input': 'https://github.com/test-owner/test-repo'
        })

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('test-owner/test-repo', data['output'])

    @patch('subprocess.run')
    def test_unknown_command(self, mock_run):
        response = self.app.post('/api/execute', json={
            'command': 'unknown_command',
            'input': 'test input'
        })

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Unknown command')

    @patch('subprocess.run')
    def test_command_execution_failure(self, mock_run):
        # Mock the subprocess.run to return a failed result
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "Error: Something went wrong"

        response = self.app.post('/api/execute', json={
            'command': 'create_repository_on_github',
            'input': 'test-owner test-repo'
        })

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], "Error: Something went wrong")

    @patch('subprocess.run')
    def test_get_audit_log(self, mock_run):
        # Mock the subprocess.run to return a sample audit log
        mock_run.return_value.stdout = json.dumps([
            {"timestamp": "2023-05-20T10:00:00", "action": "create_repository", "details": "test-owner/test-repo"},
            {"timestamp": "2023-05-20T11:00:00", "action": "remove_repository", "details": "test-owner/old-repo"}
        ])

        response = self.app.get('/api/audit-log')

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['action'], "create_repository")
        self.assertEqual(data[1]['action'], "remove_repository")

if __name__ == '__main__':
    unittest.main()
