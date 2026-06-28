import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load .env file
load_dotenv()

# Create Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)

# Ask a simple question
response = llm.invoke("What is Artificial Intelligence?")

print("\nGemini Response:\n")
print(response.content)