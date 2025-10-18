#from factverifai import fact_check
#import os
#from langchain_community.llms import Ollama

#os.environ["OPENAI_API_KEY"] = "sk-your-key-here"
#os.environ["FACTVERIFAI_MODEL"] = "openai/gpt-4o-mini"

#def aiFactChecker(inStatement):
    # Directly use the fact_check function provided by the library
    #result = fact_check(inStatement, exa="565999a9-b8ce-4d4d-a42d-e926538b2f5d")
    #result = fact_check(
        #inStatement,
        #exa="565999a9-b8ce-4d4d-a42d-e926538b2f5d"
    #)
    #print(result)
    #return result

#uncheckedStatement = input("Enter a statement to fact check: ")
#print(aiFactChecker(uncheckedStatement))

#from factverifai import fact_check


#def aiFactChecker(claim):
    # Directly use the fact_check function provided by the library
    #result = fact_check(claim)
    ##return result

# Example usage
#llm = Ollama(model="mistral")
#response = llm.invoke("Explain how solar panels generate electricity.")
##print(response)
#uncheckedStatement = "The Eiffel Tower is the tallest structure in Paris."
#print(aiFactChecker(uncheckedStatement))


#Imports
from factverifai import fact_check
from langchain_community.llms import Ollama
from twitterFetcher import tweetFetcher


# Using model to fact-check tweet.
class LocalLLM:
    def __init__(self, model="llama2"):
        self.llm = Ollama(model="llama2")
    def invoke(self, prompt):
        return self.llm.invoke(prompt)

from factverifai import core
core.llm = LocalLLM(model="llama2")  # <-- Replace "mistral" with the model you have

def aiFactChecker(inStatement):
    result = core.llm.invoke(f"Fact check the following statement and only send either True, False or Unsupported as a response (be harsh and label obviously false statements as false, and label obviously true statements as true; research for evidence to suggest either argument) {inStatement}")
    return result

#uncheckedStatement = input("Enter a statement to fact check: ")
#testUrl = "https://x.com/GrahamSmith_/status/1979466306580607447"
testUrl = input("Enter a twitter URL: ")
uncheckedStatement = tweetFetcher(testUrl)
print(uncheckedStatement)
factResponse = aiFactChecker(uncheckedStatement)
if ("true" in factResponse.lower()) and (("not true") not in factResponse.lower()):
    factResponse = "True"
elif ("false" in factResponse.lower()):
    factResponse = "False"
elif "unsupported" in factResponse.lower():
    factResponse = "Unsupported"
else:
    factResponse = "Unknown"
print(factResponse)