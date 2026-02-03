from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from uuid import UUID, uuid4
from typing import Annotated

class Debt(BaseModel):
    # Identificador único
    uuid: UUID = Field(default_factory=uuid4)

    debtor_name: str

    # Datos del deudor
    debtor_dni: str = Field(..., min_length=9, max_length=9)

    debt_amount: float = Field(..., gt=0)

    # Detalles financieros
    currency: str = Field(default="EUR", pattern="^[A-Z]{3}$")

    # La fecha desde que se originó la deuda
    debt_since: datetime

    # Ejemplo de lógica de negocio en el dominio:
    @field_validator('debt_since')
    @classmethod
    def date_must_not_be_future(cls, v: datetime) -> datetime:
        if v > datetime.now():
            raise ValueError('La fecha de la deuda no puede ser futura')
        return v

    class Config:
        # Esto permite que el modelo sea inmutable (estilo Hexagonal puro)
        frozen = True