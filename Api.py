from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import langid
from Singlish2Sinhala import Translate

app = Flask(__name__)

# Load the vectorizer and model during app initialization
Evectorizer = joblib.load('tfidf_vectorizer_english.pkl')
Emodel = joblib.load('Spam_English.pkl')
Svectorizer = joblib.load('tfidf_vectorizer_sinhala.pkl')
Smodel = joblib.load('Spam_Sinhala_Model.pkl')

@app.route('/process_text', methods=['POST'])
def process_text():
    try:
        # Get the text from the request body
        data = request.get_json()
        text_content = data['text']
        print(text_content)

        def detect_language(text):
            language = langid.classify(text)
            return language
        
        text = text_content

        detected_language = detect_language(text)

        if detected_language == 'en':
            print("The text is in English.")
            # Transform the input text using the loaded vectorizer
            input_tfidf = Evectorizer.transform([text_content])

            # Make a prediction
            prediction = Emodel.predict(input_tfidf)
            print(prediction)
            # Interpret the prediction
            if prediction[0] == 0:
                result = "It is Ham"
            else:
                result = "It is Spam"

        elif detected_language == 'si':
            print("The text is in Sinhala.")
            # Transform the input text using the loaded vectorizer
            input_tfidf = Svectorizer.transform([text_content])

            # Make a prediction
            prediction = Smodel.predict(input_tfidf)
            print(prediction)
            # Interpret the prediction
            if prediction[0] == 0:
                result = "It is Ham"
            else:
                result = "It is Spam"

        else:
            
            text_content = Translate(text_content)
            print(text_content)
            # Transform the input text using the loaded vectorizer
            input_tfidf = Svectorizer.transform([text_content])

            # Make a prediction
            prediction = Smodel.predict(input_tfidf)
            print(prediction)
            # Interpret the prediction
            if prediction[0] == 0:
                result = "It is Ham"
            else:
                result = "It is Spam"
        # Return the result as JSON
        return jsonify(result)

    except Exception as e:
        # Log the error
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
