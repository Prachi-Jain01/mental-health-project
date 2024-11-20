import React, { useState } from "react";
import "./App.css"; // Import the CSS file

const EmotionPredictor = () => {
  const [comment, setComment] = useState("");
  const [emotions, setEmotions] = useState([]);
  const [prediction, setPrediction] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [facts, setFacts] = useState([
    "Talking about your feelings can help you manage stress.",
    "Mental health is just as important as physical health.",
    "Taking breaks can improve productivity and well-being.",
    "Exercise can significantly reduce symptoms of depression and anxiety.",
    "There is no shame in seeking professional help for mental health.",
  ]);

  // Handle comment change
  const handleInputChange = (event) => {
    setComment(event.target.value);
  };

  // Handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    setEmotions([]);
    setPrediction("");

    try {
      // Send the comment to FastAPI backend
      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: comment }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch from backend");
      }

      const data = await response.json();
      setEmotions(data.emotions);
      setPrediction(data.prediction);
    } catch (error) {
      setError("Error fetching prediction. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="card">
        <h2 className="title">Mental Health Predictor</h2>
        <form onSubmit={handleSubmit} className="form">
          <div className="form-group">
            <label htmlFor="comment" className="form-label">
              Enter your comment or feeling:
            </label>
            <textarea
              id="comment"
              rows="4"
              className="form-input"
              value={comment}
              onChange={handleInputChange}
              placeholder="How are you feeling today?"
            />
          </div>

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? "Processing..." : "Predict Emotions"}
          </button>
        </form>

        {error && <p className="error-text">{error}</p>}

        {emotions.length > 0 && (
          <div className="emotions-output">
            <h3 className="output-title">Detected Emotions:</h3>
            <ul>
              {emotions.map((emotion, index) => (
                <li key={index} className="emotion-item">
                  <span>{Object.keys(emotion)[0]}</span>
                  <span className="emotion-score">
                    {Object.values(emotion)[0].toFixed(2)}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {prediction && (
          <div className="prediction-result">
            <h3 className="output-title">Prediction Result:</h3>
            <p
              className={`prediction-text ${
                prediction === "Unhealthy" ? "negative" : "positive"
              }`}
            >
              {prediction}
            </p>
          </div>
        )}

        {/* Display Mental Health Facts */}
        {/* <div className="facts-container">
        <h3>Mental Health Tips 💡</h3>
        <ul className="facts-list">
          {facts.map((fact, index) => (
            <li key={index} className="fact-item">{fact}</li>
          ))}
        </ul>
      </div> */}
      </div>
    </div>
  );
};

export default EmotionPredictor;
