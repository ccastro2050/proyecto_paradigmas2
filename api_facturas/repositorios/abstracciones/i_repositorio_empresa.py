"""
Contrato del repositorio de empresa (v2) — el mismo Protocol de la v1,
para otra entidad. El servicio depende de ESTA interfaz, nunca de una
clase concreta (inversión de dependencias).
"""

from typing import Protocol


class IRepositorioEmpresa(Protocol):
    """Las 5 operaciones de datos de la entidad empresa."""

    async def obtener_todos(self, limite: int) -> list[dict]:
        """Hasta `limite` filas ordenadas por codigo."""
        ...

    async def obtener_por_codigo(self, codigo: str) -> dict | None:
        """La empresa con ese codigo, o None si no existe."""
        ...

    async def crear(self, datos: dict) -> bool:
        """Inserta. Devuelve True si quedó insertada."""
        ...

    async def actualizar(self, codigo: str, datos: dict) -> int:
        """Escribe los campos de `datos`. Devuelve filas afectadas."""
        ...

    async def eliminar(self, codigo: str) -> int:
        """Elimina. Devuelve filas eliminadas (0 = no existía)."""
        ...
