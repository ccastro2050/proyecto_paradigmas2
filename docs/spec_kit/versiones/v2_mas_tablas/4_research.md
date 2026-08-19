# Research — Versión 2: decisiones y alternativas

> Lectura opcional: el PORQUÉ de cada decisión del [plan](3_plan.md).

---

## D1 — ¿Cuatro moldes de una sola vez?

El gemelo C# del curso replicó el molde de a poco (v2: persona; v3: el
resto). Aquí se replican 4 en una versión. **Por qué:** el molde ya quedó
demostrado en la v1 y este proyecto avanza por bloques conceptuales (el
mapa reserva la v3 para el segundo motor y la v4 para completar la BD).
La factura NECESITA cliente y vendedor con endpoints para que la cadena
comercial sea demostrable — llegan juntos.

## D2 — Factura vía procedimientos almacenados (la API como traductora)

**Alternativas:** (a) la API arma la factura con INSERTs y calcula
subtotales · (b) la API llama los SPs que ya viven en `db/init.sql`.

**Decisión: (b).** La lógica transaccional (mínimo de renglones, stock,
totales) ya está en la BD — duplicarla en Python sería tener DOS verdades.
Además es la lección ACID: cabecera + renglones + stock + total en UNA
transacción del motor. La API valida la FORMA (Pydantic), llama, traduce.

## D3 — CALL con INOUT desde asyncpg

En PostgreSQL los SPs son `PROCEDURE … INOUT p_resultado JSON` y el
`CALL` devuelve los INOUT como una fila de resultado. Con SQLAlchemy
async: `execute(text("CALL sp(…, NULL)"))` → `first()[0]` es el JSON (que
asyncpg entrega como `str` → `json.loads`). El detalle de entrada viaja
como texto y se tipa con `cast(:productos as json)` en el propio CALL.

## D4 — Una excepción de conflicto propia (`ConflictoError`)

La v1 tradujo con builtins: `ValueError` → 400, `LookupError` → 404. Para
el 409 ("ya está anulada") Python no trae un builtin razonable —
`excepciones.py` define `ConflictoError`. Sigue la misma regla: el
controller conoce EXCEPCIONES DE NEGOCIO, jamás `DBAPIError` ni SQLSTATE.

## D5 — Los autonuméricos se consumen aunque el INSERT falle

Las secuencias de PostgreSQL avanzan con cada intento — un INSERT
rechazado por FK o un SP que hace ROLLBACK **consumen el número igual**
(las secuencias viven fuera de la transacción, por velocidad). Por eso el
quickstart pide ANOTAR los ids que devuelven las lecturas en vez de
suponer "el siguiente". No es un bug de la API: es el motor.

## D6 — Cliente con opcionales de verdad

`credito` tiene DEFAULT 0 **en la BD** y `fkcodempresa` acepta NULL. La
API los declara opcionales en el modelo del POST y el INSERT es dinámico
(solo columnas enviadas): el default lo aplica quien lo declaró — la BD.
La alternativa (que la API ponga el 0) duplicaría la verdad, y cuando
cambien el default habría que cambiarlo en dos lugares.

## D7 — Anular, no borrar

La API expone **anular** (estado = 'anulada' + stock restaurado, el SP
`sp_anular_factura`) y NO expone el borrado físico aunque exista
`sp_borrar_factura_y_productosporfactura`. Negocio real: las facturas no
se esfuman — se anulan y quedan. El borrado físico quedará para roles
administrativos cuando exista control de acceso (más adelante en la ruta).
