"""
Contrato del servicio de vendedor (v2). El controller depende de esta
interfaz. Excepciones de negocio: ValueError → 400 · LookupError → 404.
"""

from typing import Protocol


class IServicioVendedor(Protocol):
    """Las operaciones de negocio sobre vendedor."""

    async def listar(self, limite: int) -> list[dict]:
        """Hasta `limite` filas. ValueError si limite <= 0."""
        ...

    async def obtener(self, id_vendedor: int) -> dict:
        """El vendedor con ese id. LookupError si no existe."""
        ...

    async def crear(self, datos: dict) -> None:
        """Crea (los datos ya vienen validados por Pydantic)."""
        ...

    async def actualizar(self, id_vendedor: int, datos: dict) -> int:
        """Escribe los campos enviados. ValueError si no llegó ninguno ·
        LookupError si no existe · devuelve filas afectadas."""
        ...

    async def eliminar(self, id_vendedor: int) -> int:
        """Elimina. LookupError si no existe · devuelve filas eliminadas."""
        ...
