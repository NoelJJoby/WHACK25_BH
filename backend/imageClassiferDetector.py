import requests
import json

from transformers import pipeline
from PIL import Image

def detect_AI_image_from_API(file):
    api_user = "82621778"
    api_secret = "Ds33pfj8A62NRJhCjbdJjXey65399EXU"
    params = {
    'models': 'genai',
    'api_user': f'{api_user}',
    'api_secret': f'{api_secret}'
    }
    files = {'media': file}

    r = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)

    output = json.loads(r.text)
    if output["status"] == "success":
        return output["type"]["ai_generated"]   
    
    return -1


# def detect_AI_from_image(image):
    
    
#     detector = pipeline("image-classification", model="haywoodsloan/ai-image-detector-dev-deploy",use_fast=True)
#     results = detector(image)
    

#     top_result = max(results, key=lambda x: x["score"])

#     return top_result["score"]

 

def detect_ai(file):

    scores = {"api":0, "visual":0}

    scores["api"] = detect_AI_image_from_API(file)

    pImage = Image.open(file)
    # scores["visual"] = detect_AI_from_image(pImage)
    return scores["api"]#, scores["visual"]

# file_path = "/mnt/noel/Code_Files/WHACK/WHACK25_BH/images/Untitled.jpg"
# print(detect_ai(file_path))