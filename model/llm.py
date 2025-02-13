from langchain_groq import ChatGroq

llm = ChatGroq(
    # model="llama-3.3-70b-versatile",
    model="qwen-2.5-32b",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)
