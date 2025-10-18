from factverifai import fact_check
import os

os.environ["OPENAI_API_KEY"] = "sk-your-key-here"
os.environ["FACTVERIFAI_MODEL"] = "openai/gpt-4o-mini"

def aiFactChecker(inStatement):
    # Directly use the fact_check function provided by the library
    #result = fact_check(inStatement, exa="565999a9-b8ce-4d4d-a42d-e926538b2f5d")
    result = fact_check(
        inStatement,
        exa="565999a9-b8ce-4d4d-a42d-e926538b2f5d"
    )
    print(result)
    return result

uncheckedStatement = input("Enter a statement to fact check: ")
print(aiFactChecker(uncheckedStatement))

from factverifai import fact_check


def aiFactChecker(claim):
    # Directly use the fact_check function provided by the library
    result = fact_check(claim)
    return result

# Example usage
uncheckedStatement = "The Eiffel Tower is the tallest structure in Paris."
print(aiFactChecker(uncheckedStatement))