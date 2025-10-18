import re
from datetime import datetime

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/image-classifier")
def image_classifier():
    return render_template("image-classifier.html")

@app.route("/image-classifier/detect", methods=["POST"])
def detect_image():
    score = 0
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        #### Run score classification moduels
        ####

        return jsonify({
                "score": score
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/bot-detector")
def bot_detector(): 
    return render_template("bot-detector.html")

@app.route("/claim-checker")
def claim_checker():
    return render_template("claim-checker.html")


@app.route("/api/data")
def grabImageData():
    return app.send_static_file('data.json')
