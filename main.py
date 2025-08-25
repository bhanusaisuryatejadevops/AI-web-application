from flask import Flask, request, jsonify
from textblob import TextBlob

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "AI App is running!"})

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Text input is required"}), 400

    text = data["text"]
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity  # value between -1 (negative) and 1 (positive)

    result = {
        "input": text,
        "sentiment": "positive" if sentiment > 0 else "negative" if sentiment < 0 else "neutral",
        "score": sentiment
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
