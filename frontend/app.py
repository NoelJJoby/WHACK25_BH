
from flask import Flask, render_template, request, jsonify


from backend import imageClassiferDetector#, claimCheckerDEFAULT




app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/image-classifier/")
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



@app.route("/bot-detector/")
def bot_detector(): 
    return render_template("bot-detector.html")

@app.route("/bot-detector/detect-bot", methods=['POST'])
def detect_bot():
    try:
        data = request.get_json()
        username = data.get("username", "").strip()
        followers = data.get("followers", 0)
        following = data.get("following", 0)
        tweets = data.get("tweets", 0)
        likes = data.get("likes", 0)

        if not username:
            return jsonify({"error": "Username is required"}), 400

        # --- Example Heuristic / Mock ML Logic ---
        bot_prob = 0.5

        label = (
            "bot" if bot_prob > 0.65
            else "human" if bot_prob < 0.4
            else "uncertain"
        )

        explanation = (
            f"Follower/following ratio ({followers}:{following}) "
            f"and tweet activity indicate {label} behavior."
        )

        return jsonify({
            "label": label,
            "confidence": round(bot_prob if label == "bot" else 1 - bot_prob, 2),
            "explanation": explanation
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/claim-checker/")
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

        #classification = claimCheckerDEFAULT.claimCheckerMain(tweet_url)
        
        
        classification = "True"
        
        if classification == "True":
            explanation = "The tweet was cross-checked with reputable news sources."
        elif classification == "False":
            explanation =  "The tweet was cross-checked with unreputable news sources"
        elif classification == "Unsupported":
            explanation = "The tweet was unsupported"
        else:
            explanation = "The tweet was unknown and couldn't be verified"
    
 

        return jsonify({
            "classification": classification,
            "explanation": explanation
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/api/data")
def grabImageData():
    return app.send_static_file('data.json')
