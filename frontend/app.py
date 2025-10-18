import re
from datetime import datetime

from flask import Flask, render_template, request, jsonify


from backend import imageClassiferDetector




app = Flask(__name__)

@app.route("/")
def index():
    return render_template("template.html")

@app.route("/index")
def home():
    return render_template("index.html")
 

@app.route("/image-classifier")
def image_classifier():
    return render_template("image-classifier.html")

@app.route("/image-classifier/detect", methods=["POST"])
def detect_image():
    score = "HELLO" 
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        #### Run score classification moduels
        ####
        api_score, local_score = imageClassiferDetector.detect_ai(request.files["file"])


        return jsonify({
                "average_score": round((api_score + local_score) / 2 *100, 3),
                "api_score": api_score,
                "local_score": local_score
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
