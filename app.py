from flask import Flask, render_template, request
import re
from textblob import TextBlob

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    sentiment = None
    polarity = 0
    subjectivity = 0
    text = ""
    positive = 0
    negative = 0
    neutral = 0
    confidence = 0
    words = 0
    characters = 0
    sentence_analysis = []
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    total_sentences = 0
    insight = ""

    if request.method == "POST":
        text = request.form["text_input"]
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        subjectivity = analysis.sentiment.subjectivity
        words = len(text.split())
        characters = len(text)

        # Sentiment

        # Overall Sentiment

        if polarity > 0:
            sentiment = "Positive"
        elif polarity < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        # Sentence-wise Analysis

        sentences = re.split(r'(?<=[.!?])\s+', text.strip())

        for s in sentences:
            if s.strip():
                blob = TextBlob(s)
                p = blob.sentiment.polarity
                total_sentences += 1
                if p > 0:
                    label = "Positive"
                    emoji = "😊"
                    color = "#22C55E"
                    positive_count += 1
                elif p < 0:
                    label = "Negative"
                    emoji = "😡"
                    color = "#EF4444"
                    negative_count += 1
                else:
                    label = "Neutral"
                    emoji = "😐"
                    color = "#FACC15"
                    neutral_count += 1

                sentence_analysis.append({
                    "sentence": s,
                    "label": label,
                    "emoji": emoji,
                    "color": color,
                    "score": round(p, 2)
                })

        # Percentages based on sentence count
        if total_sentences > 0:
            positive = round((positive_count / total_sentences) * 100)
            negative = round((negative_count / total_sentences) * 100)
            neutral = round((neutral_count / total_sentences) * 100)
        else:
            positive = 0
            negative = 0
            neutral = 0

        # Sentiment Strength

        confidence = round(abs(polarity) * 100)

        # AI Insight
        if sentiment == "Positive":
            insight = f"The text contains {positive_count} positive sentence(s), {negative_count} negative sentence(s), and {neutral_count} neutral sentence(s). Overall tone is positive."
        elif sentiment == "Negative":
            insight = f"The text contains {negative_count} negative sentence(s), {positive_count} positive sentence(s), and {neutral_count} neutral sentence(s). Overall tone is negative."
        else:
            insight = f"The text contains a balanced emotional tone with {neutral_count} neutral sentence(s)."
    return render_template(

        "index.html",
        sentiment=sentiment,
        polarity=round(polarity, 2),
        subjectivity=round(subjectivity, 2),
        confidence=confidence,
        positive=positive,
        negative=negative,
        neutral=neutral,
        words=words,
        characters=characters,
        insight=insight,
        text=text,
        sentence_analysis=sentence_analysis,
        positive_count=positive_count,
        negative_count=negative_count,
        neutral_count=neutral_count,
        total_sentences=total_sentences
    )


if __name__ == "__main__":
    app.run(debug=True)
