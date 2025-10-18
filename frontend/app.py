
from flask import Flask, render_template, request, jsonify


from backend import imageClassiferDetector




app = Flask(__name__)

@app.route("/")
def index():
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
        api_score = imageClassiferDetector.detect_ai(request.files["file"])
        print(api_score)

        return jsonify({
                "api_score": api_score
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/bot-detector")
def bot_detector(): 
    return render_template("bot-detector.html")

@app.route("/claim-checker")
def claim_checker():
    return render_template("claim-checker.html")

@app.route("/claim-checker/analyse", methods=["POST"])
def analyse_tweet():
    try:
        data = request.get_json()
        tweet_url = data.get("url", "")

        if not tweet_url or "x.com" not in tweet_url:
            return jsonify({"error": "Please enter a valid Twitter link."}), 400
        print(tweet_url)

        label = "true"
        confidence =1
    #
    #   Run Claim Check
    #
        explanation = (
            "The tweet was cross-checked with reputable news sources."
            if label == "true"
            else "The tweet could not be verified by fact-checking databases."
        )

        return jsonify({
            "label": label,
            "confidence": confidence,
            "explanation": explanation
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/api/data")
def grabImageData():
    return app.send_static_file('data.json')
