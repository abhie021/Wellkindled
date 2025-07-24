import json
import random
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for intent in knowledge_base["intents"]:
        if question in intent["patterns"]:
            responses = intent["responses"]
            return random.choice(responses) 

def chat_bot():
    knowledge_base: dict = load_knowledge_base('database.json') 
    while True:
        user_input: str = input("You: ")

        if user_input.lower() == 'quit':
            break

        best_match: str | None = find_best_match(user_input, [pattern for intent in knowledge_base["intents"] for pattern in intent["patterns"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base["intents"].append({
                    "patterns": [user_input],
                    "responses": [new_answer],
                    "context": [""]
                })
                save_knowledge_base('database.json', knowledge_base) 
                print('Bot: Thank you! I learned a new response')

if __name__ == '__main__':
    chat_bot()
