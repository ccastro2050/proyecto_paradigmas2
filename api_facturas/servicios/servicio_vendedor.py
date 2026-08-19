"""
Servicio de vendedor — la capa de NEGOCIO (v2). CALCADO del de producto:
recibe la interfaz del repositorio por constructor y comunica los
problemas con excepciones de negocio (ValueError → 400 · LookupError → 404).
"""

from repositorios.abstracciones.i_repositorio_vendedor import IRepositorioVendedor


class ServicioVendedor:
    """Reglas de negocio del CRUD de vendedor."""

    def __init__(self, repositorio: IRepositorioVendedor):
        self._repositorio = repositorio

    @staticmethod
    def _validar_id(id_vendedor: int) -> int:
        if id_vendedor <= 0:
            raise ValueError("El id debe ser un entero mayor que cero.")
        return id_vendedor

    async def listar(self, limite: int) -> list[dict]:
        if limite <= 0:
            raise ValueError("El límite debe ser un entero mayor que cero.")
        return await self._repositorio.obtener_todos(limite)

    async def obtener(self, id_vendedor: int) -> dict:
        id_vendedor = self._validar_id(id_vendedor)
        fila = await self._repositorio.obtener_por_id(id_vendedor)
        if fila is None:
            raise LookupError(f"No existe un vendedor con id = {id_vendedor}")
        return fila

    async def crear(self, datos: dict) -> None:
        await self._repositorio.crear(datos)

    async def actualizar(self, id_vendedor: int, datos: dict) -> int:
        id_vendedor = self._validar_id(id_vendedor)
        if not datos:
            raise ValueError("No se envió ningún campo para actualizar.")
        filas_afectadas = await self._repositorio.actualizar(id_vendedor, datos)
        if filas_afectadas == 0:
            raise LookupError(f"No existe un vendedor con id = {id_vendedor}")
        return filas_afectadas

    async def eliminar(self, id_vendedor: int) -> int:
        id_vendedor = self._validar_id(id_vendedor)
        filas_eliminadas = await self._repositorio.eliminar(id_vendedor)
        if filas_eliminadas == 0:
            raise LookupError(f"No existe un vendedor con id = {id_vendedor}")
        return filas_eliminadas
