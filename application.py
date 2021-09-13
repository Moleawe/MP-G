import os

from flask import Flask, flash, redirect, render_template, request, session
from flask import *
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from qr import generateqr
from string import *
import random

# Configure application
app = Flask(__name__)
app.secret_key = '12345'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def index():
    session["number"] = random.randrange(1, 1000)
    return render_template("index.html")


@app.route("/QR_Code_Generator")
def qrcode():
    return render_template("qrcode.html")


@app.route("/converted", methods=["POST"])
def convert():
    global text
    text = request.form['text']
    return render_template('converted.html')


@app.route("/download")
def download():
    generateqr(text)
    filename = text + '.png'
    return send_file(filename, as_attachment=True)


@app.route("/random", methods=["GET", "POST"])
def rnumber():
    random_number = random.randint(1, 1000)
    return render_template("random.html", random_number=random_number)


@app.route("/password")
def password():
    characters = ascii_letters + digits
    pass_random = random.SystemRandom()
    password = "".join(pass_random.choice(characters) for i in range(12))
    gPassword = str(password)
    return render_template('password.html', gPassword=gPassword)


@app.route("/guess", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        if int(request.form['guess']) == session["number"]:
            answer = "Correct!"
            return render_template("guess.html", answer=answer)
        elif int(request.form['guess']) < session['number']:
            answer = "Too Low."
            return render_template("guess.html", answer=answer)
        else:
            answer = "Too High."
            return render_template("guess.html", answer=answer)
    else:
        return render_template("guess.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()


for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
