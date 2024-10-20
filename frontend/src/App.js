import React, { useState, useEffect } from 'react';

function App() {
  const [commands, setCommands] = useState([]);
  const [selectedCommand, setSelectedCommand] = useState('');
  const [input, setInput] = useState('');
  const [result, setResult] = useState(null);

  useEffect(() => {
    fetch('http://localhost:3001/api/scripts')
      .then(response => response.json())
      .then(data => {
        setCommands(data);
        if (data.length > 0) {
          setSelectedCommand(data[0]);
        }
      });
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('http://localhost:5000/api/execute', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ command: selectedCommand, input }),
    });
    const data = await response.json();
    setResult(data);
  };

  return (
    <div>
      <h1>GitHub Repository Manager</h1>
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
    </div>
  );
}

export default App;
