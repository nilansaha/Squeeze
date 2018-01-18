from flask import Flask, render_template, request, redirect, session, url_for
from pymongo import MongoClient
import random
import string


app = Flask(__name__)

client = MongoClient('localhost:27017')
db = client.shortener
collection = db.urls

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/<urlId>')
def find(urlId):
    count = collection.find({"id" : urlId}).count()
    if count==0:
        return render_template('notfound.html')
    else:
        cursor = collection.find_one({"id" : urlId})
        print cursor['longUrl']
        return redirect(cursor['longUrl'], code=302)


@app.route("/shorturl", methods=['POST'])
def makeShortUrl():
    shortUrl = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(7))
    longUrl = request.form['url']
    collection.insert({'id':shortUrl,'longUrl':longUrl})
    return render_template('shortedurl.html', shortUrl = request.url_root + shortUrl, longUrl = longUrl )

if __name__ == '__main__':
    app.run(port=8080)
