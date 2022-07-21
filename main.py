from flask import Flask

from flask import request, render_template, redirect, url_for
from werkzeug.exceptions import HTTPException

import tweepy
import os
from random import choice
from ast import literal_eval


app = Flask(__name__)

CONSUMER_KEY = "gnb9IOOZTSXpFE5F8hR8z1Wrz"
CONSUMER_SECRET = "darQbZ7mpZXtFsjzSQX7JEmUzIfnOQv3QaSymW7WKkZaBupwjZ"

ACCESS_TOKEN = "1549848476049350657-j6BPeuZY7lul8x0c16xqqIGziq1FOM"
ACCESS_TOKEN_SECRET = "yBKplNr0klaJ4BDfPlAHBuVtXJPSxn2f8tjNJjSbYKVBh"

RESPONSES = [
    "water thaagu", "water thaagava?", "drink water", 
    "manchi neellu thaagu", "manchi neellu thaagava",
    "edavataniki kantlo neellu vundali kadha konchem water thaagu",
    "go and drink water",
]
SALUTATIONS = ["bro", "vro", "mowa", "mawa", "friend", "da", "ra"]


root = os.path.join(os.path.dirname(os.path.abspath(__file__)))
media_path = root+"/static/"
media_list = os.listdir(media_path)

tweep_error= {'code': None, 'message':None}


@app.route("/", methods=["GET", "POST"])
def home():
    global tweep_error
    tweep_error = {'code': None, 'message':None}

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    if request.method == "POST":
        username = request.form.get("username")
        print(username)

        if username[0] != '@':
            username = '@'+username
        try:
            media = api.media_upload(filename=root+'/static/'+choice(media_list))
            api.update_status(" ".join([username+",", choice(RESPONSES), choice(SALUTATIONS)]).capitalize(), media_ids=[media.media_id_string])
        except tweepy.TweepError as e:
            tweep_error = literal_eval(e.reason.strip(']['))
            if tweep_error['code']==187:
                tweep_error['message']="Someone has already tagged the person! Please try after sometime."
            return redirect(url_for("oops"))

        return redirect(url_for("home"))
    else:
        return render_template("index.html")

@app.route("/oops")
def oops():
    return render_template("error.html", code=tweep_error['code'], description=tweep_error['message'])

@app.errorhandler(HTTPException)
def handle_exception(e):
    data = {
        "code": e.code,
        "name": e.name,
        "description": e.description,
    }
    return render_template("error.html", code=data["code"], description=data["description"])


if __name__ == "__main__":
    app.run(debug=True)
