"""
Modelos Pydantic de la entidad vendedor — la FRONTERA DE ENTRADA (v2).

El mismo patrón de producto (v1): UN modelo por semántica HTTP.
- Vendedor           → POST : el id lo asigna la BD (SERIAL).
- VendedorReemplazo  → PUT  : reemplazo completo.
- VendedorActualizar → PATCH: parcial, todos los campos opcionales.
"""

from pydantic import BaseModel, Field


class Vendedor(BaseModel):
    """POST /api/vendedor — el id lo asigna la BD (SERIAL)."""

    carnet: int = Field(ge=0)
    direccion: str = Field(min_length=1, max_length=100)
    fkcodpersona: str = Field(min_length=1, max_length=10)


class VendedorReemplazo(BaseModel):
    """PUT /api/vendedor/{id_vendedor} — reemplazo COMPLETO."""

    carnet: int = Field(ge=0)
    direccion: str = Field(min_length=1, max_length=100)
    fkcodpersona: str = Field(min_length=1, max_length=10)


class VendedorActualizar(BaseModel):
    """PATCH /api/vendedor/{id_vendedor} — parcial: solo se modifican los enviados."""

    carnet: int | None = Field(default=None, ge=0)
    direccion: str | None = Field(default=None, min_length=1, max_length=100)
    fkcodpersona: str | None = Field(default=None, min_length=1, max_length=10)
