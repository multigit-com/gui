const express = require('express');
const { exec } = require('child_process');
const cors = require('cors');
const axios = require('axios');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:5000';
const SCRIPTS_DIR = path.join(__dirname, 'backend', 'scripts');

app.get('/api/repository-files', async (req, res) => {
  try {
    const response = await axios.get(`${BACKEND_URL}/api/repository-files`, {
      params: req.query
    });
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch repository files' });
  }
});

app.get('/api/organizations', async (req, res) => {
  try {
    const response = await axios.get(`${BACKEND_URL}/api/organizations`);
    res.json(response.data);
  } catch (error) {
    console.error('Error fetching organizations:', error);
    res.status(500).json({ error: 'Failed to fetch organizations' });
  }
});

app.post('/api/move-repository', (req, res) => {
    const { repoId, sourceOrgId, targetOrgId } = req.body;
    
    exec(`python ${path.join(SCRIPTS_DIR, 'move_repository.py')} ${repoId} ${sourceOrgId} ${targetOrgId}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing script: ${error}`);
            return res.status(500).json({ success: false, message: 'Failed to move repository' });
        }
        if (stderr) {
            console.error(`Script error: ${stderr}`);
            return res.status(500).json({ success: false, message: 'Script error occurred' });
        }
        try {
            const result = JSON.parse(stdout);
            res.json(result);
        } catch (parseError) {
            console.error(`Error parsing script output: ${parseError}`);
            res.status(500).json({ success: false, message: 'Failed to parse move result' });
        }
    });
});

app.post('/api/remove-repository', async (req, res) => {
  try {
    const response = await axios.post(`${BACKEND_URL}/api/remove-repository`, req.body);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to remove repository' });
  }
});

app.get('/api/repositories', async (req, res) => {
  const { org } = req.query;
  
  if (!org) {
    return res.status(400).json({ error: 'Organization parameter is required' });
  }

  try {
    console.log(`Fetching repositories for org: ${org}`);
    console.log(`Making request to: ${BACKEND_URL}/api/repositories?org=${org}`);
    const response = await axios.get(`${BACKEND_URL}/api/repositories`, {
      params: { org }
    });
    console.log('Response from backend:', response.data);
    res.json(response.data);
  } catch (error) {
    console.error('Error fetching repositories:', error.response ? error.response.data : error.message);
    res.status(500).json({ error: 'Failed to fetch repositories', details: error.message });
  }
});

function startServer(port) {
  app.listen(port, () => {
    console.log(`API server running on port ${port}`);
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
app.listen(PORT, () => {
  console.log(`API server running on port ${PORT}`);
  console.log(`BACKEND_URL is set to: ${BACKEND_URL}`);
});

// Add this at the end of the file
module.exports = app;
