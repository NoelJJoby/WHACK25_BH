import requests
import json

from transformers import pipeline
from PIL import Image

def detect_AI_image_from_API(file_path):
    api_user = "82621778"
    api_secret = "Ds33pfj8A62NRJhCjbdJjXey65399EXU"
    params = {
    'models': 'genai',
    'api_user': f'{api_user}',
    'api_secret': f'{api_secret}'
    }
    files = {'media': open(file_path, 'rb')}

    r = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)

    output = json.loads(r.text)
    if output["status"] == "success":
        return output["type"]["ai_generated"]   
    
    return -1


def detect_AI_from_image(file_path):
    
    detector = pipeline("image-classification", model="Ateeqq/ai-vs-human-image-detector", use_fast=True)
    image = Image.open(file_path)
    results = detector(image)
    

    top_result = max(results, key=lambda x: x["score"])

    return top_result["score"]



def detect_ai(file_path):
    scores = {"api":0, "visual":0}
    scores["api"] = detect_AI_image_from_API(file_path)
    scores["visual"] = detect_AI_from_image(file_path)
    print(scores)

file_path = "/mnt/noel/Code_Files/WHACK/WHACK25_BH/AIGenerationCheck/images/FirstTest.jpg"
detect_ai(file_path)