import os
import json
from flask import Flask, request, Response
from flask_cors import CORS
from dotenv import load_dotenv
from together import Together

# Load environment variables from .env file, forcing UTF-8
load_dotenv(encoding='utf-8')

# Initialize the Flask application
app = Flask(__name__)

# Enable CORS to allow cross-origin requests from the frontend
CORS(app)

# Initialize the Together client with robust error handling
try:
    client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
    # Perform a simple check to validate the API key on startup
    client.models.list() 
except Exception as e:
    print("-" * 60)
    print("FATAL ERROR: Could not connect to Together AI.")
    print("This is almost certainly due to an invalid TOGETHER_API_KEY.")
    print("Please regenerate your key, update your .env file, and restart.")
    print(f"Underlying error: {e}")
    print("-" * 60)
    exit() # Exit because the app is unusable without the client

@app.route('/api/test', methods=['GET'])
def test_connection():
    """A simple test endpoint to verify the backend is running."""
    response_data = json.dumps({'message': 'Backend is running!'})
    return Response(response_data, mimetype='application/json; charset=utf-8')

@app.route('/api/dilemma', methods=['POST'])
def generate_dilemma():
    """Generates a moral dilemma using the Together AI API."""
    try:
        response = client.chat.completions.create(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            messages=[
                {"role": "system", "content": "You are an ethical dilemma generator."},
                {"role": "user", "content": "Generate a realistic and thought-provoking moral dilemma. The dilemma should be concise, present a difficult choice without an obvious right answer, and be suitable for a general audience. Please provide only the dilemma text."}
            ]
        )
        dilemma = response.choices[0].message.content.strip()
        response_data = json.dumps({'dilemma': dilemma}, ensure_ascii=False)
        return Response(response_data, mimetype='application/json; charset=utf-8')
    except Exception as e:
        # Sanitize the error message to ensure it's clean UTF-8
        error_message = str(e).encode('utf-8', 'replace').decode('utf-8')
        response_data = json.dumps({'error': error_message})
        return Response(response_data, status=500, mimetype='application/json; charset=utf-8')

@app.route('/api/analyze/comparative', methods=['POST'])
def analyze_dilemma_comparative():
    """Analyzes a dilemma from three core ethical frameworks."""
    data = request.get_json()
    dilemma = data.get('dilemma')

    if not dilemma:
        return Response(json.dumps({'error': 'Missing dilemma'}), status=400, mimetype='application/json; charset=utf-8')

    frameworks = ["Utilitarianism", "Deontology", "Virtue Ethics"]
    analyses = {}

    try:
        for framework in frameworks:
            prompt = f"""Analyze the following ethical dilemma from the perspective of {framework}:

Dilemma: {dilemma}

Please provide a detailed analysis that explains how a follower of {framework} would approach this situation. Discuss the core principles of the framework and how they apply to the dilemma, and suggest a likely course of action.
"""
            response = client.chat.completions.create(
                model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                messages=[
                    {"role": "system", "content": "You are an expert in ethical frameworks."},
                    {"role": "user", "content": prompt}
                ]
            )
            analyses[framework] = response.choices[0].message.content.strip()
        
        response_data = json.dumps({'analyses': analyses}, ensure_ascii=False)
        return Response(response_data, mimetype='application/json; charset=utf-8')

    except Exception as e:
        error_message = str(e).encode('utf-8', 'replace').decode('utf-8')
        response_data = json.dumps({'error': error_message})
        return Response(response_data, status=500, mimetype='application/json; charset=utf-8')

@app.route('/api/analyze', methods=['POST'])
def analyze_dilemma():
    """Analyzes a dilemma based on a selected ethical framework using Together AI."""
    data = request.get_json()
    dilemma = data.get('dilemma')
    framework = data.get('framework')

    if not all([dilemma, framework]):
        error_message = 'Missing dilemma or framework'
        response_data = json.dumps({'error': error_message})
        return Response(response_data, status=400, mimetype='application/json; charset=utf-8')

    try:
        prompt = f"""Analyze the following ethical dilemma from the perspective of {framework}:

Dilemma: {dilemma}

Please provide a detailed analysis that explains how a follower of {framework} would approach this situation. Discuss the core principles of the framework and how they apply to the dilemma, and suggest a likely course of action.
"""
        response = client.chat.completions.create(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            messages=[
                {"role": "system", "content": "You are an expert in ethical frameworks and moral philosophy."},
                {"role": "user", "content": prompt}
            ]
        )
        analysis = response.choices[0].message.content.strip()
        response_data = json.dumps({'analysis': analysis}, ensure_ascii=False)
        return Response(response_data, mimetype='application/json; charset=utf-8')
    except Exception as e:
        # Sanitize the error message to ensure it's clean UTF-8
        error_message = str(e).encode('utf-8', 'replace').decode('utf-8')
        response_data = json.dumps({'error': error_message})
        return Response(response_data, status=500, mimetype='application/json; charset=utf-8')

if __name__ == '__main__':
    app.run(debug=True)
