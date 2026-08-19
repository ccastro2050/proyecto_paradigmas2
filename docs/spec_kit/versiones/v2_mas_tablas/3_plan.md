# Plan — Versión 2: más tablas (los moldes y la factura)

> Cómo se construye lo especificado en [2_spec.md](2_spec.md). El stack no
> cambia (FastAPI + SQLAlchemy async con text() + asyncpg + Pydantic):
> cambia la ESCALA — el molde de la v1 en serie, y la primera entidad que
> habla con procedimientos almacenados.

---

## 1. Inventario de archivos

**Nuevos (26):**

```
api_facturas/excepciones.py                      ← ConflictoError (→ 409)
api_facturas/models/{persona,empresa,cliente,vendedor,factura}.py        (5)
api_facturas/repositorios/abstracciones/i_repositorio_{persona,empresa,cliente,vendedor,factura}.py   (5)
api_facturas/repositorios/repositorio_{persona,empresa,cliente,vendedor,factura}_postgresql.py        (5)
api_facturas/servicios/abstracciones/i_servicio_{persona,empresa,cliente,vendedor,factura}.py         (5)
api_facturas/servicios/servicio_{persona,empresa,cliente,vendedor}.py + servicio_factura.py           (5)
api_facturas/controllers/{persona,empresa,cliente,vendedor,factura}_controller.py                     (5)
```

**Crecen (los únicos existentes que se tocan):**

| Archivo | Qué crece |
|---|---|
| `main.py` | ★ 5 `include_router` nuevos + `version="v2"` |
| `servicios/ensamblador.py` | ★ 5 funciones `crear_servicio_x()` (SIGUE siendo funciones simples — la fábrica es de la v3) |
| `pruebas/prueba_capas.py` | ★ persona con repositorio falso (criterio 6) |

**Intocables:** todo lo de producto y `db/init.sql` (las tablas, SPs y
trigger están ahí desde la v1 — infraestructura dada).

## 2. Los cuatro moldes (el calco por entidad)

La rebanada de producto se replica cambiando SOLO nombres, PK y campos:

| Pieza | producto (v1) | persona | empresa | cliente | vendedor |
|---|---|---|---|---|---|
| PK | codigo str | codigo str | codigo str | **id SERIAL** | **id SERIAL** |
| Ruta de detalle | `/{codigo}` | `/{codigo}` | `/{codigo}` | `/{id_cliente}` (int) | `/{id_vendedor}` (int) |
| Métodos repo | obtener_por_codigo | igual | igual | **obtener_por_id** | **obtener_por_id** |
| Particular | — | — | — | credito/fkcodempresa OPCIONALES al crear (D6) | — |

Reglas del calco:
- El **INSERT de cliente es dinámico**: solo las columnas enviadas — si el
  cliente no manda `credito`, el DEFAULT 0 lo pone la BD; si no manda
  `fkcodempresa`, queda NULL. (El mismo truco del SET dinámico del PATCH.)
- El PUT de cliente escribe las 3 columnas (con `fkcodempresa = NULL` si
  llegó null: reemplazo completo es reemplazo completo).
- Las entidades con PK SERIAL no la reciben en el POST: la asigna la BD.

## 3. El repositorio de factura (el único con diseño propio)

Los SPs de `db/init.sql` son `PROCEDURE` con `INOUT p_resultado JSON`. En
PostgreSQL el `CALL` devuelve los INOUT como UNA FILA de resultado:

```python
sql = text("CALL sp_insertar_factura_y_productosporfactura("
           ":cliente, :vendedor, cast(:productos as json), 1, NULL)")
async with self._obtener_engine().begin() as conexion:   # transacción
    resultado = await conexion.execute(sql, parametros)
    fila = resultado.first()          # la fila de los INOUT
    return json.loads(fila[0])        # p_resultado: JSON → dict
```

Los 4 métodos usan el mismo ayudante: `sp_listar…(NULL)`,
`sp_consultar…(:numero, NULL)`, `sp_insertar…(…)`, `sp_anular_factura(:numero, NULL)`.

**La traducción de errores** (los `RAISE EXCEPTION` de los SPs llegan como
`DBAPIError` con SQLSTATE `P0001`):

| El SP dice | La API traduce | HTTP |
|---|---|---|
| `Factura N no existe` | `LookupError` | 404 |
| `Factura N ya está anulada` | `ConflictoError` (nueva, `excepciones.py`) | 409 |
| `Stock insuficiente…` (trigger) · FK · lo demás | sube tal cual | 500 |

El patrón se decide por SQLSTATE + texto del mensaje — y NADIE por encima
del repositorio conoce `DBAPIError`.

## 4. Modelos de factura (la frontera valida la LISTA)

```python
class RenglonFactura(BaseModel):
    codigo: str = Field(min_length=1, max_length=20)
    cantidad: int = Field(ge=1)

class FacturaCrear(BaseModel):
    fkidcliente: int = Field(ge=1)
    fkidvendedor: int = Field(ge=1)
    productos: list[RenglonFactura] = Field(min_length=1)   # [] → 422
```

Nadie envía subtotales: el modelo no tiene dónde ponerlos — la frontera
también ES contrato.

## 5. El ensamblador crece (y todavía no duele lo suficiente)

Cinco funciones nuevas idénticas a `crear_servicio_producto()`. La lista
empieza a oler a repetición — ese olor es el argumento de la fábrica, pero
la fábrica SIN un segundo motor sería especulación (YAGNI): llega en la v3
con MariaDB, cuando algo la justifique.
