const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

const SCRIPTS_DIR = path.join(__dirname, '..', 'backend', 'scripts');

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

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`API server running on port ${PORT}`);
});
