# Pydantic schemas for API requests
from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    question: str = Field(..., description="The question to be answered")
    access_token: str = Field(..., description="Token of the use")