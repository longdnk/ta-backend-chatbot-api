from fastapi import APIRouter, status
from helper.init import init_knowledge_base
from schema.response import ResponseMessage

vector_database_router = APIRouter(prefix="/knowledge-base", tags=["Knowledge Base"])

@vector_database_router.get("/init", status_code=status.HTTP_200_OK, name="Initialize the knowledge base")
async def init():
    try:
        init_knowledge_base()
        return ResponseMessage(
            code=status.HTTP_200_OK,
            message="Reload knowledge base success"
        )
    except Exception as e:
        return ResponseMessage(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"Error from server {str(e)}"
        )