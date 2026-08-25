"""
Punto de entrada de la API Facturas v2.

Crea la aplicación FastAPI, registra el router de producto y expone el
endpoint de diagnóstico. Swagger queda en /docs y ReDoc en /redoc
(los defaults de FastAPI).

Arranque:  uvicorn main:app --port 8003 --reload
Requiere:  la variable de entorno DB_POSTGRES (ver 7_quickstart.md).
"""

from fastapi import FastAPI

from controllers.cliente_controller import router as router_cliente
from controllers.empresa_controller import router as router_empresa
from controllers.factura_controller import router as router_factura
from controllers.persona_controller import router as router_persona
from controllers.producto_controller import router as router_producto
from controllers.vendedor_controller import router as router_vendedor

app = FastAPI(
    title="API Facturas",
    version="v2",
    description="Producto, persona, empresa, cliente, vendedor y factura "
                "maestro-detalle contra PostgreSQL — versión 2 del proyecto.",
)

# Un router por entidad — el molde de la v1, replicado (v2):
app.include_router(router_producto)
app.include_router(router_persona)
app.include_router(router_empresa)
app.include_router(router_cliente)
app.include_router(router_vendedor)
app.include_router(router_factura)


@app.get("/", tags=["Diagnóstico"])
async def diagnostico():
    """Confirma que la API está en línea (usable como healthcheck)."""
    return {"mensaje": "API Facturas funcionando", "version": "v2",
            "documentacion": "/docs"}
