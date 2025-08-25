from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TEXT_API_URL = os.getenv("TEXT_API_URL", "http://text-processing.com/api/sentiment/")

@app.route("/")
def home():
    return jsonify({"message": "AI App is running!"})

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Text input is required"}), 400

    text = data["text"]
    try:
        response = requests.post(TEXT_API_URL, data={"text": text})
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "AI API error", "status": response.status_code}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
