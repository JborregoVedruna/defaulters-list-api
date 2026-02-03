from pydantic import BaseModel
from src.domain.models.pagination import Page, Pageable
from src.domain.models.debt import Debt
from src.domain.ports.out.debt_repository import DebtRepository

class GetDebtsQuery(BaseModel):
    pageable: Pageable

class GetDebtsHandler:
    def __init__(self, repository: DebtRepository):
        self._repository = repository

    def __call__(self, query: GetDebtsQuery) -> Page[Debt]:
        return self._repository.find_all(query.pageable)
