#Import required libaries
import requests
import math
import nltk
from difflib import SequenceMatcher
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from transformers import pipeline

#Key Constants
API_KEY = "AIzaSyDgELmawO8uyMVHoIrObCc3jwOIQHg0Aa0"
BASE_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
Key = "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"

#from ai_summarizer import summarize_text
#from openai import OpenAI
#client = OpenAI(api_key="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")

#from googleapiclient.discovery import build
import time

#def fact_check_query(query):
    #service = build("factchecktools", "v1alpha1", developerKey=API_KEY)
    ##cleaned = clean_query(query)
    #cleaned = query
    #response = service.claims().search(query=cleaned, languageCode="en").execute()
    #if 'claims' in response:
        #return response['claims']
    
    # Try shorter keyword version
    #short_query = ' '.join(cleaned.split()[:3])
    #time.sleep(0.3)
    #response = service.claims().search(query=short_query, languageCode="en").execute()
    #return response.get('claims', [])




summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_to_length(text, maxLen):
    summary = summarizer(text, max_length=maxLen, min_length=1, do_sample=False)[0]['summary_text']
    if len(summary) > maxLen:
        summary = summary[:maxLen].rsplit(' ', 1)[0] + '...'
    return summary

#Uses Google Fact Check API to check statement based on keywords
def fact_check(query, max_results=10):
    params = {
        "query": query,
        "key": API_KEY,
        "languageCode": "en",
        "pageSize": max_results
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()  # Raises error if something goes wrong

    claims = response.json().get("claims", [])

    data = response.json()
    #return data.get("claims", [])

    # Re-rank sources by textual similarity to query
    ranked = sorted(
        claims,
        key=lambda c: SequenceMatcher(None, query.lower(), c.get("text", "").lower()).ratio(),
        reverse=True
    )
    return ranked

#Input and pass tweet statement (Main Program)
def googleFactCheckerMain(inStatement):
    global falseCount
    falseCount = 0
    global unprovenCount
    unprovenCount = 0
    global truthCount 
    truthCount = 0

    #inStatement = input("Enter a test Twitter statement.")
    #print(summarize_to_length(inStatement, 100))

    summary_length = 50
    model = "gpt-3.5-turbo"
    if len(inStatement) > 50:
        inStatement = summarize_to_length(inStatement, 50)

    #print(inStatement)

    global tokens 
    tokens = word_tokenize(inStatement)
    global keywords 
    keywords = [word for word in tokens if word.lower() not in stopwords.words('english') and word.isalnum()]
    #print(keywords)
    global keywordString 
    keywordString = ""
    for each in keywords:
        keywordString = keywordString + " " + each
    #print(keywordString)
    global results

    results = fact_check(keywordString)

    #Organises data returned from Google Fact Check API
    for claim in results:
        text = claim.get("text")
        claimant = claim.get("claimant")
        review = claim["claimReview"][0]
        publisher = review["publisher"]["name"]
        rating = review["textualRating"]
        totalKeywordCount = len(keywords)
        #relevanceValue = 0
        #for each in keywords:
            #each = each.lower()
            #if each in text.lower():
                #relevanceValue +=1
        #if relevanceValue >= totalKeywordCount/2:
            #ClaimText = (f"Claim: {text}")
            #ClaimantText = (f"Claimant: {claimant}")
            #SourceText = (f"Source: {publisher}")
            #RatingText = (f"Rating: {rating}")
            #URLText = (f"URL: {review['url']}")
            #print(ClaimText, "\n", ClaimantText, "\n", SourceText, "\n", RatingText, "\n", URLText)
            #print(rating)
        if ("false" in rating.lower()) or ("misleading" in rating.lower()) or ("fake" in rating.lower()):
            falseCount +=1
        elif ("unsupported" in rating.lower()) or ("unproven" in rating.lower()):
            unprovenCount +=1
        elif ("true" in rating.lower()):
            truthCount +=1

    if (falseCount + unprovenCount + truthCount) == 0:
        #print("No Relevant Sources found.")
        results = "None"
    else:
        #print("Number of sources found:")
        #print("According to ", math.trunc((falseCount/(falseCount+unprovenCount+truthCount))*100),
               #"% of sources, this tweet's information is false." )
        falsePercentage = math.trunc((falseCount/(falseCount+unprovenCount+truthCount))*100)
        #print("According to ", math.trunc((truthCount/(falseCount+unprovenCount+truthCount))*100), 
              #"% of sources, this tweet's information is true." )
        truthPercentage = math.trunc((truthCount/(falseCount+unprovenCount+truthCount))*100)
       # print("According to ", math.trunc((unprovenCount/(falseCount+unprovenCount+truthCount))*100),
               #"% of sources, this tweet's information is unproven to be true or false." )
        unprovenPercentage = math.trunc((unprovenCount/(falseCount+unprovenCount+truthCount))*100)
        displaySourcesBool = input("See sources? (Y/N) \n")
        if displaySourcesBool == "Y":
            for claim in results:
                text = claim.get("text")
                claimant = claim.get("claimant")
                review = claim["claimReview"][0]
                publisher = review["publisher"]["name"]
                rating = review["textualRating"]
                totalKeywordCount = len(keywords)

                #print(f"Claim: {text}")
                #print(f"Claimant: {claimant}")
                #print(f"Source: {publisher}")
                #print(f"Rating: {rating}")
                #print(f"URL: {review['url']}")
                #print( "-" * 60, "\n")
    return results, falseCount, unprovenCount, truthCount #remove prints


uncheckedStatement = input("Enter a statement to fact check: ")
print(googleFactCheckerMain(uncheckedStatement))




#IGNORE - backup code
# Download stopwords (only needed once)
#nltk.download('punkt')  
#nltk.download('punkt_tab')
#nltk.download('stopwords')

#text = "Python is a powerful programming language for data analysis and machine learning"

# Tokenize and remove stopwords
##tokens = word_tokenize(text)
#keywords = [word for word in tokens if word.lower() not in stopwords.words('english') and word.isalnum()]

#print(keywords)