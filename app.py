from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from sample import get_sentence
from datetime import datetime
import random
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/tweet_coll')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
tweet_coll = db.tweet_coll

app = Flask(__name__)

@app.route('/')
def index():
    sentence = get_sentence(random.randint(1,20))
    return render_template('index.html', sentence=sentence)

@app.route('/<sentence>')
def save_tweet(sentence):
    """saves a given phrase as a tweet in a db and tweets it out"""
    tweet = {
        'tweet_content': sentence,
        'created_at': datetime.now(),
    }
    tweet_id = tweet_coll.insert_one(tweet).inserted_id

    # ADD PIECE THAT TWEETS IT OUT

    sentence = get_sentence(random.randint(1,20))
    return redirect(url_for('index', sentence=sentence))

@app.route('/view_favorites/<tweet_id>/delete', methods=['POST'])
def delete_tweet(tweet_id):
    """Delete one tweet."""
    tweet_coll.delete_one({'_id': ObjectId(tweet_id)})
    return redirect(url_for('view_favorites'))

@app.route('/view_favorites')
def view_favorites():
    return render_template('view_favorites.html', tweets=tweet_coll.find().sort([('created_at', -1)]))

@app.route('/description')
def description():
    return render_template('description.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
