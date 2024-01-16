from flask import Flask, render_template, render_template_string, redirect
import os, subprocess

app = Flask(__name__)
execpath = os.path.abspath(__file__).split("app.py")[0]

@app.route("/")
def home():
    return redirect("/1")

@app.route("/1")
def intro():
    return render_template("index.html")

@app.route("/2")
def st2():
    return render_template("st2.html")

@app.route("/3")
def st3():
    return render_template("st3.html")