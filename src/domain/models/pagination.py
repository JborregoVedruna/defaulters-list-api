from pydantic import BaseModel
from typing import TypeVar, Generic, List

T = TypeVar('T')

class Page(BaseModel, Generic[T]):
    content: List[T]
    totalElements: int
    totalPages: int
    numberOfElements: int
    size: int
    number: int

class Pageable(BaseModel):
    page: int = 0
    size: int = 10
    sort: str = "uuid"
