import os, requests
import datetime

from flask import Flask, redirect, url_for, session, render_template, request
from flask_session import Session
from flask_socketio import SocketIO, emit
from functools import wraps

channels = []
users = []
counter = 0

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# decorater for checking if logged in and redirecting to login if not
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrap

@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', error=e)

@app.errorhandler(405)
def method_not_found(e):
    return render_template('error.html', error=e)

@app.route("/", methods=["GET", "POST"])
def index():
    error = ''
    if request.method == "POST":
        title = request.form.get("title")
        for channel in channels:
            if channel['title'] == title:
                error = "Channel already exists."
                return render_template("index.html", channels=channels, error=error)
        channels.append({'title':title, 'messages':[]})
        return render_template("index.html", channels=channels, new_channel=title)
    else:
        return render_template("index.html", channels=channels)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = ''
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")

        if len(users) == 0:
            error = "username or password incorrect"
            return render_template("login.html", error=error)

        for user in users:
            if user['name'] == name and user['password'] == password:
                break
            error = "username or password incorrect"
            return render_template("login.html", error=error)

        session["user"] = name

        return redirect(url_for('index'))
    else:
        return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = ''
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")

        for user in users:
            if user['name'] == name:
                error = "username already exists."
                return render_template("signup.html", error=error)

        users.append({'name':name, 'password':password})
        session["user"] = name

        return redirect(url_for('index'))
    else:
        return render_template("signup.html")

@app.route("/logout")
@login_required
def logout():
    session.pop('user', None)
    return redirect(url_for("index"))

@app.route("/channel/<title>")
@login_required
def channel(title):
    error = ''
    for channel in channels:
        if channel["title"] == title:
            return render_template("channel.html", channel=channel)
    error = "Channel does not exist."
    return render_template("error.html", error=error)        

@socketio.on("message")
def message(data):
    title = data["title"]
    user = data["user"]
    text = data["text"]
    global counter
    date = datetime.datetime.now()
    timestamp = date.strftime("%c")

    for i, channel in enumerate(channels):
        if channel["title"] == title:
            channels[i]["messages"].append({'id': counter,'user': user,'timestamp': timestamp, 'text': text})
            counter += counter + 1
            text_id = channels[i]['messages'][-1]['id']

    emit("message", {'title': title, 'id': text_id, 'user': user, 'timestamp': timestamp, 'text': text}, broadcast=True)

@socketio.on("delete")
def delete(data):
    title = data["title"]
    text_id = int(data["id"])

    for i, channel in enumerate(channels):
        if channel["title"] == title:
            for message in channel['messages']:
                if message['id'] == text_id:
                    channels[i]["messages"].remove(message)   
                    emit("delete", {'title': title, 'id': text_id}, broadcast=True)
