from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TEXT_API_URL = os.getenv("TEXT_API_URL", "http://text-processing.com/api/sentiment/")
TIMEOUT = int(os.getenv("EXTERNAL_API_TIMEOUT", "10"))

@app.route("/")
def index():
    return jsonify({"message": "AI App is running!"}), 200

@app.route("/analyze", methods=["POST"])
def analyze_sentiment():
    try:
        data = request.json
        text = data.get("text", "")
        if not text:
            return jsonify({"error": "No text provided"}), 400

        response = requests.post(TEXT_API_URL, data={"text": text}, timeout=TIMEOUT)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
