import React, { useState, useEffect } from 'react';

function App() {
  const [commands, setCommands] = useState([]);
  const [selectedCommand, setSelectedCommand] = useState('');
  const [input, setInput] = useState('');
  const [result, setResult] = useState(null);
  const [auditLog, setAuditLog] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('http://localhost:3001/api/scripts')
      .then(response => response.json())
      .then(data => {
        setCommands(data);
        if (data.length > 0) {
          setSelectedCommand(data[0]);
        }
      })
      .catch(err => setError('Failed to fetch commands: ' + err.message));

    fetchAuditLog();
  }, []);

  const fetchAuditLog = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/audit-log');
      if (!response.ok) throw new Error('Network response was not ok');
      const data = await response.json();
      setAuditLog(data);
    } catch (err) {
      setError('Failed to fetch audit log: ' + err.message);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      const response = await fetch('http://localhost:5000/api/execute', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ command: selectedCommand, input }),
      });
      if (!response.ok) throw new Error('Network response was not ok');
      const data = await response.json();
      setResult(data);
      fetchAuditLog();
    } catch (err) {
      setError('Failed to execute command: ' + err.message);
    }
  };

  return (
    <div>
      <h1>GitHub Repository Manager</h1>
      {error && <p style={{color: 'red'}}>{error}</p>}
      <p>
        Need to update your GitHub token? {' '}
        <a href="http://localhost:3002" target="_blank" rel="noopener noreferrer">
          Click here to open the Token Updater
        </a>
      </p>
      <form onSubmit={handleSubmit}>
        <select
          value={selectedCommand}
          onChange={(e) => setSelectedCommand(e.target.value)}
        >
          {commands.map(command => (
            <option key={command} value={command}>{command}</option>
          ))}
        </select>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter input"
        />
        <button type="submit">Execute</button>
      </form>
      {result && (
        <div>
          <h2>Result:</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
      <div>
        <h2>Audit Log:</h2>
        <ul>
          {auditLog.map((entry, index) => (
            <li key={index}>
              {entry.timestamp}: {entry.action} - {entry.details}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
