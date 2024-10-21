import React, { useState } from 'react';
import { getRepoNameFromUrl, getOrgNameFromUrl } from '../utils/githubUrlParser';

const ExampleComponent = () => {
  const [url, setUrl] = useState('');
  const [org, setOrg] = useState('');
  const [repo, setRepo] = useState('');

  const handleUrlChange = (e) => {
    const newUrl = e.target.value;
    setUrl(newUrl);
    setOrg(getOrgNameFromUrl(newUrl) || '');
    setRepo(getRepoNameFromUrl(newUrl) || '');
  };

  return (
    <div>
      <input
        type="text"
        value={url}
        onChange={handleUrlChange}
        placeholder="Enter GitHub URL"
      />
      <p>Organization: {org}</p>
      <p>Repository: {repo}</p>
    </div>
  );
};

export default ExampleComponent;
