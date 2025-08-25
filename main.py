from flask import Flask, request, jsonify
import os, requests

app = Flask(__name__)

TEXT_API_URL = os.getenv("TEXT_API_URL", "http://text-processing.com/api/sentiment/")
API_TIMEOUT = int(os.getenv("EXTERNAL_API_TIMEOUT", "10"))

@app.get("/")
def root():
    return jsonify({"message": "AI App is running!"}), 200

@app.get("/healthz")
def healthz():
    return "ok", 200

@app.post("/analyze")
def analyze():
    # Accepts JSON: {"text": "..."} or form-encoded "text=..."
    text = None
    if request.is_json:
        body = request.get_json(silent=True) or {}
        text = body.get("text")
    if not text:
        text = request.form.get("text")

    if not text:
        return jsonify({"error": "Missing 'text'"}), 400

    try:
        # text-processing.com expects form-encoded body
        resp = requests.post(
            TEXT_API_URL,
            data={"text": text},
            timeout=API_TIMEOUT,
        )
        resp.raise_for_status()
        # Response example: {"label": "pos", "probability": {...}}
        data = resp.json()
        label_map = {"pos": "positive", "neg": "negative", "neutral": "neutral"}
        label = label_map.get(data.get("label"), data.get("label"))
        return jsonify({"text": text, "sentiment": label, "raw": data}), 200
    except requests.exceptions.Timeout:
        return jsonify({"error": "Upstream timeout"}), 504
    except Exception as e:
        return jsonify({"error": f"Upstream failure: {str(e)}"}), 502

if __name__ == "__main__":
    # for local testing only; in k8s we use gunicorn
    app.run(host="0.0.0.0", port=8000)
