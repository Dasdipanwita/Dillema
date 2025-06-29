import React, { useState, useEffect } from 'react';
import DilemmaDisplay from './DilemmaDisplay';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [dilemma, setDilemma] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    // Fetch the test message from the backend
    fetch('/api/test')
      .then((response) => response.json())
      .then((data) => setMessage(data.message))
      .catch((error) => console.error('Error fetching test data:', error));
  }, []);

  const generateDilemma = () => {
    setLoading(true);
    setError('');
    setDilemma('');

    fetch('/api/dilemma', { method: 'POST' })
      .then((response) => {
        // If the response is not OK, parse the JSON to get the error message
        if (!response.ok) {
          return response.json().then(errorData => {
            throw new Error(errorData.error || 'An unexpected server error occurred.');
          });
        }
        return response.json();
      })
      .then((data) => {
        if (data.error) {
          throw new Error(data.error);
        }
        setDilemma(data.dilemma);
      })
      .catch((error) => setError(error.message))
      .finally(() => setLoading(false));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Ethical Dilemma Simulator</h1>
        <p>{message}</p>
        <button onClick={generateDilemma} disabled={loading}>
          {loading ? 'Generating...' : 'Generate New Dilemma'}
        </button>
        {error && <p className="error-text">Error: {error}</p>}
        <DilemmaDisplay dilemma={dilemma} />
      </header>
    </div>
  );
}

export default App;
