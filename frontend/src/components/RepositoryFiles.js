import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchRepositoryFiles } from '../actions/repositoryActions';

const RepositoryFiles = ({ org, repo }) => {
  const dispatch = useDispatch();
  const { files, loading, error } = useSelector(state => state.repository);

  useEffect(() => {
    if (org && repo) {
      dispatch(fetchRepositoryFiles(org, repo));
    }
  }, [org, repo, dispatch]);

  useEffect(() => {
    console.log('Files in component:', files);
  }, [files]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  const formatSize = (size) => {
    const units = ['B', 'KB', 'MB', 'GB'];
    let unitIndex = 0;
    while (size >= 1024 && unitIndex < units.length - 1) {
      size /= 1024;
      unitIndex++;
    }
    return `${size.toFixed(2)} ${units[unitIndex]}`;
  };

  return (
    <div>
      <h2>Repository Files</h2>
      {files.length === 0 ? (
        <p>No files found in this repository.</p>
      ) : (
        <ul>
          {files.map((file, index) => (
            <li key={index}>
              {file.name} ({formatSize(file.size)}) - {file.type}
              <br />
              <small>Path: {file.path}</small>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default RepositoryFiles;
