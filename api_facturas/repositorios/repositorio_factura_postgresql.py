"""
Repositorio de factura para PostgreSQL — la API como TRADUCTORA (v2).

Este repositorio no escribe SQL de tablas: llama los PROCEDIMIENTOS
ALMACENADOS que viven en db/init.sql desde el día 1, recibe su resultado
como JSON por el parámetro INOUT p_resultado, y lo entrega como dicts.

Dos detalles del dialecto:
1. En PostgreSQL el CALL devuelve los INOUT como UNA FILA de resultado:
   `first()[0]` es el JSON (el dialecto asyncpg de SQLAlchemy lo entrega
   ya deserializado como dict/list — o como str, según el codec).
2. Los RAISE EXCEPTION de los SPs llegan como DBAPIError con SQLSTATE
   'P0001': aquí (y SOLO aquí) se traducen a excepciones de negocio —
   nadie por encima conoce DBAPIError.
"""

import json

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from excepciones import ConflictoError


class RepositorioFacturaPostgreSQL:
    """Implementación concreta de IRepositorioFactura contra PostgreSQL."""

    def __init__(self, cadena_conexion: str):
        self._cadena_conexion = cadena_conexion
        self._engine: AsyncEngine | None = None

    def _obtener_engine(self) -> AsyncEngine:
        if self._engine is None:
            self._engine = create_async_engine(self._cadena_conexion)
        return self._engine

    # ------------------------------------------------------------------
    # El ayudante central: ejecutar un CALL y devolver su JSON
    # ------------------------------------------------------------------

    @staticmethod
    def _traducir_si_es_negocio(excepcion: DBAPIError) -> None:
        """P0001 (raise_exception) + patrón del mensaje → excepción de negocio."""
        causa = excepcion.orig
        # El asyncpg real puede venir envuelto por el adaptador de SQLAlchemy:
        causa = getattr(causa, "__cause__", None) or causa
        sqlstate = getattr(causa, "sqlstate", None)
        mensaje = getattr(causa, "message", None) or str(causa)
        if sqlstate == "P0001":
            if "no existe" in mensaje:
                raise LookupError(mensaje)          # → 404
            if "anulada" in mensaje:
                raise ConflictoError(mensaje)       # → 409
        # Lo demás (stock insuficiente del trigger, FK, mínimo de
        # renglones) sube tal cual → 500 con el mensaje del motor.

    async def _ejecutar_sp(self, sql_call: str, parametros: dict) -> dict | list | None:
        sql = text(sql_call)
        try:
            # begin() = transacción: los SPs ESCRIBEN (insertar/anular).
            async with self._obtener_engine().begin() as conexion:
                resultado = await conexion.execute(sql, parametros)
                fila = resultado.first()
        except DBAPIError as excepcion:
            self._traducir_si_es_negocio(excepcion)
            raise
        # fila[0] = p_resultado (el INOUT). El dialecto asyncpg de
        # SQLAlchemy ya DESERIALIZA las columnas json (llegan como
        # dict/list); si llegara como texto, se abre aquí:
        if fila is None or fila[0] is None:
            return None
        valor = fila[0]
        return json.loads(valor) if isinstance(valor, str) else valor

    # ------------------------------------------------------------------
    # Los 4 métodos del contrato
    # ------------------------------------------------------------------

    async def listar(self) -> list[dict]:
        resultado = await self._ejecutar_sp(
            "CALL sp_listar_facturas_y_productosporfactura(NULL)", {})
        return resultado or []

    async def consultar(self, numero: int) -> dict:
        resultado = await self._ejecutar_sp(
            "CALL sp_consultar_factura_y_productosporfactura(:numero, NULL)",
            {"numero": numero})
        # El SP responde {"factura": {…}, "productos": […]}; se aplana a la
        # MISMA forma de las facturas del listado (productos adentro):
        factura = resultado["factura"]
        factura["productos"] = resultado["productos"] or []
        return factura

    async def crear(self, fkidcliente: int, fkidvendedor: int,
                    productos_json: str) -> dict:
        # El detalle viaja como JSON y el SP lo abre — un solo viaje a la
        # BD, UNA transacción (la lección ACID). El cast(:productos as
        # json) tipa el texto para el parámetro JSON del SP:
        return await self._ejecutar_sp(
            "CALL sp_insertar_factura_y_productosporfactura("
            ":cliente, :vendedor, cast(:productos as json), 1, NULL)",
            {"cliente": fkidcliente, "vendedor": fkidvendedor,
             "productos": productos_json})

    async def anular(self, numero: int) -> dict:
        return await self._ejecutar_sp(
            "CALL sp_anular_factura(:numero, NULL)", {"numero": numero})
