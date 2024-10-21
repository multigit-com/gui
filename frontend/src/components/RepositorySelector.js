import React, { useState, useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { fetchRepositories, setCurrentRepository } from '../actions/repositoryActions';

const RepositorySelector = () => {
  const [organizations, setOrganizations] = useState([]);
  const [selectedOrg, setSelectedOrg] = useState('');
  const [repositories, setRepositories] = useState([]);
  const [selectedRepo, setSelectedRepo] = useState('');
  const dispatch = useDispatch();

  useEffect(() => {
    // Fetch organizations when component mounts
    fetchOrganizations();
  }, []);

  useEffect(() => {
    if (selectedOrg) {
      fetchRepositories(selectedOrg);
    }
  }, [selectedOrg]);

  const handleOrgChange = (e) => {
    setSelectedOrg(e.target.value);
    setSelectedRepo('');
  };

  const handleRepoChange = (e) => {
    setSelectedRepo(e.target.value);
    if (selectedOrg && e.target.value) {
      dispatch(setCurrentRepository(selectedOrg, e.target.value));
    }
  };

  // ... (implement fetchOrganizations and fetchRepositories)

  return (
    <div>
      <select value={selectedOrg} onChange={handleOrgChange}>
        <option value="">Select an organization</option>
        {organizations.map(org => (
          <option key={org.id} value={org.login}>{org.login}</option>
        ))}
      </select>
      <select value={selectedRepo} onChange={handleRepoChange} disabled={!selectedOrg}>
        <option value="">Select a repository</option>
        {repositories.map(repo => (
          <option key={repo.id} value={repo.name}>{repo.name}</option>
        ))}
      </select>
    </div>
  );
};

export default RepositorySelector;
