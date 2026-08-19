# Modelo de datos — Versión 2: las tablas que entran en juego

> La BD `bdfacturas_postgres_local` está COMPLETA desde la v1
> (`db/init.sql` — infraestructura dada). La v2 no crea tablas: EMPIEZA A
> USAR seis que ya estaban ahí. Este documento describe esas seis, sus
> semillas y la lógica de BD que la API va a traducir.

---

## 1. Los cuatro moldes

| Tabla | PK | Columnas | Restricciones |
|---|---|---|---|
| `persona` | codigo VARCHAR(10) | nombre 100, email 100, telefono 20 (todos NOT NULL) | — |
| `empresa` | codigo VARCHAR(10) | nombre 100 NOT NULL | — |
| `cliente` | id SERIAL | credito NUMERIC NOT NULL **DEFAULT 0**, fkcodpersona 10 NOT NULL, fkcodempresa 10 **NULL** | FK → persona, FK → empresa |
| `vendedor` | id SERIAL | carnet INT NOT NULL, direccion 100 NOT NULL, fkcodpersona 10 NOT NULL | FK → persona |

## 2. El maestro-detalle

| Tabla | PK | Columnas clave |
|---|---|---|
| `factura` | numero SERIAL | fecha (DEFAULT now), total (DEFAULT 0), estado (DEFAULT 'activa'), fkidcliente, fkidvendedor |
| `productosporfactura` | (fknumfactura, fkcodproducto) | cantidad, subtotal (DEFAULT 0) — FK a factura ON DELETE CASCADE |

**El trigger `actualizar_totales_y_stock()`** (BEFORE INSERT/UPDATE/DELETE
sobre `productosporfactura`): valida stock suficiente, calcula `subtotal`
(cantidad × valorunitario), descuenta/restaura `stock` y recalcula el
`total` de la factura. La API JAMÁS escribe esas columnas.

**Los SPs que la v2 llama** (todos con `INOUT p_resultado JSON`):

| SP | Papel | Errores de negocio (P0001) |
|---|---|---|
| `sp_listar_facturas_y_productosporfactura` | todas las facturas, nombres de cliente/vendedor resueltos, productos adentro | — |
| `sp_consultar_factura_y_productosporfactura` | una factura, igual de completa | `Factura N no existe` → 404 |
| `sp_insertar_factura_y_productosporfactura` | cabecera + renglones en UNA transacción (el trigger hace las cuentas) | mínimo de renglones (no llega: Pydantic corta antes) · stock insuficiente (trigger) → 500 |
| `sp_anular_factura` | estado='anulada' + stock restaurado (borrado lógico) | `no existe` → 404 · `ya está anulada` → 409 |

## 3. Semillas (las que la v2 empieza a mostrar)

| Tabla | Filas | Detalle |
|---|---|---|
| persona | 6 | P001 Ana Torres … P006 Pedro Castillo |
| empresa | 3 | E001, E002, E999 |
| cliente | 4 | ids **1, 2, 3 y 5** (el hueco del 4 es a propósito — y D5 del research explica por qué los ids no siempre son "el siguiente") |
| vendedor | 3 | ids 1-3, carnets 1001-1003 (P002, P004, P006) |
| factura | 6 | numeros 1-6, todas 'activa', con 12 renglones en productosporfactura |
| producto | 8 | (v1) — PR001 stock 17, PR003 stock 42: los números de la regresión |

## 4. Verdades que la API debe respetar

- `productosporfactura` NO tiene endpoints: se lee dentro de factura y se
  escribe a través del SP de insertar.
- `subtotal`, `total` y `stock` son del TRIGGER: si la API los recibiera
  en un body, sería un agujero de integridad (por eso los modelos Pydantic
  ni los declaran).
- El DEFAULT de `credito` es de la BD; la API no lo conoce (D6).
- Los emails/telefonos de persona NO llevan formato validado en BD; la
  frontera Pydantic exige solo longitudes (el formato estricto llegaría
  como regla de negocio si el curso lo pide).
