const request = require('supertest');
const express = require('express');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

jest.mock('fs');
jest.mock('child_process');

const app = require('./server');

describe('API Endpoints', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('GET /api/scripts', () => {
    it('should return a list of scripts', async () => {
      fs.readdir.mockImplementation((dir, callback) => {
        callback(null, ['script1.py', 'script2.py', 'not_a_script.txt']);
      });

      const response = await request(app).get('/api/scripts');
      expect(response.status).toBe(200);
      expect(response.body).toEqual(['script1', 'script2']);
    });

    it('should handle errors when reading scripts directory', async () => {
      fs.readdir.mockImplementation((dir, callback) => {
        callback(new Error('Failed to read directory'), null);
      });

      const response = await request(app).get('/api/scripts');
      expect(response.status).toBe(500);
      expect(response.body).toEqual({ error: 'Failed to read scripts directory' });
    });
  });

  describe('GET /api/repositories', () => {
    it('should return a list of repositories for a given organization', async () => {
      exec.mockImplementation((command, callback) => {
        callback(null, JSON.stringify([{ id: 1, name: 'repo1' }, { id: 2, name: 'repo2' }]), null);
      });

      const response = await request(app).get('/api/repositories?org=testorg');
      expect(response.status).toBe(200);
      expect(response.body).toEqual([{ id: 1, name: 'repo1' }, { id: 2, name: 'repo2' }]);
    });

    it('should handle missing organization parameter', async () => {
      const response = await request(app).get('/api/repositories');
      expect(response.status).toBe(400);
      expect(response.body).toEqual({ error: 'Organization parameter is required' });
    });

    it('should handle script execution errors', async () => {
      exec.mockImplementation((command, callback) => {
        callback(new Error('Script execution failed'), null, 'Error output');
      });

      const response = await request(app).get('/api/repositories?org=testorg');
      expect(response.status).toBe(500);
      expect(response.body).toEqual({ error: 'Failed to list repositories' });
    });
  });

  describe('POST /api/move-repository', () => {
    it('should move a repository successfully', async () => {
      exec.mockImplementation((command, callback) => {
        callback(null, JSON.stringify({ success: true, message: 'Repository moved successfully' }), null);
      });

      const response = await request(app)
        .post('/api/move-repository')
        .send({ repoId: '123', sourceOrgId: 'org1', targetOrgId: 'org2' });
      expect(response.status).toBe(200);
      expect(response.body).toEqual({ success: true, message: 'Repository moved successfully' });
    });

    it('should handle missing parameters', async () => {
      const response = await request(app)
        .post('/api/move-repository')
        .send({ repoId: '123', sourceOrgId: 'org1' });
      expect(response.status).toBe(400);
      expect(response.body).toEqual({ error: 'Missing required parameters' });
    });

    it('should handle script execution errors', async () => {
      exec.mockImplementation((command, callback) => {
        callback(new Error('Script execution failed'), null, 'Error output');
      });

      const response = await request(app)
        .post('/api/move-repository')
        .send({ repoId: '123', sourceOrgId: 'org1', targetOrgId: 'org2' });
      expect(response.status).toBe(500);
      expect(response.body).toEqual({ error: 'Failed to move repository' });
    });
  });
});
