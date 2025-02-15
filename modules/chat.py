from fastapi.responses import StreamingResponse
from schema.chat_request import ChatRequest
from graph.app_graph import app_graph
from fastapi import APIRouter, status
from groq import AsyncGroq
from io import StringIO
import asyncio
import time

chat_router = APIRouter(prefix="/chats", tags=["Chats"])


@chat_router.post("/completion", status_code=status.HTTP_200_OK, name="Simple chat")
async def simple_chat(request: ChatRequest):
    client = AsyncGroq()
    stream = await client.chat.completions.create(
        messages=request.conservation,
        model=(
            request.model_name
            if request.model_name is not None
            else "llama-3.3-70b-versatile"
        ),
        temperature=request.temperature if request.temperature is not None else 0.5,
        max_completion_tokens=(
            request.max_tokens if request.max_tokens is not None else 1024
        ),
        top_p=1,
        stop=None,
        stream=True,
    )

    async def event_generator():
        async for chunk in stream:
            token = chunk.choices[0].delta.content
            if token:
                for digit in token:
                    yield digit
                    await asyncio.sleep(0.002)
            # if token:
            #     yield token
            #     await asyncio.sleep(0.01)

    return StreamingResponse(event_generator(), media_type="text/plain")


@chat_router.post("/rag-chat", status_code=status.HTTP_200_OK, name="Chat with rag")
async def chat_with_rag(request: ChatRequest):
    inputs = {"question": request.conservation[-1]["content"]}

    # Create an async generator for streaming
    async def generate():
        # Using your app_graph.stream to generate response in chunks
        async for chunk in app_graph.astream(
            inputs, stream_mode="updates"
        ):  # Assuming astream is async
            print("chunk1: ", chunk)
            if "retrieve" in chunk:
                yield f"""<blockquote style="margin-bottom: 24px;padding: 10px;border: 2px solid;border-color: #4229fb;border-radius: 6px;">
                        <strong>Retrieve Document: </strong>
                        """
                for index, document in enumerate(chunk["retrieve"]["documents"]):
                    content = document.page_content
                    # Yield document content immediately when it's retrieved
                    yield f"""<details open style="
                                    font-weight: 500;
                                    margin-bottom: 12px;
                                ">
                                <summary>Document {index+1}</summary>
                                <p style="padding-left: 20px;">{content}</p>
                        </details>"""
                    await asyncio.sleep(0.5)
                yield f"""</blockquote>"""

            if "grade_documents" in chunk:
                yield f"""<blockquote style="margin-bottom: 24px;padding: 10px;border: 2px solid;border-color: #4229fb;border-radius: 6px;">
                        <strong>Grade Document: </strong>
                        """
                for index, document_object in enumerate(chunk["grade_documents"]["documents"]):
                    document = document_object['document']
                    grade = document_object['grade']
                    # Set title and text color based on grade
                    if grade.lower() == "no":
                        title = "Irrelevant"
                        color = "red"
                    elif grade.lower() == "yes":
                        title = "Relevant"
                        color = "green"
                    else:
                        title = "Unknown"  # Fallback for other values
                        color = "gray"  # Default color
                    content = document.page_content
                    # Yield document content immediately when it's retrieved
                    yield f"""<details open style="
                                    font-weight: 500;
                                    margin-bottom: 12px;
                                    color: {color};
                                ">
                                <summary>Document {index+1} -- {title}</summary>
                                <p style="padding-left: 20px;">{content}</p>
                        </details>"""
                    await asyncio.sleep(0.5)
                yield f"""</blockquote>"""

            if "generate" in chunk:
                generated_content = chunk["generate"]["generation"]
                # Yield generated content immediately
                # yield f"\n**Generated Response**: {content}\n"
                yield f"""<blockquote style="margin-bottom: 24px;padding: 10px;border: 2px solid;border-color: #4229fb;border-radius: 6px;">
                        <strong>Generate Response: </strong>
                        <p style="padding-left: 20px; font-weight: 500;">{generated_content}</p>
                    </blockquote>"""
                await asyncio.sleep(0.5)

    # Return the StreamingResponse that will yield the content
    return StreamingResponse(generate(), media_type="text/plain")
