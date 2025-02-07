import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, status

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_ENV_KEY")

from modules.chat import chat_router
from modules.vector_database import vector_database_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(vector_database_router)

@app.get("/", status_code=status.HTTP_200_OK)
async def check_health():
    return {
        "code": status.HTTP_200_OK,
        "message": "Check success"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5005)