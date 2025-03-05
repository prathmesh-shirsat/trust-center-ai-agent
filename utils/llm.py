from langchain_openai import ChatOpenAI

llmInstance = ChatOpenAI(
    model='gpt-4o',
    temperature=0.0,
    timeout=90
)
