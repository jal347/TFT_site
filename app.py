from flask import Flask, request, url_for, render_template, redirect
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import features
import redis
import logging
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = "*"

f = open('redis.json', "r")
data = json.load(f)
r = redis.Redis(host=data["host"], port=data["port"],
                password=data["password"])


@app.route('/api/v1/leaderboard')
@cross_origin()
def leaderboard():

    client = MongoClient()
    collection = client["test1"]["products"]
    docs = list(collection.find())

    def _apply(doc):
        doc["_id"] = str(doc["_id"])
        return doc

    docs = list(map(_apply, docs))
    return {"results": docs}


@app.route('/api/v1/statistics')
@cross_origin()
def api():
    return features.get_player_stats(
        request.args["region"],
        request.args["name"],
        request.args["api_key"]
    )


@app.route('/player', methods=['POST'])
def player():

    name = request.form['uname'].replace(" ", "").lower()
    if r.exists(name):
        info = r.hgetall(name)
        info = {k.decode(): v.decode() for k, v in info.items()}

    else:
        info = features.get_player_stats(
            request.form['region'],
            name,
            request.form['api_key']
        )
        r.hmset(name, info)
    logging.error(info)
    return render_template('player.html', **info)


@app.route('/', methods=['GET', 'POST'])
def form():
    # if request.method == 'POST':
    #     # "Whipped Yesman" is the same as "whippedyesman" in this game
    #     name = request.form['uname'].replace(" ", "").lower()
    #     region = request.form['region']
    #     api_key = request.form['api_key']
    #     return redirect(url_for('player', name=name, region=region, api_key=api_key))
    if request.method == 'GET':
        return render_template('home.html')

@app.route('/leaderboards')
def masters():
    client = MongoClient()
    collection = client["test1"]["products"]
    docs = list(collection.find())

    def _apply(doc):
        doc["_id"] = str(doc["_id"])
        return doc

    docs = list(map(_apply, docs))
    docs = sorted(docs, key=lambda i: int(i['rank']))
    for d in docs:
        del d["_id"]
    return render_template('leaderboards.html', docs=docs)

