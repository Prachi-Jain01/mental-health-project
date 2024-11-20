# Mental Health Project: Toxic Comment Classifier

This web application predicts whether a comment is toxic or non-toxic using a fine-tuned machine learning model enhanced with emotion detection features. It is designed to promote healthier online discussions by identifying potentially harmful content.

---

## Features

- **Toxic Comment Detection**: Classifies comments as toxic or non-toxic.
- **Emotion-Based Insights**: Utilizes emotion detection from `nateraw/bert-base-uncased-emotion` for enhanced accuracy.
- **Interactive Web App**: Easy-to-use interface for entering and analyzing comments.

---

## Installation

1. **Clone the Repository**  
   Clone the project to your local machine:  
   ```bash
   git clone https://github.com/Prachi-Jain01/mental-health-project.git
   cd mental-health-project
   ```

2. **Install Dependencies**

   **Backend**:  
   Install the required Python libraries:  
   ```bash
   pip install -r requirements.txt
   ```

   **Frontend**:  
   Navigate to the `mhp` directory and install the Node.js dependencies:  
   ```bash
   cd mhp
   npm install
   ```

3. **Download the Pre-Trained Model**  
   Download the fine-tuned model from this link.  
   Place the downloaded file in the `backend/app/model/` directory.

---

## Usage

### Start the Backend

Navigate to the `backend` directory and run:  
```bash
uvicorn app.main:app --reload
```

### Start the Frontend

Navigate to the `mhp` directory and run:  
```bash
npm start
```

After successful compilation, the app will be available at:

- Local: http://localhost:3000
- Network: http://<your-network-ip>:3000

---

## Analyze Comments

1. Open the web app in your browser.
2. Enter a comment in the text input field.
3. Click the **Get Insights** button to classify the comment and view emotion-based insights.

---

## Project Structure

```
mental-health-project/
│
├── backend/                  # Backend API and model logic
│   ├── app/
│   │   ├── model/
│   │   │   ├── fine_tuned_model.ckpt  # Fine-tuned model
│   │   │   ├── model_utils.py         # Utility functions for the model
│   │   │   ├── mhp_classifier.py      # Classification logic
│   │   ├── main.py                    # Entry point for the backend
│   │   ├── config.py                  # Configuration settings
│   │   ├── schemas.py                 # Data schemas
│
├── mhp/                      # Frontend React app
│   ├── src/                  # React source files
│   ├── public/               # Public assets
│   ├── package.json          # Frontend dependencies
│
├── requirements.txt          # Backend and project dependencies
├── README.md                 # Project documentation
```

---

## Acknowledgements

- **Emotion Detection**: Powered by `nateraw/bert-base-uncased-emotion`.
- **Toxic Comment Classification**: Fine-tuned RoBERTa model.
- **Frontend Framework**: Built with React.

---

