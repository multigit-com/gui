const express = require('express');
const cors = require('cors');
const axios = require('axios');

const app = express();
app.use(cors());
app.use(express.json());

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:5000';

// Proxy middleware function
const proxyRequest = async (req, res, endpoint) => {
  const maxRetries = 3;
  let retries = 0;

  while (retries < maxRetries) {
    try {
      const response = await axios({
        method: req.method,
        url: `${BACKEND_URL}${endpoint}`,
        params: req.query,
        data: req.body,
      });
      return res.json(response.data);
    } catch (error) {
      if (error.response && error.response.status === 403 && error.response.data.message.includes('API rate limit exceeded')) {
        retries++;
        console.log(`Rate limit exceeded. Retrying in ${2 ** retries} seconds...`);
        await new Promise(resolve => setTimeout(resolve, 1000 * (2 ** retries)));
      } else {
        console.error(`Error in ${endpoint}:`, error.response ? error.response.data : error.message);
        return res.status(error.response ? error.response.status : 500).json({ 
          error: `Failed to ${req.method} ${endpoint}`, 
          details: error.response ? error.response.data : error.message 
        });
      }
    }
  }

  console.error(`Failed after ${maxRetries} retries`);
  res.status(429).json({ error: 'Rate limit exceeded. Please try again later.' });
};

// Repository files
app.get('/api/repository-files', (req, res) => proxyRequest(req, res, '/api/repository-files'));

// Organizations
app.get('/api/organizations', (req, res) => proxyRequest(req, res, '/api/organizations'));

// Move repository
app.post('/api/move-repository', (req, res) => proxyRequest(req, res, '/api/move-repository'));

// Remove repository
app.post('/api/remove-repository', (req, res) => proxyRequest(req, res, '/api/remove-repository'));

// Repositories
app.get('/api/repositories', (req, res) => proxyRequest(req, res, '/api/repositories'));

// README
app.get('/api/readme', (req, res) => proxyRequest(req, res, '/api/readme'));

// Set repo
app.post('/api/repo', (req, res) => proxyRequest(req, res, '/api/repo'));

// Get repo
app.get('/api/repo', (req, res) => proxyRequest(req, res, '/api/repo'));

// New routes for renaming
app.post('/api/rename-organization', (req, res) => proxyRequest(req, res, '/api/rename-organization'));
app.post('/api/rename-repository', (req, res) => proxyRequest(req, res, '/api/rename-repository'));

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
