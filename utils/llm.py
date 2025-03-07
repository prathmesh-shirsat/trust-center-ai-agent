import os
from langchain_openai import ChatOpenAI

llmInstance = ChatOpenAI(
    model='gpt-4o',
    temperature=0.0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)
