from pymongo import MongoClient
from src.domain.models.debt import Debt
from src.domain.models.pagination import Page, Pageable
from src.domain.ports.out.debt_repository import DebtRepository

import math

class MongoDebtRepository(DebtRepository):
    def __init__(self, client: MongoClient, db_name: str):
        self._collection = client[db_name]["debts"]

    def save(self, debt: Debt) -> Debt:
        debt_data = debt.model_dump()
        # Ensure uuid is string for Mongo if not already (pydantic handles UUID to str usually)
        debt_data["uuid"] = str(debt_data["uuid"])
        
        self._collection.update_one(
            {"uuid": debt_data["uuid"]},
            {"$set": debt_data},
            upsert=True
        )
        return debt

    def find_all(self, pageable: Pageable) -> Page[Debt]:
        return self._find_paginated({}, pageable)

    def find_by_debtor_dni(self, debtor_dni: str, pageable: Pageable) -> Page[Debt]:
        return self._find_paginated({"debtor_dni": debtor_dni}, pageable)

    def _find_paginated(self, filter_query: dict, pageable: Pageable) -> Page[Debt]:
        skip = pageable.page * pageable.size
        limit = pageable.size
        
        # Simple sorting implementation
        sort_dir = 1
        sort_field = pageable.sort
        if sort_field.startswith("-"):
            sort_dir = -1
            sort_field = sort_field[1:]
        
        if filter_query:
            cursor = self._collection.find(filter_query).sort(sort_field, sort_dir).skip(skip).limit(limit)
        else:
            cursor = self._collection.find().sort(sort_field, sort_dir).skip(skip).limit(limit)
        
        content = [Debt(**doc) for doc in cursor]
        total_elements = self._collection.count_documents(filter_query)
        total_pages = math.ceil(total_elements / pageable.size) if pageable.size > 0 else 0
        
        return Page(
            content=content,
            totalElements=total_elements,
            totalPages=total_pages,
            numberOfElements=len(content),
            size=pageable.size,
            number=pageable.page
        )
