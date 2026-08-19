"""
Modelos Pydantic de la entidad empresa — la FRONTERA DE ENTRADA (v2).

El mismo patrón de producto (v1): UN modelo por semántica HTTP.
- Empresa           → POST : con su código.
- EmpresaReemplazo  → PUT  : reemplazo completo.
- EmpresaActualizar → PATCH: parcial, todos los campos opcionales.
"""

from pydantic import BaseModel, Field


class Empresa(BaseModel):
    """POST /api/empresa — con su código."""

    codigo: str = Field(min_length=1, max_length=10)
    nombre: str = Field(min_length=1, max_length=100)


class EmpresaReemplazo(BaseModel):
    """PUT /api/empresa/{codigo} — reemplazo COMPLETO."""

    nombre: str = Field(min_length=1, max_length=100)


class EmpresaActualizar(BaseModel):
    """PATCH /api/empresa/{codigo} — parcial: solo se modifican los enviados."""

    nombre: str | None = Field(default=None, min_length=1, max_length=100)
