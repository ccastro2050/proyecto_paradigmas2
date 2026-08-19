"""
Modelos Pydantic de la entidad cliente — la FRONTERA DE ENTRADA (v2).

El mismo patrón de producto (v1): UN modelo por semántica HTTP.
- Cliente           → POST : el id lo asigna la BD (SERIAL).
- ClienteReemplazo  → PUT  : reemplazo completo.
- ClienteActualizar → PATCH: parcial, todos los campos opcionales.
"""

from decimal import Decimal

from pydantic import BaseModel, Field


class Cliente(BaseModel):
    """POST /api/cliente — el id lo asigna la BD (SERIAL).
    (`credito` y `fkcodempresa` son OPCIONALES: el default de credito
    lo pone la BD y la empresa puede quedar en NULL — research D6.)
    """

    fkcodpersona: str = Field(min_length=1, max_length=10)
    credito: Decimal | None = Field(default=None, ge=0)
    fkcodempresa: str | None = Field(default=None, min_length=1, max_length=10)


class ClienteReemplazo(BaseModel):
    """PUT /api/cliente/{id_cliente} — reemplazo COMPLETO."""

    credito: Decimal = Field(ge=0)
    fkcodpersona: str = Field(min_length=1, max_length=10)
    fkcodempresa: str | None = Field(default=None, min_length=1, max_length=10)


class ClienteActualizar(BaseModel):
    """PATCH /api/cliente/{id_cliente} — parcial: solo se modifican los enviados."""

    credito: Decimal | None = Field(default=None, ge=0)
    fkcodpersona: str | None = Field(default=None, min_length=1, max_length=10)
    fkcodempresa: str | None = Field(default=None, min_length=1, max_length=10)
