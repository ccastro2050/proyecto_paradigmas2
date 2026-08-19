"""
Modelos Pydantic de la entidad persona — la FRONTERA DE ENTRADA (v2).

El mismo patrón de producto (v1): UN modelo por semántica HTTP.
- Persona           → POST : con su código.
- PersonaReemplazo  → PUT  : reemplazo completo.
- PersonaActualizar → PATCH: parcial, todos los campos opcionales.
"""

from pydantic import BaseModel, Field


class Persona(BaseModel):
    """POST /api/persona — con su código."""

    codigo: str = Field(min_length=1, max_length=10)
    nombre: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=100)
    telefono: str = Field(min_length=1, max_length=20)


class PersonaReemplazo(BaseModel):
    """PUT /api/persona/{codigo} — reemplazo COMPLETO."""

    nombre: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=100)
    telefono: str = Field(min_length=1, max_length=20)


class PersonaActualizar(BaseModel):
    """PATCH /api/persona/{codigo} — parcial: solo se modifican los enviados."""

    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    email: str | None = Field(default=None, min_length=1, max_length=100)
    telefono: str | None = Field(default=None, min_length=1, max_length=20)
