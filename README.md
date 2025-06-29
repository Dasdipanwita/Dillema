# Ethical Dilemma Simulator

This project is a web-based application that uses a large language model (LLM) to generate and analyze complex ethical dilemmas. It provides users with a tool to explore moral philosophy by presenting dilemmas and offering reasoned analyses from the perspectives of three major ethical frameworks: Utilitarianism, Deontology, and Virtue Ethics.

## Core Features

- **Dynamic Dilemma Generation**: Generates unique and thought-provoking moral dilemmas on demand.
- **User-Submitted Dilemmas**: Allows users to input their own custom dilemmas for analysis.
- **Comparative Framework Analysis**: Provides a side-by-side comparison of how Utilitarianism, Deontology, and Virtue Ethics would approach a given dilemma.
- **Detailed Reasoning**: For each framework, the application offers a detailed explanation of the core principles and how they apply to the situation.
- **Interactive Web Interface**: A clean and simple UI built with React for a seamless user experience.

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: React (JavaScript)
- **LLM API**: Together AI (running the Mixtral-8x7B-Instruct-v0.1 model)
- **Styling**: Plain CSS

## Project Structure

```
Dillema/
├── backend/
│   ├── venv/                 # Python virtual environment
│   ├── app.py                # Main Flask application
│   ├── requirements.txt      # Backend dependencies
│   └── .env                  # Environment variables (API key)
├── frontend/
│   ├── public/
│   │   └── index.html        # Main HTML file
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   ├── App.css           # Main stylesheet
│   │   ├── DilemmaDisplay.js # Component for dilemma/analysis UI
│   │   └── index.js          # React entry point
│   └── package.json          # Frontend dependencies
└── README.md                 # This file
```

## Setup and Installation

### Prerequisites

- Python 3.8+ and Pip
- Node.js and npm

### 1. Backend Setup

First, navigate to the backend directory and set up the Python environment.

```bash
# Navigate to the backend folder
cd backend

# Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install the required Python packages
pip install -r requirements.txt
```

### 2. Frontend Setup

Next, open a **new terminal**, navigate to the frontend directory, and install the Node.js dependencies.

```bash
# Navigate to the frontend folder
cd frontend

# Install the required npm packages
npm install
```

### 3. API Key Configuration

The application requires an API key from Together AI to function.

1.  Create a `.env` file inside the `backend` directory.
2.  Sign up for an account at [Together.ai](https://www.together.ai/).
3.  Navigate to your [API Keys dashboard](https://api.together.ai/settings/api-keys) and generate a new key.
4.  Open the `backend/.env` file and paste your key into it, like so:

    ```
    TOGETHER_API_KEY=your_api_key_goes_here
    ```

## How to Run the Application

You must have two terminals open to run both the backend and frontend servers.

**Terminal 1: Start the Backend (Flask)**

```bash
# Make sure you are in the backend/ directory with the venv active
cd backend
python app.py
```

The backend server will start on `http://127.0.0.1:5000`.

**Terminal 2: Start the Frontend (React)**

```bash
# Make sure you are in the frontend/ directory
cd frontend
npm start
```

The frontend development server will start and automatically open the application in your web browser at `http://localhost:3000`.
