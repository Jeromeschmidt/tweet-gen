from flask import Flask, render_template, request, redirect, url_for
from sample import get_sentence

app = Flask(__name__)

@app.route('/')
def index():
    sentence = get_sentence(10)
    return render_template('index.html', sentence=sentence)
