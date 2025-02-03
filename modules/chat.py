from fastapi.responses import StreamingResponse
from schema.chat_request import ChatRequest
from graph.app_graph import app_graph
from fastapi import APIRouter, status
from groq import AsyncGroq
from io import StringIO
import asyncio
import time

chat_router = APIRouter(prefix='/chat', tags=['Chats'])

@chat_router.post("/completion", status_code=status.HTTP_200_OK, name="Simple chat")
async def simple_chat(request: ChatRequest):
    client = AsyncGroq()
    stream = await client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Your name is Mr.Beast very helpful assistant"
            },
            {
                "role": "user",
                "content": request.input_text
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=request.temperature if request.temperature is not None else 0.5,
        max_completion_tokens=request.max_tokens if request.max_tokens is not None else 1024,
        top_p=1,
        stop=None,
        stream=True,
    )

    async def event_generator():
        async for chunk in stream:
            token = chunk.choices[0].delta.content
            if token:
                yield token 
                await asyncio.sleep(0.01)
                # for digit in token:
                #     yield digit 
                #     await asyncio.sleep(0.01)

    return StreamingResponse(event_generator(), media_type="text/plain")

@chat_router.post("/rag-chat", status_code=status.HTTP_200_OK, name="Chat with rag")
async def chat_with_rag(request: ChatRequest):
    inputs = {"question": request.input_text}

    # Create an async generator for streaming
    async def generate():
        # Using your app_graph.stream to generate response in chunks
        async for chunk in app_graph.astream(inputs, stream_mode="updates"):  # Assuming astream is async
            if 'retrieve' in chunk:
                for document in chunk['retrieve']["documents"]:
                    content = document.page_content
                    # Yield document content immediately when it's retrieved
                    yield """<details>\n<summary>Retrieved Document</summary>"""
                    yield f"{content}"
                    yield "\n</details>"
                    await asyncio.sleep(1)

            if 'grade_documents' in chunk:
                for document in chunk['grade_documents']["documents"]:
                    content = document.page_content
                    # Yield document content immediately when it's retrieved
                    yield """<details>\n<summary>Match Document</summary>"""
                    yield f"{content}"
                    yield "\n</details>"
                    await asyncio.sleep(1)

            if 'generate' in chunk:
                generated_content = chunk['generate']['generation']
                # Yield generated content immediately
                # yield f"Generated Response: {generated_content}\n\n"
                yield "\n\n**Result:**\n"
                for token in generated_content:  # Assuming each token is space-separated
                    yield token
                    await asyncio.sleep(0.01)  # Simulate delay between tokens

    # Return the StreamingResponse that will yield the content
    return StreamingResponse(generate(), media_type="text/plain")
