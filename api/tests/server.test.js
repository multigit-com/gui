const request = require('supertest');
const express = require('express');
const { exec } = require('child_process');
const app = require('../server');

jest.mock('child_process');

describe('API Server', () => {
  test('GET /api/repository-files', async () => {
    exec.mockImplementation((cmd, callback) => {
      callback(null, JSON.stringify({ files: [{ name: 'file1.txt', size: 100 }] }), null);
    });

    const response = await request(app).get('/api/repository-files?repo=test/repo');
    expect(response.status).toBe(200);
    expect(response.body).toEqual({ files: [{ name: 'file1.txt', size: 100 }] });
  });

  test('GET /api/readme', async () => {
    exec.mockImplementation((cmd, callback) => {
      callback(null, JSON.stringify({ content: '# Test README' }), null);
    });

    const response = await request(app).get('/api/readme?repo=test/repo');
    expect(response.status).toBe(200);
    expect(response.body).toEqual({ content: '# Test README' });
  });

  test('POST /api/move-repository', async () => {
    exec.mockImplementation((cmd, callback) => {
      callback(null, JSON.stringify({ success: true, message: 'Repository moved successfully' }), null);
    });

    const response = await request(app)
      .post('/api/move-repository')
      .send({ repoId: '123', sourceOrgId: 'org1', targetOrgId: 'org2' });
    expect(response.status).toBe(200);
    expect(response.body).toEqual({ success: true, message: 'Repository moved successfully' });
  });

  // Add more tests for other endpoints...
});
