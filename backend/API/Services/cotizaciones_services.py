from datetime import date

from Services.helpers import (clean, ensure_cliente, execute, new_uuid, query,
                              resolve_producto, serialize_rows)
from Services.validation import non_negative_number, optional_id, valid_date


def servListCotizaciones(id=None):
    rows = query(
        """SELECT r.id, r.uuid, r.numero, r.fecha, r.cliente, r.cliente_correo,
                  c.COT_PRO_NOMBRE AS producto, c.COT_PRO_CANTIDAD AS cantidad,
                  r.total, r.estado, r.notas, r.cantidad_items, r.asesor
           FROM V_RESUMEN_COTIZACIONES r
           JOIN T_COTIZACIONES c ON c.COT_ID = r.id
           {where}
           ORDER BY r.fecha DESC, r.id DESC"""
        .format(where="WHERE r.id = %s" if id is not None else ""),
        (id,) if id is not None else (),
    )
    rows = serialize_rows(rows)
    if not rows:
        return rows

    ids = [row["id"] for row in rows]
    placeholders = ",".join(["%s"] * len(ids))
    detalles = query(
        f"""SELECT DETCOT_COT_ID AS cot_id, DETCOT_CODIGO AS codigo, DETCOT_NOMBRE AS nombre,
                   DETCOT_CANTIDAD AS cantidad, DETCOT_PRECIO_UNITARIO AS precio,
                   DETCOT_SUBTOTAL AS subtotal
            FROM T_DETALLE_COTIZACION
            WHERE DETCOT_COT_ID IN ({placeholders})
            ORDER BY DETCOT_ID""",
        tuple(ids),
    )
    for row in rows:
        row["items"] = [
            {k: v for k, v in d.items() if k != "cot_id"}
            for d in detalles
            if d["cot_id"] == row["id"]
        ]
    return rows


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
    estado = clean(data.get("estado"), "Pendiente")
    if estado not in ("Pendiente", "Enviada", "Aprobada", "Rechazada"):
        estado = "Pendiente"
    notas = clean(data.get("notas"), "")
    producto = clean(data.get("producto"), "")
    precio = data.get("precio")
    try:
        precio = float(precio) if precio not in (None, "") else (total / cantidad if cantidad else 0)
    except (TypeError, ValueError):
        precio = 0.0
    codigo = clean(data.get("producto_codigo"), "")
    if not codigo and producto:
        fila = query("SELECT PROD_CODIGO FROM T_PRODUCTOS WHERE PROD_NOMBRE = %s LIMIT 1", (producto,))
        codigo = fila[0]["PROD_CODIGO"] if fila else ""
    return fecha, total, cantidad, estado, notas, producto, precio, codigo


def _siguiente_numero():
    ultimo = query(
        """SELECT MAX(CAST(SUBSTRING_INDEX(COT_NUMERO, '-', -1) AS UNSIGNED)) AS n
           FROM T_COTIZACIONES WHERE COT_NUMERO IS NOT NULL"""
    )
    return f"COT-{int((ultimo[0]['n'] or 0) + 1):03d}"


