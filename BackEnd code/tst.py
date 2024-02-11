from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot_database.db'
db = SQLAlchemy(app)

# Define the database model for chatbot questions and answers
class QA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Initialize the database
db.create_all()

# Load the student dataset from JSON file
with open('student_dataset.json', 'r') as file:
    student_dataset = json.load(file)

# Function to simulate a chatbot answering questions based on the student dataset
def get_chatbot_answer(question):
    # Check if the question is present in the database
    qa_pair = QA.query.filter_by(question=question).first()
    if qa_pair:
        return qa_pair.answer
    else:
        # If the question is not in the database, provide a random answer based on the dataset
        random_record = random.choice(student_dataset)
        return f"On {random_record['date']}, I attended {random_record['lectures_attended']} lectures, completed {random_record['assignments_completed']} assignments, and read {len(random_record['books_read'])} books."

# API endpoint for receiving questions and providing responses
@app.route('/ask', methods=['POST'])
def ask():
    """
    Endpoint to receive questions and provide responses.
    Expects a JSON object with a 'question' key in the request body.
    Returns a JSON response with the corresponding answer.
    """
    data = request.json
    question = data.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    # Get answer from chatbot
    answer = get_chatbot_answer(question)

    # Store the question-answer pair in the database
    qa_pair = QA(question=question, answer=answer)
    db.session.add(qa_pair)
    db.session.commit()

    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
