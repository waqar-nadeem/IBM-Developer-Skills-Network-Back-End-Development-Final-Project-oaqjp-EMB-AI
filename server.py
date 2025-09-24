"""
Flask server to deploy the Emotion Detection application.
"""

from flask import Flask, request, render_template, jsonify
from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.route('/')
def index():
    """
    Render the index.html page.
    """
    return render_template('index.html')


@app.route('/emotionDetector', methods=['POST'])
def emotion_detect():
    """
    Handle emotion detection POST request.
    Returns JSON of emotion scores and formatted response.
    """
    # Get the text input from the form/JSON
    text_to_analyze = request.form.get('text') if request.form.get('text') else (
        request.json.get('text') if request.is_json and request.json.get('text') else None
    )

    # Run the detector
    result = emotion_detector(text_to_analyze)

    # Handle error case
    if result['dominant_emotion'] is None:
        return jsonify({"formatted_response": "Invalid text! Please try again!"})

    # Build the customer-friendly string response
    formatted_response = (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )

    # Return JSON response
    return jsonify({
        "anger": result['anger'],
        "disgust": result['disgust'],
        "fear": result['fear'],
        "joy": result['joy'],
        "sadness": result['sadness'],
        "dominant_emotion": result['dominant_emotion'],
        "formatted_response": formatted_response
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
