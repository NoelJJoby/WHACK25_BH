import requests
import json

from PIL import Image, ExifTags #type:ignore

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





current_file_path = "/mnt/noel/Code_Files/WHACK/WHACK25_BH/AIGenerationCheck/images/Untitled.jpg"

scores = {"api":0,"provenance":0, "visual":0}



#scores["api"] = detect_AI_image_from_API(current_file_path)

