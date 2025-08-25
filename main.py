from flask import Flask, request, jsonify
from textblob import TextBlob

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "AI App is running!"})

@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    if request.method == "GET":
        text = request.args.get("text")
        if not text:
            return jsonify({"error": "Text input is required"}), 400
    else:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "Text input is required"}), 400
        text = data["text"]

    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity

    result = {
        "input": text,
        "sentiment": "positive" if sentiment > 0 else "negative" if sentiment < 0 else "neutral",
        "score": round(sentiment, 3)
    }
    return jsonify(result)
