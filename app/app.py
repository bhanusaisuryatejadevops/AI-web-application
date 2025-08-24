import os
import time
from flask import Flask, request, jsonify
import requests
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Metrics
REQUEST_COUNT = Counter("app_requests_total", "Total HTTP requests", ["endpoint", "method", "http_status"])
REQUEST_LATENCY = Histogram("app_request_latency_seconds", "Latency of requests in seconds", ["endpoint"])
INFERENCE_LATENCY = Histogram("app_inference_latency_seconds", "Latency of external AI inference in seconds")
INFERENCE_ERRORS = Counter("app_inference_errors_total", "Total errors from external AI inference")

# Config
HUGGINGFACE_API_URL = os.getenv("HUGGINGFACE_API_URL", "https://api-inference.huggingface.co/models/facebook/bart-large-cnn")
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN", "")
TIMEOUT_SEC = float(os.getenv("EXTERNAL_API_TIMEOUT", "20.0"))

@app.route("/healthz", methods=["GET"])
def health():
    REQUEST_COUNT.labels("/healthz", "GET", 200).inc()
    return jsonify({"status": "ok"}), 200

@app.route("/predict", methods=["POST"])
def predict():
    start = time.time()
    try:
        data = request.get_json(force=True) or {}
        text = data.get("text", "")
        task = data.get("task", "summarization")  # summarization / sentiment-analysis

        if not text:
            REQUEST_COUNT.labels("/predict", "POST", 400).inc()
            return jsonify({"error": "Missing 'text'"}), 400

        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"} if HUGGINGFACE_API_TOKEN else {}
        payload = {"inputs": text}
        url = HUGGINGFACE_API_URL

        ext_start = time.time()
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT_SEC)
            ext_elapsed = time.time() - ext_start
            INFERENCE_LATENCY.observe(ext_elapsed)
        except Exception as e:
            INFERENCE_ERRORS.inc()
            REQUEST_COUNT.labels("/predict", "POST", 502).inc()
            return jsonify({"error": "Upstream AI service error", "details": str(e)}), 502

        if resp.status_code >= 400:
            INFERENCE_ERRORS.inc()
            REQUEST_COUNT.labels("/predict", "POST", resp.status_code).inc()
            return jsonify({"error": "AI service failed", "status_code": resp.status_code, "body": resp.text}), 502

        result = resp.json()
        elapsed = time.time() - start
        REQUEST_LATENCY.labels("/predict").observe(elapsed)
        REQUEST_COUNT.labels("/predict", "POST", 200).inc()
        return jsonify({"result": result, "elapsed_seconds": elapsed}), 200

    except Exception as e:
        REQUEST_COUNT.labels("/predict", "POST", 500).inc()
        return jsonify({"error": "Server error", "details": str(e)}), 500

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    # For local testing only; use gunicorn in containers
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
