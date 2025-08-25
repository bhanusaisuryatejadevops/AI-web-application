from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TEXT_API_URL = os.getenv("TEXT_API_URL", "http://text-processing.com/api/sentiment/")

@app.route("/")
def home():
    return jsonify({"message": "AI App is running!"})

@app.route("/analyze", methods=["GET"])
def analyze():
    text = request.args.get("text")
    if not text:
        return jsonify({"error": "Please provide text parameter"}), 400

    try:
        response = requests.post(TEXT_API_URL, data={"text": text})
        if response.status_code == 200:
            result = response.json()
            return jsonify({
                "input": text,
                "sentiment": result.get("label")
            })
        else:
            return jsonify({"error": "AI API error", "status": response.status_code}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
