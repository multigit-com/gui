import React, { useState, useEffect } from 'react';

function App() {
  const [commands, setCommands] = useState([]);
  const [inputs, setInputs] = useState({});
  const [results, setResults] = useState({});
  const [auditLog, setAuditLog] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('http://localhost:3001/api/scripts')
      .then(response => response.json())
      .then(data => {
        setCommands(data);
        const initialInputs = {};
        data.forEach(command => {
          initialInputs[command] = command === 'move_repository' ? ['', ''] : '';
        });
        setInputs(initialInputs);
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

  const handleInputChange = (command, value, index = 0) => {
    setInputs(prevInputs => ({
      ...prevInputs,
      [command]: Array.isArray(prevInputs[command])
        ? prevInputs[command].map((v, i) => i === index ? value : v)
        : value
    }));
  };

  const handleSubmit = async () => {
    setError(null);
    const promises = commands.map(command => {
      const input = inputs[command];
      if (input && (typeof input === 'string' ? input.trim() !== '' : input.some(v => v.trim() !== ''))) {
        return fetch('http://localhost:5000/api/execute', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
            command, 
            input: Array.isArray(input) ? input : [input] 
          }),
        })
        .then(response => response.json())
        .then(data => ({ command, data }))
        .catch(err => ({ command, error: err.message }));
      }
      return null;
    }).filter(Boolean);

    try {
      const results = await Promise.all(promises);
      const newResults = {};
      results.forEach(({ command, data, error }) => {
        newResults[command] = error || data;
      });
      setResults(newResults);
      fetchAuditLog();
    } catch (err) {
      setError('Failed to execute commands: ' + err.message);
    }
  };

  return (
    <div>
      <h1>GitHub Repository Manager</h1>
      {error && <p style={{color: 'red'}}>{error}</p>}
      <table>
        <thead>
          <tr>
            <th>Command</th>
            <th>Input</th>
            <th>Result</th>
          </tr>
        </thead>
        <tbody>
          {commands.map(command => (
            <tr key={command}>
              <td>{command}</td>
              <td>
                {Array.isArray(inputs[command]) ? (
                  <>
                    <input
                      type="text"
                      value={inputs[command][0] || ''}
                      onChange={(e) => handleInputChange(command, e.target.value, 0)}
                      placeholder="Source URL"
                    />
                    <input
                      type="text"
                      value={inputs[command][1] || ''}
                      onChange={(e) => handleInputChange(command, e.target.value, 1)}
                      placeholder="Target URL"
                    />
                  </>
                ) : (
                  <input
                    type="text"
                    value={inputs[command] || ''}
                    onChange={(e) => handleInputChange(command, e.target.value)}
                    placeholder="Enter input"
                  />
                )}
              </td>
              <td>
                {results[command] && (
                  <pre>{JSON.stringify(results[command], null, 2)}</pre>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <button onClick={handleSubmit}>Execute All</button>
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
