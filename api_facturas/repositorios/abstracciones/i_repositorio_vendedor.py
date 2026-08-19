"""
Contrato del repositorio de vendedor (v2) — el mismo Protocol de la v1,
para otra entidad. El servicio depende de ESTA interfaz, nunca de una
clase concreta (inversión de dependencias).
"""

from typing import Protocol


class IRepositorioVendedor(Protocol):
    """Las 5 operaciones de datos de la entidad vendedor."""

    async def obtener_todos(self, limite: int) -> list[dict]:
        """Hasta `limite` filas ordenadas por id."""
        ...

    async def obtener_por_id(self, id_vendedor: int) -> dict | None:
        """El vendedor con ese id, o None si no existe."""
        ...

    async def crear(self, datos: dict) -> bool:
        """Inserta. Devuelve True si quedó insertado."""
        ...

    async def actualizar(self, id_vendedor: int, datos: dict) -> int:
        """Escribe los campos de `datos`. Devuelve filas afectadas."""
        ...

    async def eliminar(self, id_vendedor: int) -> int:
        """Elimina. Devuelve filas eliminadas (0 = no existía)."""
        ...
