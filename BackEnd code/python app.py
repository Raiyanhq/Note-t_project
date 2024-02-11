from flask import Flask, request, jsonify, render_template
import requests
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
import json

app = Flask(__name__)

# Initialize data storage
qa_pairs = []

# Load existing data if available
try:
    with open('data.json', 'r') as file:
        data = json.load(file)
        qa_pairs = data['qa_pairs']
except FileNotFoundError:
    pass

# Function to update the model with new question-answer pairs
def update_model(X, y):
    model = Sequential()
    model.add(Dense(64, input_dim=X.shape[1], activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(y.shape[1], activation='softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(X, y, epochs=10, batch_size=32)

    return model

# Function to preprocess text data
def preprocess_text(text):
    # Implement text preprocessing steps here
    return text

# Function to vectorize questions
def vectorize_questions(questions):
    # Implement vectorization method here, e.g., TF-IDF or word embeddings
    return np.random.rand(len(questions), 100)  # Dummy implementation

# Function to vectorize answers
def vectorize_answers(answers):
    # Implement vectorization method here, e.g., one-hot encoding
    return np.random.rand(len(answers), 10)  # Dummy implementation

# Function to get answer from specified API
def get_answer_from_api(question, api_endpoint):
    response = requests.get(api_endpoint, params={'question': question})
    if response.status_code == 200:
        return response.json().get('answer')
    else:
        return None

# API endpoint for receiving new question-answer pairs
@app.route('/')
def welcome():
    return render_template('index.html')

def update():
    data = request.json
    question = preprocess_text(data['question'])
    answer = preprocess_text(data['answer'])

    qa_pairs.append({'question': question, 'answer': answer})
    X = vectorize_questions([pair['question'] for pair in qa_pairs])
    y = vectorize_answers([pair['answer'] for pair in qa_pairs])

    model = update_model(X, y)

    # Save updated model and data
    model.save('model.h5')
    with open('data.json', 'w') as file:
        json.dump({'qa_pairs': qa_pairs}, file)

    response = {'status': 'success'}
    return jsonify(response)

# API endpoint for receiving questions and providing responses
@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = preprocess_text(data['question'])

    # Load model
    model = Sequential()
    model = model.load_weights('model.h5')

    # Vectorize question
    X_question = vectorize_questions([question])

    # Get predicted answer
    predicted_answer = model.predict(X_question)

    response = {'answer': predicted_answer}
    return jsonify(response)

# API endpoint for answering questions from the web
@app.route('/answer', methods=['GET'])
def answer():
    question = request.args.get('question')
    api_endpoint = request.args.get('api')
    if not question or not api_endpoint:
        return jsonify({'error': 'No question or API endpoint provided'}), 400

    # Get answer from specified API
    api_answer = get_answer_from_api(question, api_endpoint)
    if api_answer:
        response = {'answer': api_answer}
    else:
        response = {'answer': 'Sorry, I couldn\'t find an answer for that question.'}

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)



