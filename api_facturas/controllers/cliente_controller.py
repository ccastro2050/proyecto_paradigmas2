"""
Controller de cliente — la capa HTTP (v2). CALCADO del de producto:
traduce peticiones → servicio y excepciones de negocio → códigos.
"""

from fastapi import APIRouter, HTTPException, Response

from models.cliente import Cliente, ClienteActualizar, ClienteReemplazo
from servicios.ensamblador import crear_servicio_cliente

router = APIRouter(prefix="/api", tags=["Cliente"])


def _error(estado: int, mensaje: str, detalle: str) -> HTTPException:
    return HTTPException(
        status_code=estado,
        detail={"estado": estado, "mensaje": mensaje, "detalle": detalle},
    )


@router.get("/cliente")
async def listar_clientes(limite: int = 1000):
    try:
        servicio = crear_servicio_cliente()
        filas = await servicio.listar(limite)
        if not filas:
            return Response(status_code=204)
        return {"tabla": "cliente", "limite": limite,
                "total": len(filas), "datos": filas}
    except ValueError as excepcion:
        raise _error(400, "Parámetros inválidos.", str(excepcion))
    except Exception as excepcion:
        raise _error(500, "Error al consultar clientes.", str(excepcion))


@router.get("/cliente/{id_cliente}")
async def obtener_cliente(id_cliente: int):
    try:
        servicio = crear_servicio_cliente()
        return await servicio.obtener(id_cliente)
    except ValueError as excepcion:
        raise _error(400, "Parámetros inválidos.", str(excepcion))
    except LookupError as excepcion:
        raise _error(404, "Cliente no encontrado.", str(excepcion))
    except Exception as excepcion:
        raise _error(500, "Error al consultar el cliente.", str(excepcion))


@router.post("/cliente")
async def crear_cliente(modelo: Cliente):
    try:
        servicio = crear_servicio_cliente()
        # Opcionales fuera del INSERT: la BD pone sus defaults (D6):
        datos = modelo.model_dump(exclude_none=True)
        await servicio.crear(datos)
        return {"estado": 200, "mensaje": "Cliente creado exitosamente."}
    except ValueError as excepcion:
        raise _error(400, "Datos inválidos.", str(excepcion))
    except Exception as excepcion:
        # Aquí caen la PK duplicada y las FK: el motor viaja en `detalle`.
        raise _error(500, "No se pudo crear el cliente.", str(excepcion))


@router.put("/cliente/{id_cliente}")
async def reemplazar_cliente(id_cliente: int, modelo: ClienteReemplazo):
    try:
        servicio = crear_servicio_cliente()
        # PUT escribe las 3 columnas (fkcodempresa = NULL si llegó null):
        filas = await servicio.actualizar(id_cliente, modelo.model_dump())
        return {"estado": 200, "mensaje": "Cliente reemplazado exitosamente.",
                "filasAfectadas": filas}
    except ValueError as excepcion:
        raise _error(400, "Parámetros inválidos.", str(excepcion))
    except LookupError as excepcion:
        raise _error(404, "Cliente no encontrado.", str(excepcion))
    except Exception as excepcion:
        raise _error(500, "No se pudo reemplazar el cliente.", str(excepcion))


@router.patch("/cliente/{id_cliente}")
async def actualizar_cliente(id_cliente: int, modelo: ClienteActualizar):
    try:
        servicio = crear_servicio_cliente()
        datos = modelo.model_dump(exclude_none=True)
        filas = await servicio.actualizar(id_cliente, datos)
        return {"estado": 200, "mensaje": "Cliente actualizado exitosamente.",
                "filasAfectadas": filas}
    except ValueError as excepcion:
        raise _error(400, "Parámetros inválidos.", str(excepcion))
    except LookupError as excepcion:
        raise _error(404, "Cliente no encontrado.", str(excepcion))
    except Exception as excepcion:
        raise _error(500, "No se pudo actualizar el cliente.", str(excepcion))


@router.delete("/cliente/{id_cliente}")
async def eliminar_cliente(id_cliente: int):
    try:
        servicio = crear_servicio_cliente()
        filas = await servicio.eliminar(id_cliente)
        return {"estado": 200, "mensaje": "Cliente eliminado exitosamente.",
                "filasEliminadas": filas}
    except ValueError as excepcion:
        raise _error(400, "Parámetros inválidos.", str(excepcion))
    except LookupError as excepcion:
        raise _error(404, "Cliente no encontrado.", str(excepcion))
    except Exception as excepcion:
        raise _error(500, "No se pudo eliminar el cliente.", str(excepcion))
