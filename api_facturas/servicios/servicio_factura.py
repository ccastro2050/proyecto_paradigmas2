"""
Servicio de factura — la capa de NEGOCIO (v2).

El más delgado de los servicios, A PROPÓSITO: las reglas duras de la
factura (mínimo de renglones, stock, totales) viven en la BD y la forma
la validó Pydantic. Aquí queda lo poco que es negocio de la API: sanear
argumentos y empacar el detalle como JSON para el SP.
"""

import json

from repositorios.abstracciones.i_repositorio_factura import IRepositorioFactura


class ServicioFactura:
    """Reglas de negocio de factura (delegación consciente)."""

    def __init__(self, repositorio: IRepositorioFactura):
        self._repositorio = repositorio

    @staticmethod
    def _validar_numero(numero: int) -> int:
        if numero <= 0:
            raise ValueError("El número de factura debe ser mayor que cero.")
        return numero

    async def listar(self) -> list[dict]:
        return await self._repositorio.listar()

    async def consultar(self, numero: int) -> dict:
        numero = self._validar_numero(numero)
        return await self._repositorio.consultar(numero)

    async def crear(self, fkidcliente: int, fkidvendedor: int,
                    productos: list[dict]) -> dict:
        # El detalle viaja al SP como JSON (un solo viaje, una transacción):
        productos_json = json.dumps(productos)
        return await self._repositorio.crear(fkidcliente, fkidvendedor,
                                             productos_json)

    async def anular(self, numero: int) -> dict:
        numero = self._validar_numero(numero)
        return await self._repositorio.anular(numero)
