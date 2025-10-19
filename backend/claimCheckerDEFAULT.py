# from factverifai import fact_check
# import os
# from langchain_community.llms import Ollama

# os.environ["OPENAI_API_KEY"] =
# os.environ["FACTVERIFAI_MODEL"] = "openai/gpt-4o-mini"
from langchain_community.llms import Ollama
from factverifai import fact_check, core
from .twitterFetcher import tweetFetcher
import re

# def aiFactChecker(inStatement):
# Directly use the fact_check function provided by the library
# result = fact_check(inStatement, exa="565999a9-b8ce-4d4d-a42d-e926538b2f5d")
# result = fact_check(
# inStatement,
# exa="565999a9-b8ce-4d4d-a42d-e926538b2f5d"
# )
# print(result)
# return result

# uncheckedStatement = input("Enter a statement to fact check: ")
# print(aiFactChecker(uncheckedStatement))

# from factverifai import fact_check


# def aiFactChecker(claim):
# Directly use the fact_check function provided by the library
# result = fact_check(claim)
##return result

# Example usage
# llm = Ollama(model="mistral")
# response = llm.invoke("Explain how solar panels generate electricity.")
##print(response)
# uncheckedStatement = "The Eiffel Tower is the tallest structure in Paris."
# print(aiFactChecker(uncheckedStatement))


# Using model to fact-check tweet.
class LocalLLM:

    def __init__(self, model="llama2", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.llm = Ollama(model=model, base_url=base_url)

    def invoke(self, prompt):
        return self.llm.invoke(prompt)


core = type("Core", (), {})()
core.llm = LocalLLM()


def aiFactChecker(inStatement):
    prompt = f"""Fact check the following statement and only send either True, False or Unsupported as a response (be harsh and label obviously false statements as false, \\
        and label obviously true statements as true; research for evidence to suggest either argument) {inStatement}"""

    return core.llm.invoke(prompt)


# uncheckedStatement = input("Enter a statement to fact check: ")
# testUrl = "https://x.com/GrahamSmith_/status/1979466306580607447"


# testUrl = input("Enter a twitter URL: ")
def claimCheckerMain(testUrl):
    # Imports

    # testUrl = ""
    uncheckedStatement = tweetFetcher(testUrl)
    # print(uncheckedStatement)
    factResponse = aiFactChecker(uncheckedStatement)
    
    match = re.search(r"\b(true|false|unsupported)\b", factResponse, re.IGNORECASE)
    return match.group(1).capitalize() if match else "Unknown" , factResponse


# print(claimCheckerMain(testUrl))
