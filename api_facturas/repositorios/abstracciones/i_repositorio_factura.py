"""
Contrato del repositorio de factura (v2) — la abstracción de la entidad
maestro-detalle. Quien lo implementa decide CÓMO hablar con la BD (los
SPs, en el caso PostgreSQL); quien lo usa recibe dicts listos.

Errores de negocio que el implementador debe traducir:
LookupError (la factura no existe) · ConflictoError (ya está anulada).
"""

from typing import Protocol


class IRepositorioFactura(Protocol):
    """Las 4 operaciones de datos de factura."""

    async def listar(self) -> list[dict]:
        """Todas las facturas con nombres resueltos y detalle adentro."""
        ...

    async def consultar(self, numero: int) -> dict:
        """Una factura igual de completa. LookupError si no existe."""
        ...

    async def crear(self, fkidcliente: int, fkidvendedor: int,
                    productos_json: str) -> dict:
        """Cabecera + renglones en UNA transacción de la BD.

        Devuelve {"factura": {…}, "productos": […]} con los números que
        CALCULÓ el trigger.
        """
        ...

    async def anular(self, numero: int) -> dict:
        """Borrado lógico: estado='anulada' + stock restaurado.

        LookupError si no existe · ConflictoError si ya estaba anulada.
        """
        ...
