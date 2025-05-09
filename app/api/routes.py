# FastAPI route definitions
from fastapi import APIRouter
from app.schemas.query import QueryRequest
from app.services.query_handler import handle_query

router = APIRouter()

@router.post("/ask")
async def ask(query: QueryRequest):
    """
    Endpoint that receives the user's question and data and answers it with artificial intelligence
    """
    return await handle_query(query.question, query.access_token)