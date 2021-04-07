"""Flask Login Example and instagram fallowing find"""

from flask import Flask, url_for, render_template, request, redirect, session
import re
import os
import requests
import json
# import xmltodict
from pprint import pprint
from requests.auth import HTTPBasicAuth

# base_url = "https://192.168.103.97:9060/ers/config/"
# ise_user = "admin"
# ise_password = "1q2w3e4rT"

# headers = {"Content-Type": "application/json",
#     "Accept": "application/json"}
# auth = HTTPBasicAuth(ise_user, ise_password)


# from flask.ext.session import Session

app = Flask(__name__)
app.secret_key = "123"


def initialize_ise(name, passw):
    url = "https://192.168.103.97:9060/ers/config/adminuser/?filter=name.CONTAINS." + name
    headers = {"Content-Type": "application/json",
               "Accept": "application/json"}
    ise_user = name
    ise_password = passw
    auth = HTTPBasicAuth(ise_user, ise_password)
    response = requests.get(url=url, auth=auth, headers=headers, verify=False)
    # if response.text == 200:
    if response.json()['SearchResult']['resources'][0]["name"] == name:
        return("Done")
    else:
        print(f"ERROR: Can't access ISE. Code: {response.status_code}")
        return("ERROR")


@app.route('/', methods=['GET', 'POST'])
def home():
    """ Session control"""
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        print("WOW!!!")
        return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['username']
        passw = request.form['password']
        x = initialize_ise(name, passw)

        if x == "Done":
            print("Thanks")
            session['logged_in'] = True
            return redirect(url_for('app1'))
        else:
            print("Problem1")
            return 'Dont Login'


# @app.route('/register/', methods=['GET', 'POST'])
# def register():
#     """Register Form"""
#     if request.method == 'POST':
#         new_user = User(
#             username=request.form['username'],
#             password=request.form['password'])
#         db.session.add(new_user)
#         db.session.commit()
#         return render_template('login.html')
#     return render_template('register.html')


@app.route('/app1')
def app1():
    if session.get('logged_in'):
        return render_template('app.html')
    else:
        return redirect(url_for('home'))


@app.route("/logout")
def logout():
    """Logout Form"""
    session['logged_in'] = False
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.debug = True
    # db.create_all()
    app.run(host='0.0.0.0')
