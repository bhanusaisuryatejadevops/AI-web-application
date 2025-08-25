from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

@app.route("/")
def root():
    return jsonify({"message": "AI App is running!"})

@app.route("/healthz")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/analyze", methods=["POST"])
def analyze():
    text = request.form.get("text", "")
    if not text:
        return jsonify({"error": "Text is required"}), 400
    try:
        api_url = os.getenv("TEXT_API_URL", "http://text-processing.com/api/sentiment/")
        timeout = int(os.getenv("EXTERNAL_API_TIMEOUT", 10))
        res = requests.post(api_url, data={"text": text}, timeout=timeout)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
