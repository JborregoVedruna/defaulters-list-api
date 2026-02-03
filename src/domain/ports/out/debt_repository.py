from abc import ABC, abstractmethod
from src.domain.models.debt import Debt
from src.domain.models.pagination import Page, Pageable

class DebtRepository(ABC):
    @abstractmethod
    def save(self, debt: Debt) -> Debt:
        pass

    @abstractmethod
    def find_all(self, pageable: Pageable) -> Page[Debt]:
        pass

    @abstractmethod
    def find_by_debtor_dni(self, debtor_dni: str, pageable: Pageable) -> Page[Debt]:
        pass
