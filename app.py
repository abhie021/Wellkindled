from flask import Flask, render_template, request, jsonify
from chatbot import find_best_match, get_answer_for_question, load_knowledge_base

app = Flask(__name__)

knowledge_base = load_knowledge_base('database.json')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('message')
    best_match = find_best_match(user_input, [pattern for intent in knowledge_base["intents"] for pattern in intent["patterns"]])

    if best_match:
        answer = get_answer_for_question(best_match, knowledge_base)
    else:
        answer = "I'm sorry, I don't know the answer to that yet."

    return jsonify({'response': answer})

if __name__ == '__main__':
    app.run(debug=True)
