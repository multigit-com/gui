const fs = require('fs');
const path = require('path');

const htmlFilePath = path.join(__dirname, 'public', 'blocks.html');
let htmlContent = fs.readFileSync(htmlFilePath, 'utf8');

const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:3001';
htmlContent = htmlContent.replace('<!-- REACT_APP_API_URL -->', apiUrl);

fs.writeFileSync(htmlFilePath, htmlContent);

console.log('Placeholders replaced successfully.');
