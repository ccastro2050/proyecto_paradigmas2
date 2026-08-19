"""
Servicio de persona — la capa de NEGOCIO (v2). CALCADO del de producto:
recibe la interfaz del repositorio por constructor y comunica los
problemas con excepciones de negocio (ValueError → 400 · LookupError → 404).
"""

from repositorios.abstracciones.i_repositorio_persona import IRepositorioPersona


class ServicioPersona:
    """Reglas de negocio del CRUD de persona."""

    def __init__(self, repositorio: IRepositorioPersona):
        self._repositorio = repositorio

    @staticmethod
    def _validar_codigo(codigo: str) -> str:
        codigo = (codigo or "").strip()
        if not codigo:
            raise ValueError("El código de la persona no puede estar vacío.")
        return codigo

    async def listar(self, limite: int) -> list[dict]:
        if limite <= 0:
            raise ValueError("El límite debe ser un entero mayor que cero.")
        return await self._repositorio.obtener_todos(limite)

    async def obtener(self, codigo: str) -> dict:
        codigo = self._validar_codigo(codigo)
        fila = await self._repositorio.obtener_por_codigo(codigo)
        if fila is None:
            raise LookupError(f"No existe una persona con codigo = {codigo}")
        return fila

    async def crear(self, datos: dict) -> None:
        await self._repositorio.crear(datos)

    async def actualizar(self, codigo: str, datos: dict) -> int:
        codigo = self._validar_codigo(codigo)
        if not datos:
            raise ValueError("No se envió ningún campo para actualizar.")
        filas_afectadas = await self._repositorio.actualizar(codigo, datos)
        if filas_afectadas == 0:
            raise LookupError(f"No existe una persona con codigo = {codigo}")
        return filas_afectadas

    async def eliminar(self, codigo: str) -> int:
        codigo = self._validar_codigo(codigo)
        filas_eliminadas = await self._repositorio.eliminar(codigo)
        if filas_eliminadas == 0:
            raise LookupError(f"No existe una persona con codigo = {codigo}")
        return filas_eliminadas
