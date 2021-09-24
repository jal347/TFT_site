from flask import Flask, request, url_for, render_template, redirect
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import features

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = "*"


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


@app.route('/player')
def player():
    info = features.get_player_stats(
        request.args['region'],
        request.args['name'],
        request.args['api_key']
    )

    return render_template('player.html', **info)


@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['uname']
        region = request.form['region']
        api_key = request.form['api_key']
        return redirect(url_for('player', name=name, region=region, api_key=api_key))
    if request.method == 'GET':
        return render_template('home.html')


