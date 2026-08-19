"""
Modelos Pydantic de factura — la FRONTERA DE ENTRADA (v2).

Solo existe el modelo del POST: factura no tiene PUT/PATCH/DELETE (se
ANULA, borrado lógico). Fíjese en lo que NO está: subtotal y total no
tienen dónde llegar — los calcula el trigger de la BD. La frontera
también ES contrato.
"""

from pydantic import BaseModel, Field


class RenglonFactura(BaseModel):
    """Un renglón del detalle: qué producto y cuántas unidades."""

    codigo: str = Field(min_length=1, max_length=20)
    cantidad: int = Field(ge=1)


class FacturaCrear(BaseModel):
    """POST /api/factura — cabecera + detalle en un solo body.

    `min_length=1`: una factura sin renglones muere en 422 ANTES de tocar
    la BD (el SP también lo valida — defensa en profundidad, pero la
    frontera corta primero).
    """

    fkidcliente: int = Field(ge=1)
    fkidvendedor: int = Field(ge=1)
    productos: list[RenglonFactura] = Field(min_length=1)
