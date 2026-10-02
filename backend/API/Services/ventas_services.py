from datetime import date

from Services.helpers import (clean, ensure_cliente, execute, new_uuid, query,
                              resolve_producto, serialize_rows)
from Services.validation import non_negative_number, optional_id, valid_date


def servListVentas(id=None):
    rows = query(
        """SELECT id, uuid, factura, fecha, cliente, cliente_documento,
                  productos_resumen AS producto, unidades_totales AS cantidad,
                  total, estado, vendedor
           FROM V_HISTORIAL_VENTAS
           {where}
           ORDER BY fecha DESC, id DESC"""
        .format(where="WHERE id = %s" if id is not None else ""),
        (id,) if id is not None else (),
    )
    return serialize_rows(rows)


def _payload(data):
    fecha = clean(data.get("fecha")) or date.today().isoformat()
    try:
        total = float(data.get("total") or 0)
    except (TypeError, ValueError):
        total = 0.0
    try:
        cantidad = int(float(data.get("cantidad") or 1))
    except (TypeError, ValueError):
        cantidad = 1
    if cantidad < 1:
        cantidad = 1
    estado = clean(data.get("estado"), "Completada")
    if estado not in ("Completada", "Pendiente", "Cancelada"):
        estado = "Completada"
    return fecha, total, cantidad, estado


def _siguiente_factura():
    ultimo = query(
        """SELECT MAX(CAST(SUBSTRING_INDEX(VENT_NUMERO_FACTURA, '-', -1) AS UNSIGNED)) AS n
           FROM T_VENTAS WHERE VENT_NUMERO_FACTURA IS NOT NULL"""
    )
    return f"VNT-{int((ultimo[0]['n'] or 0) + 1):03d}"


def addVentas(data):
    if data.get("fecha") not in (None, ""):
        error = valid_date(data["fecha"])
        if error:
            return error
    if data.get("estado") not in (None, "", "Completada", "Pendiente", "Cancelada"):
        return {"mensaje": "El estado de la venta no es valido"}, 400
    for field, integer, strictly_positive in (
        ("total", False, False),
        ("cantidad", True, True),
    ):
        value = data.get(field)
        if value not in (None, ""):
            _, error, status = non_negative_number(
                value, field, integer=integer, strictly_positive=strictly_positive
            )
            if error:
                return error, status
    user_id, error = optional_id(data.get("usua_id"), "usua_id")
    if error:
        return error
    if user_id is not None and not query(
        "SELECT USUA_ID FROM T_USUARIOS WHERE USUA_ID = %s", (user_id,)
    ):
        return {"mensaje": "Usuario no encontrado"}, 404
    fecha, total, cantidad, estado = _payload(data)
    cliente = clean(data.get("cliente"))
    producto = clean(data.get("producto"))
    if not cliente:
        return {"mensaje": "El cliente es obligatorio"}, 400

    cli_id = ensure_cliente(cliente, clean(data.get("cliente_documento")))
    prod_id = resolve_producto(producto)

    vent_id = execute(
        """INSERT INTO T_VENTAS
           (VENT_UUID, VENT_NUMERO_FACTURA, VENT_FECHA, VENT_TOTAL, VENT_ESTADO,
            VENT_USUA_ID, VENT_CLI_ID, VENT_OBSERVACIONES)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (new_uuid(), _siguiente_factura(), fecha, total, estado,
         user_id, cli_id, producto or None),
    )

    if prod_id:
        precio_unitario = round(total / cantidad, 2) if cantidad else 0
        execute(
            """INSERT INTO T_VENT_PROD
               (VENTPRO_UUID, VENTPRO_CANTIDAD, VENTPRO_PRECIO_UNITARIO, VENTPRO_SUBTOTAL,
                VENTPRO_VENT_ID, VENTPRO_PROD_ID)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (new_uuid(), cantidad, precio_unitario, total, vent_id, prod_id),
        )

    return {"mensaje": "Venta agregada correctamente", "id": vent_id}, 201


def updateVentas(id, data):
    if not query("SELECT VENT_ID FROM T_VENTAS WHERE VENT_ID = %s", (id,)):
        return {"mensaje": "Venta no encontrada"}, 404

    if data.get("fecha") not in (None, ""):
        error = valid_date(data["fecha"])
        if error:
            return error
    if data.get("estado") not in (None, "", "Completada", "Pendiente", "Cancelada"):
        return {"mensaje": "El estado de la venta no es valido"}, 400
    for field, integer, strictly_positive in (
        ("total", False, False),
        ("cantidad", True, True),
    ):
        value = data.get(field)
        if value not in (None, ""):
            _, error, status = non_negative_number(
                value, field, integer=integer, strictly_positive=strictly_positive
            )
            if error:
                return error, status
    fecha, total, cantidad, estado = _payload(data)
    cliente = clean(data.get("cliente"))
    producto = clean(data.get("producto"))
    if not cliente:
        return {"mensaje": "El cliente es obligatorio"}, 400

    cli_id = ensure_cliente(cliente, clean(data.get("cliente_documento")))
    prod_id = resolve_producto(producto)

    execute(
        """UPDATE T_VENTAS SET VENT_FECHA = %s, VENT_TOTAL = %s, VENT_ESTADO = %s,
           VENT_CLI_ID = %s, VENT_OBSERVACIONES = %s
           WHERE VENT_ID = %s""",
        (fecha, total, estado, cli_id, producto or None, id),
    )

    execute("DELETE FROM T_VENT_PROD WHERE VENTPRO_VENT_ID = %s", (id,))
    if prod_id:
        precio_unitario = round(total / cantidad, 2) if cantidad else 0
        execute(
            """INSERT INTO T_VENT_PROD
               (VENTPRO_UUID, VENTPRO_CANTIDAD, VENTPRO_PRECIO_UNITARIO, VENTPRO_SUBTOTAL,
                VENTPRO_VENT_ID, VENTPRO_PROD_ID)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (new_uuid(), cantidad, precio_unitario, total, id, prod_id),
        )

    return {"mensaje": "Venta actualizada correctamente", "id": id}, 200


def deleteVentas(id):
    if not query("SELECT VENT_ID FROM T_VENTAS WHERE VENT_ID = %s", (id,)):
        return {"mensaje": "Venta no encontrada"}, 404
    execute("DELETE FROM T_VENTAS WHERE VENT_ID = %s", (id,))
    return {"mensaje": "Venta eliminada correctamente"}, 200
