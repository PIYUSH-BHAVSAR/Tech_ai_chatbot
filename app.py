from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Load API key from environment variable (More secure for deployment)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    input_text = request.json.get('inputText')
    if not input_text:
        return jsonify({'error': 'No input text provided'}), 400

    if not GEMINI_API_KEY:
        return jsonify({'error': 'Gemini API Key is missing'}), 500

    data = {"contents": [{"parts": [{"text": input_text}]}]}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}",
            json=data, headers=headers
        )
        response.raise_for_status()
        bot_response = response.json()

        # Extract response text safely
        content_text = None
        if 'candidates' in bot_response and bot_response['candidates']:
            first_candidate = bot_response['candidates'][0]
            if 'content' in first_candidate and 'parts' in first_candidate['content']:
                content_text = first_candidate['content']['parts'][0].get('text', '')

        return jsonify({'response': content_text if content_text else "I'm not sure how to respond to that."})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
