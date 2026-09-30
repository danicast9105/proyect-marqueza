from datetime import date

from Services.helpers import (clean, ensure_cliente, execute, new_uuid, query,
                              resolve_producto, serialize_rows)


def servListVentas():
    rows = query(
        """SELECT id, uuid, factura, fecha, cliente, cliente_documento,
                  productos_resumen AS producto, unidades_totales AS cantidad,
                  total, estado, vendedor
           FROM v_historial_ventas
           ORDER BY fecha DESC, id DESC"""
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
           FROM t_ventas WHERE VENT_NUMERO_FACTURA IS NOT NULL"""
    )
    return f"VNT-{int((ultimo[0]['n'] or 0) + 1):03d}"


def addVentas(data):
    fecha, total, cantidad, estado = _payload(data)
    cliente = clean(data.get("cliente"))
    producto = clean(data.get("producto"))
    if not cliente:
        return {"mensaje": "El cliente es obligatorio"}, 400

    cli_id = ensure_cliente(cliente, clean(data.get("cliente_documento")))
    prod_id = resolve_producto(producto)

    vent_id = execute(
        """INSERT INTO t_ventas
           (VENT_UUID, VENT_NUMERO_FACTURA, VENT_FECHA, VENT_TOTAL, VENT_ESTADO,
            VENT_USUA_ID, VENT_CLI_ID, VENT_OBSERVACIONES)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (new_uuid(), _siguiente_factura(), fecha, total, estado,
         data.get("usua_id") or None, cli_id, producto or None),
    )

    if prod_id:
        precio_unitario = round(total / cantidad, 2) if cantidad else 0
        execute(
            """INSERT INTO t_vent_prod
               (VENTPRO_UUID, VENTPRO_CANTIDAD, VENTPRO_PRECIO_UNITARIO, VENTPRO_SUBTOTAL,
                VENTPRO_VENT_ID, VENTPRO_PROD_ID)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (new_uuid(), cantidad, precio_unitario, total, vent_id, prod_id),
        )

    return {"mensaje": "Venta agregada correctamente", "id": vent_id}, 201


def updateVentas(id, data):
    if not query("SELECT VENT_ID FROM t_ventas WHERE VENT_ID = %s", (id,)):
        return {"mensaje": "Venta no encontrada"}, 404

    fecha, total, cantidad, estado = _payload(data)
    cliente = clean(data.get("cliente"))
    producto = clean(data.get("producto"))
    if not cliente:
        return {"mensaje": "El cliente es obligatorio"}, 400

    cli_id = ensure_cliente(cliente, clean(data.get("cliente_documento")))
    prod_id = resolve_producto(producto)

    execute(
        """UPDATE t_ventas SET VENT_FECHA = %s, VENT_TOTAL = %s, VENT_ESTADO = %s,
           VENT_CLI_ID = %s, VENT_OBSERVACIONES = %s
           WHERE VENT_ID = %s""",
        (fecha, total, estado, cli_id, producto or None, id),
    )

    execute("DELETE FROM t_vent_prod WHERE VENTPRO_VENT_ID = %s", (id,))
    if prod_id:
        precio_unitario = round(total / cantidad, 2) if cantidad else 0
        execute(
            """INSERT INTO t_vent_prod
               (VENTPRO_UUID, VENTPRO_CANTIDAD, VENTPRO_PRECIO_UNITARIO, VENTPRO_SUBTOTAL,
                VENTPRO_VENT_ID, VENTPRO_PROD_ID)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (new_uuid(), cantidad, precio_unitario, total, id, prod_id),
        )

    return {"mensaje": "Venta actualizada correctamente", "id": id}, 200


def deleteVentas(id):
    if not query("SELECT VENT_ID FROM t_ventas WHERE VENT_ID = %s", (id,)):
        return {"mensaje": "Venta no encontrada"}, 404
    execute("DELETE FROM t_ventas WHERE VENT_ID = %s", (id,))
    return {"mensaje": "Venta eliminada correctamente"}, 200
