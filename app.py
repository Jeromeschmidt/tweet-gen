from flask import Flask
from sample import get_sentence

app = Flask(__name__)

@app.route('/')
def hello_world():
    sentence = get_sentence(10)
    return sentence
