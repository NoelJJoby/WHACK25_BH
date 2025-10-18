import re
from datetime import datetime

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, Flask!"


@app.route("/hello/")
@app.route("/hello/<name>")

def hello_there(name = None):
    return render_template(
        "template.html",
        name=name,
        date=datetime.now()
    )

@app.route("/api/data")
def grabImageData():
    return app.send_static_file('data.json')
