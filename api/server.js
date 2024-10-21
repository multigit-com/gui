const express = require('express');
const cors = require('cors');
const proxyRequest = require('./utils/proxyRequest');

const app = express();
app.use(cors());
app.use(express.json());

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:5000';

// Repository files
app.get('/api/repository-files', (req, res) => proxyRequest(req, res, '/api/repository-files', BACKEND_URL));

// Organizations
app.get('/api/organizations', (req, res) => proxyRequest(req, res, '/api/organizations', BACKEND_URL));

// Move repository
app.post('/api/move-repository', (req, res) => proxyRequest(req, res, '/api/move-repository', BACKEND_URL));

// Remove repository
app.post('/api/remove-repository', (req, res) => proxyRequest(req, res, '/api/remove-repository', BACKEND_URL));

// Repositories
app.get('/api/repositories', (req, res) => proxyRequest(req, res, '/api/repositories', BACKEND_URL));

// README
app.get('/api/readme', (req, res) => proxyRequest(req, res, '/api/readme', BACKEND_URL));

// Set repo
app.post('/api/repo', (req, res) => proxyRequest(req, res, '/api/repo', BACKEND_URL));

// Get repo
app.get('/api/repo', (req, res) => proxyRequest(req, res, '/api/repo', BACKEND_URL));

// New routes for renaming
app.post('/api/rename-organization', (req, res) => proxyRequest(req, res, '/api/rename-organization', BACKEND_URL));
app.post('/api/rename-repository', (req, res) => proxyRequest(req, res, '/api/rename-repository', BACKEND_URL));

function startServer(port) {
  app.listen(port, () => {
    console.log(`API server running on port ${port}`);
    console.log(`BACKEND_URL is set to: ${BACKEND_URL}`);
  }).on('error', (err) => {
    if (err.code === 'EADDRINUSE') {
      console.log(`Port ${port} is busy, trying ${port + 1}`);
      startServer(port + 1);
    } else {
      console.error('Server error:', err);
    }
  });
}

const PORT = process.env.PORT || 3001;
startServer(PORT);

module.exports = app;
