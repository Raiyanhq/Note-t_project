from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/answer', methods=['GET'])
def answer():
    question = request.args.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    # Call your function to get the answer
    # Example:
    # api_answer = get_answer_from_api(question)

    # Return the answer as a JSON response
    return jsonify({'answer': 'This is the answer to your question.'})

if __name__ == '__main__':
    app.run(debug=True)
