"""
Servicio de cliente — la capa de NEGOCIO (v2). CALCADO del de producto:
recibe la interfaz del repositorio por constructor y comunica los
problemas con excepciones de negocio (ValueError → 400 · LookupError → 404).
"""

from repositorios.abstracciones.i_repositorio_cliente import IRepositorioCliente


class ServicioCliente:
    """Reglas de negocio del CRUD de cliente."""

    def __init__(self, repositorio: IRepositorioCliente):
        self._repositorio = repositorio

    @staticmethod
    def _validar_id(id_cliente: int) -> int:
        if id_cliente <= 0:
            raise ValueError("El id debe ser un entero mayor que cero.")
        return id_cliente

    async def listar(self, limite: int) -> list[dict]:
        if limite <= 0:
            raise ValueError("El límite debe ser un entero mayor que cero.")
        return await self._repositorio.obtener_todos(limite)

    async def obtener(self, id_cliente: int) -> dict:
        id_cliente = self._validar_id(id_cliente)
        fila = await self._repositorio.obtener_por_id(id_cliente)
        if fila is None:
            raise LookupError(f"No existe un cliente con id = {id_cliente}")
        return fila

    async def crear(self, datos: dict) -> None:
        await self._repositorio.crear(datos)

    async def actualizar(self, id_cliente: int, datos: dict) -> int:
        id_cliente = self._validar_id(id_cliente)
        if not datos:
            raise ValueError("No se envió ningún campo para actualizar.")
        filas_afectadas = await self._repositorio.actualizar(id_cliente, datos)
        if filas_afectadas == 0:
            raise LookupError(f"No existe un cliente con id = {id_cliente}")
        return filas_afectadas

    async def eliminar(self, id_cliente: int) -> int:
        id_cliente = self._validar_id(id_cliente)
        filas_eliminadas = await self._repositorio.eliminar(id_cliente)
        if filas_eliminadas == 0:
            raise LookupError(f"No existe un cliente con id = {id_cliente}")
        return filas_eliminadas
