import requests

API_KEY = "AIzaSyDgELmawO8uyMVHoIrObCc3jwOIQHg0Aa0"
BASE_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

def fact_check(query, max_results=5):
    params = {
        "query": query,
        "key": API_KEY,
        "languageCode": "en",
        "pageSize": max_results
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()  # Raises error if something goes wrong

    data = response.json()
    return data.get("claims", [])

# Example usage
results = fact_check("vaccines cause autism")

for claim in results:
    #text = claim.get("text")
    #claimant = claim.get("claimant")
    review = claim["claimReview"][0]
    #publisher = review["publisher"]["name"]
    rating = review["textualRating"]

    print(f"Claim: {text}")
    print(f"Claimant: {claimant}")
    print(f"Source: {publisher}")
    print(f"Rating: {rating}")
    #print(f"URL: {review['url']}")
    print("-" * 60)
