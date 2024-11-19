// frontend/src/components/Result.js
import React from 'react';

function Result({ result }) {
  return (
    <div>
      <h3>Model Output:</h3>
      <p>Prediction: {result.prediction}</p>
      <p>Emotions:</p>
      <ul>
        {result.emotions.map((emotion, index) => (
          <li key={index}>
            {emotion.label}: {emotion.score.toFixed(2)}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Result;
