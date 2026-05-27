from pydantic import BaseModel, Field


class TodoItem(BaseModel):
    id: str = Field(..., min_length=1)
    text: str = Field(..., min_length=1, max_length=1000)
    status: str = Field(default="pending")
    user_id: int
    created_at: str


class ShoppingItem(BaseModel):
    id: str = Field(..., min_length=1)
    text: str = Field(..., min_length=1, max_length=1000)
    status: str = Field(default="pending")
    user_id: int
    created_at: str
