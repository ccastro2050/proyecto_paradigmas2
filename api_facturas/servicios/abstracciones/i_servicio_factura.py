"""
Contrato del servicio de factura (v2). El controller depende de esta
interfaz. Excepciones de negocio: ValueError → 400 · LookupError → 404 ·
ConflictoError → 409 (ya estaba anulada).
"""

from typing import Protocol


class IServicioFactura(Protocol):
    """Las operaciones de negocio sobre facturas."""

    async def listar(self) -> list[dict]:
        """Todas las facturas, completas (nombres y detalle adentro)."""
        ...

    async def consultar(self, numero: int) -> dict:
        """Una factura completa. ValueError si numero ≤ 0 · LookupError
        si no existe."""
        ...

    async def crear(self, fkidcliente: int, fkidvendedor: int,
                    productos: list[dict]) -> dict:
        """Crea cabecera + renglones. Devuelve el resultado del SP (la
        factura con los números que calculó el trigger)."""
        ...

    async def anular(self, numero: int) -> dict:
        """Borrado lógico. LookupError si no existe · ConflictoError si
        ya estaba anulada."""
        ...