def _guardar_detalle(cot_id, data):
    items = data.get("items")
    if not isinstance(items, list) or not items:
        return
    execute("DELETE FROM T_DETALLE_COTIZACION WHERE DETCOT_COT_ID = %s", (cot_id,))
    for item in items:
        nombre = clean(item.get("nombre"))
        if not nombre:
            continue
        try:
            cantidad = int(float(item.get("cantidad") or 1))
        except (TypeError, ValueError):
            cantidad = 1
        try:
            precio = float(item.get("precio") or 0)
        except (TypeError, ValueError):
            precio = 0.0
        prod_id = resolve_producto(nombre)
        execute(
            """INSERT INTO T_DETALLE_COTIZACION
               (DETCOT_UUID, DETCOT_COT_ID, DETCOT_PROD_ID, DETCOT_CODIGO, DETCOT_NOMBRE,
                DETCOT_CANTIDAD, DETCOT_PRECIO_UNITARIO, DETCOT_SUBTOTAL)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (new_uuid(), cot_id, prod_id, clean(item.get("codigo")) or "", nombre,
             cantidad, precio, round(cantidad * precio, 2)),
        )


def _validate_items(data):
    items = data.get("items")
    if items is None:
        return None
    if not isinstance(items, list):
        return {"mensaje": "El campo items debe ser una lista"}, 400
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            return {"mensaje": f"El elemento items[{index}] debe ser un objeto"}, 400
        if not clean(item.get("nombre")):
            return {"mensaje": f"El campo nombre es obligatorio en items[{index}]"}, 400
        _, error, status = non_negative_number(
            item.get("cantidad", 1), f"items[{index}].cantidad",
            integer=True, strictly_positive=True,
        )
        if error:
            return error, status
        _, error, status = non_negative_number(
            item.get("precio", 0), f"items[{index}].precio",
        )
        if error:
            return error, status
    return None


def addCotizaciones(data):
    error = _validate_items(data)
    if error:
        return error
    if data.get("fecha") not in (None, ""):
        error = valid_date(data["fecha"])
        if error:
            return error
    if data.get("estado") not in (None, "", "Pendiente", "Enviada", "Aprobada", "Rechazada"):
        return {"mensaje": "El estado de la cotizacion no es valido"}, 400
    for field, integer, strictly_positive in (
        ("total", False, False),
        ("cantidad", True, True),
        ("precio", False, False),
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
    fecha, total, cantidad, estado, notas, producto, precio, codigo = _payload(data)
    cliente = clean(data.get("cliente"))
    if not cliente:
        return {"mensaje": "El cliente es obligatorio"}, 400

    cli_id = ensure_cliente(cliente, clean(data.get("cliente_documento")))

    cot_id = execute(
        """INSERT INTO T_COTIZACIONES
           (COT_UUID, COT_NUMERO, COT_FECHA, COT_TOTAL_PAGAR, COT_ESTADO, COT_NOTAS,
            COT_USUA_ID, COT_CLI_ID, COT_PRO_CODIGO, COT_PRO_NOMBRE, COT_PRO_CANTIDAD,
            COT_PRO_PRECIO)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (new_uuid(), _siguiente_numero(), fecha, total, estado, notas,
         user_id, cli_id, codigo, producto or None, cantidad, precio),
    )
    _guardar_detalle(cot_id, data)
    return {"mensaje": "Cotizacion agregada correctamente", "id": cot_id}, 201


def updateCotizaciones(id, data):
    if not query("SELECT COT_ID FROM T_COTIZACIONES WHERE COT_ID = %s", (id,)):
        return {"mensaje": "Cotizacion no encontrada"}, 404

    error = _validate_items(data)
    if error:
        return error
    if data.get("fecha") not in (None, ""):
        error = valid_date(data["fecha"])
        if error:
            return error
    if data.get("estado") not in (None, "", "Pendiente", "Enviada", "Aprobada", "Rechazada"):
        return {"mensaje": "El estado de la cotizacion no es valido"}, 400
    for field, integer, strictly_positive in (
        ("total", False, False),
        ("cantidad", True, True),
        ("precio", False, False),
    ):
        value = data.get(field)
        if value not in (None, ""):
            _, error, status = non_negative_number(
                value, field, integer=integer, strictly_positive=strictly_positive
            )
            if error:
                return error, status
    fecha, total, cantidad, estado, notas, producto, precio, codigo = _payload(data)
    cliente = clean(data.get("cliente"))
    if not cliente:
        return {"mensaje": "El cliente es obligatorio"}, 400

    cli_id = ensure_cliente(cliente, clean(data.get("cliente_documento")))

    execute(
        """UPDATE T_COTIZACIONES SET COT_FECHA = %s, COT_TOTAL_PAGAR = %s, COT_ESTADO = %s,
           COT_NOTAS = %s, COT_CLI_ID = %s, COT_PRO_CODIGO = %s, COT_PRO_NOMBRE = %s,
           COT_PRO_CANTIDAD = %s, COT_PRO_PRECIO = %s
           WHERE COT_ID = %s""",
        (fecha, total, estado, notas, cli_id, codigo, producto or None, cantidad, precio, id),
    )
    _guardar_detalle(id, data)
    return {"mensaje": "Cotizacion actualizada correctamente", "id": id}, 200


def deleteCotizaciones(id):
    if not query("SELECT COT_ID FROM T_COTIZACIONES WHERE COT_ID = %s", (id,)):
        return {"mensaje": "Cotizacion no encontrada"}, 404
    execute("DELETE FROM T_COTIZACIONES WHERE COT_ID = %s", (id,))
    return {"mensaje": "Cotizacion eliminada correctamente"}, 200
