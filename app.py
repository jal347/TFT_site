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

#open file containing redis information
f = open('redis.json', "r")
data = json.load(f)

#connect to the database
r = redis.Redis(host=data["host"], port=data["port"],
                password=data["password"])


#generates leaderboard endpoint api
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

#generates api for a players stats
@app.route('/api/v1/statistics')
@cross_origin()
def api():
    return features.get_player_stats(
        request.args["region"],
        request.args["name"],
        request.args["api_key"]
    )


# renders player html templates. Checks redis database for player information. If player information is not available
# then request the player data using riot api and store it in redis database for a day
@app.route('/player', methods=['POST'])
def player():
    #day in seconds
    day = 86400
    # Use the name + region as the key for the database
    name = request.form['uname'].replace(" ", "").lower()
    region = request.form['region']
    # player info available and call the information from the database (decode the binary string) and remake the dict
    if r.exists(name + region):
        info = r.hgetall(name + region)
        info = {k.decode(): v.decode() for k, v in info.items()}

    else:
        info = features.get_player_stats(
            region,
            name,
            request.form['api_key']
        )
        r.hmset(name + region, info)
        # set the key to expire in a day
        r.expire(name + region, day)
    return render_template('player.html', **info)

# home page. Uses a form to request player data
@app.route('/', methods=['GET', 'POST'])
def form():

    if request.method == 'GET':
        return render_template('home.html')

#generates masters leaderboard
@app.route('/leaderboards')
def masters():
    client = MongoClient()
    collection = client["test1"]["products"]
    docs = list(collection.find())

    def _apply(doc):
        #get id to return as string
        doc["_id"] = str(doc["_id"])
        return doc

    docs = list(map(_apply, docs))

    #sort by rank
    docs = sorted(docs, key=lambda i: int(i['rank']))
    for d in docs:
        del d["_id"]
    return render_template('leaderboards.html', docs=docs)

