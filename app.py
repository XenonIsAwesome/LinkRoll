from flask import Flask, render_template, request, abort, redirect, session, url_for
from flask_session import Session 
from util.db_management.db_connection import connect_to_db
from util.misc import generate_code
from util.datatypes.user import User

import re

app = Flask(__name__)

app.secret_key = 'add-yours'
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)    

links_tbl = connect_to_db("links")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('index.html')
    
    if request.method == "POST":

        dis = request.form.get("dis_link")
        if not dis:
            dis = "https://xeshort.herokuapp.com/"

        roll = request.form.get("user_link")
        if not roll:
            roll = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

        exp = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"

        if not (re.match(exp, dis) and re.match(exp, roll)):
            return render_template('index.html')
        
        doc = links_tbl.find_one({
            'discord_link': dis,
            'user_link': roll
        })

        if doc:
            return render_template('after.html', link_code=doc["link_code"]) 

        random_code = generate_code(5)

        links_tbl.insert_one(
            {
                'link_code': random_code,
                'discord_link': dis,
                'user_link': roll
            }
        )
        
        return render_template('after.html', link_code=random_code)


@app.route('/<link_code>')
def router(link_code):
    doc = links_tbl.find_one({'link_code': link_code})
    if not doc: abort(404)
    if 'discord' in request.headers.get('User-Agent').lower():
        return redirect(doc["discord_link"])
    else:
        return redirect(doc["user_link"])


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        if session.get("username"):
            if session["username"] == "xenon":
                return render_template('register.html', err=None)
        return abort(404)
    if request.method == "POST":
        username = request.form.get("uname")
        passwd = request.form.get("passwd")

        u = User()
        success = u.register(username, passwd)

        if success:
            session["username"] = u.username
            return redirect(url_for("index"))
        return render_template('register.html', err="Couldn't register.")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html', err=None)
    if request.method == "POST":
        username = request.form.get("uname")
        passwd = request.form.get("passwd")

        u = User()
        success = u.login(username, passwd)

        if success:
            session["username"] = u.username
            return redirect(url_for("index"))
        return render_template('login.html', err="Couldn't login.")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route('/custom', methods=['GET', 'POST'])
def custom():
    if request.method == "GET":
        if not session.get("username"):
            return abort(404)
        return render_template("custom.html", err=None)
    if request.method == "POST":
        custom_url = request.form.get("url")
        user_link = request.form.get("user_link")
        dis = request.form.get("dis_link") or user_link

        exists = links_tbl.find_one({'link_code': custom_url})
        if exists:
            return render_template('custom.html', err="Link already exists.")

        links_tbl.insert_one({
            'link_code': custom_url,
            'discord_link': dis,
            'user_link': user_link
        })

        return render_template('after.html', link_code=custom_url)


# app.run(host='0.0.0.0', port=5000)
