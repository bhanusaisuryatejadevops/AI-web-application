from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Health Check
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "AI App is running!"})

# Sentiment Analysis Endpoint
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Text is required"}), 400

    text = data["text"]

    # External API for sentiment analysis
    try:
        response = requests.post(
            "http://text-processing.com/api/sentiment/",
            data={"text": text},
            timeout=10
        )
        if response.status_code == 200:
            result = response.json()
            return jsonify(result)
        else:
            return jsonify({"error": "External API error"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
