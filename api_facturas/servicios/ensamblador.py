"""
Ensamblador — el ÚNICO lugar del sistema que conoce clases concretas.

La v2 lo hace crecer con cinco funciones más, TODAS de la misma forma: la
repetición ya se nota — ese olor es el argumento de la fábrica, pero la
fábrica sin un segundo motor sería especulación (YAGNI). Cuando la v3
agregue MariaDB, SOLO este archivo se convertirá en la fábrica real —
controllers y servicios no se tocarán: ese será el examen del principio
abierto/cerrado.
"""

import os

from repositorios.repositorio_cliente_postgresql import (
    RepositorioClientePostgreSQL,
)
from repositorios.repositorio_empresa_postgresql import (
    RepositorioEmpresaPostgreSQL,
)
from repositorios.repositorio_factura_postgresql import (
    RepositorioFacturaPostgreSQL,
)
from repositorios.repositorio_persona_postgresql import (
    RepositorioPersonaPostgreSQL,
)
from repositorios.repositorio_producto_postgresql import (
    RepositorioProductoPostgreSQL,
)
from repositorios.repositorio_vendedor_postgresql import (
    RepositorioVendedorPostgreSQL,
)
from servicios.abstracciones.i_servicio_cliente import IServicioCliente
from servicios.abstracciones.i_servicio_empresa import IServicioEmpresa
from servicios.abstracciones.i_servicio_factura import IServicioFactura
from servicios.abstracciones.i_servicio_persona import IServicioPersona
from servicios.abstracciones.i_servicio_producto import IServicioProducto
from servicios.abstracciones.i_servicio_vendedor import IServicioVendedor
from servicios.servicio_cliente import ServicioCliente
from servicios.servicio_empresa import ServicioEmpresa
from servicios.servicio_factura import ServicioFactura
from servicios.servicio_persona import ServicioPersona
from servicios.servicio_producto import ServicioProducto
from servicios.servicio_vendedor import ServicioVendedor


def crear_servicio_producto() -> IServicioProducto:
    """Arma el servicio con su repositorio (la cadena viene del entorno)."""
    repositorio = RepositorioProductoPostgreSQL(os.environ["DB_POSTGRES"])
    return ServicioProducto(repositorio)


# ----------------------------------------------------------------------
# v2 — las cinco rebanadas nuevas (el mismo molde de tres líneas)
# ----------------------------------------------------------------------

def crear_servicio_persona() -> IServicioPersona:
    """Arma el servicio de persona con su repositorio PostgreSQL."""
    repositorio = RepositorioPersonaPostgreSQL(os.environ["DB_POSTGRES"])
    return ServicioPersona(repositorio)


def crear_servicio_empresa() -> IServicioEmpresa:
    """Arma el servicio de empresa con su repositorio PostgreSQL."""
    repositorio = RepositorioEmpresaPostgreSQL(os.environ["DB_POSTGRES"])
    return ServicioEmpresa(repositorio)


def crear_servicio_cliente() -> IServicioCliente:
    """Arma el servicio de cliente con su repositorio PostgreSQL."""
    repositorio = RepositorioClientePostgreSQL(os.environ["DB_POSTGRES"])
    return ServicioCliente(repositorio)


def crear_servicio_vendedor() -> IServicioVendedor:
    """Arma el servicio de vendedor con su repositorio PostgreSQL."""
    repositorio = RepositorioVendedorPostgreSQL(os.environ["DB_POSTGRES"])
    return ServicioVendedor(repositorio)


def crear_servicio_factura() -> IServicioFactura:
    """Arma el servicio de factura con su repositorio PostgreSQL (SPs)."""
    repositorio = RepositorioFacturaPostgreSQL(os.environ["DB_POSTGRES"])
    return ServicioFactura(repositorio)
