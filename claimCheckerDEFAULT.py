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



from factverifai import fact_check
from langchain_community.llms import Ollama

# Use your downloaded model (example: "mistral" or "llama3")
class LocalLLM:
    def __init__(self, model="llama2"):
        self.llm = Ollama(model="llama2")
    def invoke(self, prompt):
        return self.llm.invoke(prompt)

from factverifai import core
core.llm = LocalLLM(model="llama2")  # <-- Replace "mistral" with the model you have

def aiFactChecker(inStatement):
    result = fact_check(
        inStatement,
        exa="565999a9-b8ce-4d4d-a42d-e926538b2f5d"  # skip EXA API (or None)
    )
    return result

uncheckedStatement = input("Enter a statement to fact check: ")
print(aiFactChecker(uncheckedStatement))