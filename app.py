from flask import Flask, render_template, request, abort, redirect, session, url_for
from flask_session import Session 
from util.db_management.db_connection import connect_to_db
from util.misc import generate_code, insert_code
from util.datatypes.user import User

import re, os

app = Flask(__name__)

# heroku config:set APP_KEY=your-secret-key
app_key = os.getenv('APP_KEY') 
app.secret_key = app_key

app.config['SESSION_TYPE'] = 'filesystem'

Session(app)    

links_tbl = connect_to_db("links")
user_tbl = connect_to_db("users")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('index.html', err=None)
    
    if request.method == "POST":

        dis = request.form.get("dis_link")
        roll = request.form.get("user_link")
        random_code = generate_code(5)

        response = insert_code(False, random_code, dis, roll)
        
        if response['success']:
            return render_template('after.html', link_code=response['link_code'])
        return render_template('index.html', err=response['err'])


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
            u = User(username=session['username'])
            if u.is_admin:
                return render_template('register.html', err=None)
        return abort(404)
    if request.method == "POST":
        username = request.form.get("uname")
        passwd = request.form.get("passwd")

        u = User()
        response = u.register(username, passwd)

        if response['success']:
            return redirect(url_for("index"))
        return render_template('register.html', err=response['err'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html', err=None)
    if request.method == "POST":
        username = request.form.get("uname")
        passwd = request.form.get("passwd")

        u = User()
        response = u.login(username, passwd)

        if response['success']:
            session["username"] = u.username
            return redirect(url_for("index"))
        return render_template('login.html', err=response['err'])


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

        response = insert_code(True, custom_url, dis, user_link, session.get('username'))
        if response['success']:
            return render_template('after.html', link_code=response['link_code'])
        return render_template('custom.html', err=response['err'])


@app.route('/links')
def links():
    if session.get("username"):
        u = User(username=session['username'])
        if u.is_admin:
            links = [l for l in links_tbl.find({})]
            return render_template('links.html', links=enumerate(links), links_len=len(links))
    return abort(404)


@app.route('/delete_link')
def del_link():
    if session.get("username"):
        u = User(username=session['username'])
        if u.is_admin:
            _id = int(request.args.get('id'))
            doc = list(links_tbl.find({}))[_id]

            links_tbl.delete_one(doc)

            return redirect(url_for('links'))
    return abort(404)


@app.route('/users')
def users():
    if session.get("username"):
        u = User(username=session['username'])
        if u.is_admin:
            users = [u for u in user_tbl.find({})]
            return render_template('users.html', users=enumerate(users), users_len=len(users))
    return abort(404)


@app.route('/delete_user')
def del_user():
    if session.get("username"):
        u = User(username=session['username'])
        if u.is_admin:
            _id = int(request.args.get('id'))
            doc = list(user_tbl.find({}))[_id]

            user_tbl.delete_one(doc)

            return redirect(url_for('users'))
    return abort(404)


# app.run(host='localhost', port=5000, debug=True)
