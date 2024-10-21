const axios = require('axios');

const proxyRequest = async (req, res, endpoint, BACKEND_URL) => {
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

module.exports = proxyRequest;
