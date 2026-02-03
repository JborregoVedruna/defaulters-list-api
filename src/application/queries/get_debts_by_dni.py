from pydantic import BaseModel
from src.domain.models.pagination import Page, Pageable
from src.domain.models.debt import Debt
from src.domain.ports.out.debt_repository import DebtRepository

class GetDebtsByDniQuery(BaseModel):
    debtor_dni: str
    pageable: Pageable

class GetDebtsByDniHandler:
    def __init__(self, repository: DebtRepository):
        self._repository = repository

    def __call__(self, query: GetDebtsByDniQuery) -> Page[Debt]:
        return self._repository.find_by_debtor_dni(query.debtor_dni, query.pageable)
