"""
Controller de vendedor — la capa HTTP (v2). CALCADO del de producto:
traduce peticiones → servicio y excepciones de negocio → códigos.
"""

from fastapi import APIRouter, HTTPException, Response

from models.vendedor import Vendedor, VendedorActualizar, VendedorReemplazo
from servicios.ensamblador import crear_servicio_vendedor

router = APIRouter(prefix="/api", tags=["Vendedor"])


def _error(estado: int, mensaje: str, detalle: str) -> HTTPException:
    return HTTPException(
        status_code=estado,
        detail={"estado": estado, "mensaje": mensaje, "detalle": detalle},
    )


@router.get("/vendedor")
async def listar_vendedors(limite: int = 1000):
    try:
        servicio = crear_servicio_vendedor()
        filas = await servicio.listar(limite)
        if not filas:
            return Response(status_code=204)
        return {"tabla": "vendedor", "limite": limite,
                "total": len(filas), "datos": filas}
    except ValueError as excepcion:
        raise _error(400, "Parámetros inválidos.", str(excepcion))
    except Exception as excepcion:
        raise _error(500, "Error al consultar vendedors.", str(excepcion))


@router.get("/vendedor/{id_vendedor}")
async def obtener_vendedor(id_vendedor: int):
    try:
        servicio = crear_servicio_vendedor()
        return await servicio.obtener(id_vendedor)
    except ValueError as excepcion:
        raise _error(400, "Parámetros inválidos.", str(excepcion))
    except LookupError as excepcion:
        raise _error(404, "Vendedor no encontrado.", str(excepcion))
    except Exception as excepcion:
        raise _error(500, "Error al consultar el vendedor.", str(excepcion))


@router.post("/vendedor")
async def crear_vendedor(modelo: Vendedor):
    try:
        servicio = crear_servicio_vendedor()
        await servicio.crear(modelo.model_dump())
        return {"estado": 200, "mensaje": "Vendedor creado exitosamente."}
    except ValueError as excepcion:
        raise _error(400, "Datos inválidos.", str(excepcion))
    except Exception as excepcion:
        # Aquí caen la PK duplicada y las FK: el motor viaja en `detalle`.
        raise _error(500, "No se pudo crear el vendedor.", str(excepcion))


@router.put("/vendedor/{id_vendedor}")
async def reemplazar_vendedor(id_vendedor: int, modelo: VendedorReemplazo):
    try:
        servicio = crear_servicio_vendedor()
        filas = await servicio.actualizar(id_vendedor, modelo.model_dump())
        return {"estado": 200, "mensaje": "Vendedor reemplazado exitosamente.",
                "filasAfectadas": filas}
    except ValueError as excepcion:
        raise _error(400, "Parámetros inválidos.", str(excepcion))
    except LookupError as excepcion:
        raise _error(404, "Vendedor no encontrado.", str(excepcion))
    except Exception as excepcion:
        raise _error(500, "No se pudo reemplazar el vendedor.", str(excepcion))


@router.patch("/vendedor/{id_vendedor}")
async def actualizar_vendedor(id_vendedor: int, modelo: VendedorActualizar):
    try:
        servicio = crear_servicio_vendedor()
        datos = modelo.model_dump(exclude_none=True)
        filas = await servicio.actualizar(id_vendedor, datos)
        return {"estado": 200, "mensaje": "Vendedor actualizado exitosamente.",
                "filasAfectadas": filas}
    except ValueError as excepcion:
        raise _error(400, "Parámetros inválidos.", str(excepcion))
    except LookupError as excepcion:
        raise _error(404, "Vendedor no encontrado.", str(excepcion))
    except Exception as excepcion:
        raise _error(500, "No se pudo actualizar el vendedor.", str(excepcion))


@router.delete("/vendedor/{id_vendedor}")
async def eliminar_vendedor(id_vendedor: int):
    try:
        servicio = crear_servicio_vendedor()
        filas = await servicio.eliminar(id_vendedor)
        return {"estado": 200, "mensaje": "Vendedor eliminado exitosamente.",
                "filasEliminadas": filas}
    except ValueError as excepcion:
        raise _error(400, "Parámetros inválidos.", str(excepcion))
    except LookupError as excepcion:
        raise _error(404, "Vendedor no encontrado.", str(excepcion))
    except Exception as excepcion:
        raise _error(500, "No se pudo eliminar el vendedor.", str(excepcion))
