const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();

app.use(express.json());
app.use(express.static('public'));

const ENV_FILE_PATH = path.join(__dirname, '..', '.env');

app.post('/update-token', (req, res) => {
  const { token } = req.body;
  
  if (!token) {
    return res.status(400).json({ error: 'Token is required' });
  }

  const envContent = `GITLAB_TOKEN=${token}\n`;

  fs.writeFile(ENV_FILE_PATH, envContent, (err) => {
    if (err) {
      console.error('Error writing to .env file:', err);
      return res.status(500).json({ error: 'Failed to update token' });
    }
    res.json({ message: 'GitLab token updated successfully' });
  });
});

const PORT = process.env.PORT || 3003;
app.listen(PORT, () => {
  console.log(`GitLab Token updater service running on port ${PORT}`);
});
