"""
Contrato del servicio de persona (v2). El controller depende de esta
interfaz. Excepciones de negocio: ValueError → 400 · LookupError → 404.
"""

from typing import Protocol


class IServicioPersona(Protocol):
    """Las operaciones de negocio sobre persona."""

    async def listar(self, limite: int) -> list[dict]:
        """Hasta `limite` filas. ValueError si limite <= 0."""
        ...

    async def obtener(self, codigo: str) -> dict:
        """La persona con ese codigo. LookupError si no existe."""
        ...

    async def crear(self, datos: dict) -> None:
        """Crea (los datos ya vienen validados por Pydantic)."""
        ...

    async def actualizar(self, codigo: str, datos: dict) -> int:
        """Escribe los campos enviados. ValueError si no llegó ninguno ·
        LookupError si no existe · devuelve filas afectadas."""
        ...

    async def eliminar(self, codigo: str) -> int:
        """Elimina. LookupError si no existe · devuelve filas eliminadas."""
        ...
