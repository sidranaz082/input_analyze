from flask import Flask, request, jsonify
from textblob import TextBlob

app = Flask(__name__)

def get_sentiment_label(polarity):
    if polarity > 0.5:
        return "Strongly Positive"
    elif 0 < polarity <= 0.5:
        return "Positive"
    elif polarity == 0:
        return "Neutral"
    elif -0.5 <= polarity < 0:
        return "Negative"
    else:
        return "Strongly Negative"

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()

    if not data or 'texts' not in data:
        return jsonify({"error": "Invalid input. Provide a 'texts' list."}), 400

    texts = data['texts']

    if not isinstance(texts, list):
        return jsonify({"error": "Texts should be a list of strings."}), 400

    results = []

    for text in texts:
        if not isinstance(text, str) or not text.strip():
            results.append({
                "input": text,
                "error": "Invalid input. Please enter a valid string."
            })
            continue

        blob = TextBlob(text)
        polarity = round(blob.sentiment.polarity, 3)
        label = get_sentiment_label(polarity)

        results.append({
            "input": text,
            "polarity": polarity,
            "sentiment": label
        })

    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True)
