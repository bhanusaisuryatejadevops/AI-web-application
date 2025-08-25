from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TEXT_API_URL = os.getenv("TEXT_API_URL", "http://text-processing.com/api/sentiment/")
EXTERNAL_API_TIMEOUT = int(os.getenv("EXTERNAL_API_TIMEOUT", 10))

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "AI App is running!"})

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Text input is required"}), 400

    try:
        response = requests.post(TEXT_API_URL, data={"text": data["text"]}, timeout=EXTERNAL_API_TIMEOUT)
        if response.status_code == 200:
            return jsonify({"input": data["text"], "result": response.json()})
        else:
            return jsonify({"error": "AI API error", "status": response.status_code}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "External API call failed", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
