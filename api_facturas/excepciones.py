"""
Excepciones de NEGOCIO propias de la API (v2).

La v1 tradujo con builtins (ValueError → 400 · LookupError → 404). El 409
no tiene builtin razonable — nace aquí. La regla sigue: los controllers
conocen EXCEPCIONES DE NEGOCIO, jamás DBAPIError ni códigos SQLSTATE.
"""


class ConflictoError(Exception):
    """El estado actual del recurso rechaza la operación → HTTP 409.

    El caso de la v2: anular una factura que YA está anulada.
    """
