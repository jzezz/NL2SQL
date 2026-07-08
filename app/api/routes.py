from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()


class QueryRequest(BaseModel):
    question: str


@router.post("/chat")
async def chat(request: QueryRequest):
    from app.services.nl2sql_service import process_question
    return await process_question(request.question)
