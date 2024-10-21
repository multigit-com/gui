const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
const { exec } = require('child_process');

const app = express();
app.use(cors());
app.use(express.json());

const SCRIPTS_DIR = path.join(__dirname, '..', 'backend', 'scripts');
const BACKEND_URL = process.env.BACKEND_URL || 'http://backend:5000';

app.get('/api/scripts', (req, res) => {
  fs.readdir(SCRIPTS_DIR, (err, files) => {
    if (err) {
      res.status(500).json({ error: 'Failed to read scripts directory' });
    } else {
      const scripts = files
        .filter(file => file.endsWith('.py'))
        .map(file => path.parse(file).name);
      res.json(scripts);
    }
  });
});

app.get('/api/repositories', (req, res) => {
  const { org } = req.query;
  if (!org) {
    return res.status(400).json({ error: 'Organization parameter is required' });
  }

  const scriptPath = path.join(SCRIPTS_DIR, 'list_repositories.py');
  exec(`python ${scriptPath} ${org}`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing script: ${error}`);
      return res.status(500).json({ error: 'Failed to list repositories' });
    }
    if (stderr) {
      console.error(`Script error: ${stderr}`);
      return res.status(500).json({ error: 'Script error occurred' });
    }
    try {
      const repositories = JSON.parse(stdout);
      res.json(repositories);
    } catch (parseError) {
      console.error(`Error parsing script output: ${parseError}`);
      res.status(500).json({ error: 'Failed to parse repository list' });
    }
  });
});

app.post('/api/move-repository', (req, res) => {
  const { repoId, sourceOrgId, targetOrgId } = req.body;
  if (!repoId || !sourceOrgId || !targetOrgId) {
    return res.status(400).json({ error: 'Missing required parameters' });
  }

  const scriptPath = path.join(SCRIPTS_DIR, 'move_repository.py');
  exec(`python ${scriptPath} ${repoId} ${sourceOrgId} ${targetOrgId}`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing script: ${error}`);
      return res.status(500).json({ error: 'Failed to move repository' });
    }
    if (stderr) {
      console.error(`Script error: ${stderr}`);
      return res.status(500).json({ error: 'Script error occurred' });
    }
    try {
      const result = JSON.parse(stdout);
      res.json(result);
    } catch (parseError) {
      console.error(`Error parsing script output: ${parseError}`);
      res.status(500).json({ error: 'Failed to parse move result' });
    }
  });
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`API server running on port ${PORT}`);
});

// Add this at the end of the file
module.exports = app;
