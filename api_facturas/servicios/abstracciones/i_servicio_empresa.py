"""
Contrato del servicio de empresa (v2). El controller depende de esta
interfaz. Excepciones de negocio: ValueError → 400 · LookupError → 404.
"""

from typing import Protocol


class IServicioEmpresa(Protocol):
    """Las operaciones de negocio sobre empresa."""

    async def listar(self, limite: int) -> list[dict]:
        """Hasta `limite` filas. ValueError si limite <= 0."""
        ...

    async def obtener(self, codigo: str) -> dict:
        """La empresa con ese codigo. LookupError si no existe."""
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
