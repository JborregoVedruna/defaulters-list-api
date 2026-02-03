from pydantic import BaseModel
from src.domain.models.debt import Debt
from src.domain.ports.out.debt_repository import DebtRepository

class SaveDebtCommand(BaseModel):
    debt: Debt

class SaveDebtHandler:
    def __init__(self, repository: DebtRepository):
        self._repository = repository

    def __call__(self, command: SaveDebtCommand) -> Debt:
        return self._repository.save(command.debt)
