import React, { useState } from 'react';

const DilemmaDisplay = ({ dilemma, onGenerateDilemma }) => {
    const [customDilemma, setCustomDilemma] = useState('');
    const [analyses, setAnalyses] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleAnalyze = async () => {
        const dilemmaToAnalyze = customDilemma.trim() || dilemma;
        if (!dilemmaToAnalyze) {
            setError('Please generate or enter a dilemma first.');
            return;
        }

        setLoading(true);
        setError('');
        setAnalyses(null);

        try {
            const response = await fetch('http://127.0.0.1:5000/api/analyze/comparative', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ dilemma: dilemmaToAnalyze }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            setAnalyses(data.analyses);
        } catch (e) {
            setError(e.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="dilemma-container">
            <div className="dilemma-text">
                <p>{dilemma || 'Click the button above to generate a new dilemma.'}</p>
            </div>

            <div className="custom-dilemma-section">
                <textarea
                    className="custom-dilemma-input"
                    placeholder="Or, enter your own dilemma here..."
                    value={customDilemma}
                    onChange={(e) => setCustomDilemma(e.target.value)}
                />
            </div>

            <button onClick={handleAnalyze} disabled={loading || (!dilemma && !customDilemma.trim())}>
                {loading ? 'Analyzing...' : 'Run Comparative Analysis'}
            </button>

            {error && <p className="error-text">Error: {error}</p>}

            {analyses && (
                <div className="analysis-section-comparative">
                    {Object.entries(analyses).map(([framework, text]) => (
                        <div key={framework} className="analysis-column">
                            <h3>{framework}</h3>
                            <p>{text}</p>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default DilemmaDisplay;
