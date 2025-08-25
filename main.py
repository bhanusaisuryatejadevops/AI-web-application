from flask import Flask, request, jsonify, render_template_string
import requests
import os

app = Flask(__name__)

TEXT_API_URL = os.getenv("TEXT_API_URL", "http://text-processing.com/api/sentiment/")
TIMEOUT = int(os.getenv("EXTERNAL_API_TIMEOUT", 10))

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
        response = requests.post(TEXT_API_URL, data={"text": text}, timeout=TIMEOUT)
        if response.status_code == 200:
            result = response.json()
            sentiment = max(result["probability"], key=result["probability"].get)
            score = result["probability"][sentiment]
            return jsonify({"input": text, "sentiment": sentiment, "score": score})
        else:
            return jsonify({"error": "AI API error", "status": response.status_code}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/ui", methods=["GET", "POST"])
def ui():
    if request.method == "POST":
        text = request.form.get("text")
        if text:
            response = requests.post(TEXT_API_URL, data={"text": text}, timeout=TIMEOUT)
            if response.status_code == 200:
                result = response.json()
                sentiment = max(result["probability"], key=result["probability"].get)
                score = result["probability"][sentiment]
                return render_template_string(HTML_TEMPLATE, result=f"Sentiment: {sentiment}, Score: {score}")
            else:
                return render_template_string(HTML_TEMPLATE, result="Error from AI API")
        else:
            return render_template_string(HTML_TEMPLATE, result="Please enter text.")
    return render_template_string(HTML_TEMPLATE, result="")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Sentiment Analyzer</title>
</head>
<body>
    <h2>Enter Text for Sentiment Analysis</h2>
    <form method="POST">
        <textarea name="text" rows="4" cols="50" placeholder="Type something..."></textarea><br><br>
        <button type="submit">Analyze</button>
    </form>
    <h3>{{ result }}</h3>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
