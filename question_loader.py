import json
import random

def load_questions(file_path):

    with open(file_path, "r") as f:
        questions = json.load(f)

    return random.sample(questions, 10)