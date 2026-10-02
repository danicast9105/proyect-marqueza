from Services.helpers import (clean, execute, new_uuid, query,
                              resolve_categoria, resolve_proveedor,
                              serialize_rows)
from Services.validation import non_negative_number, optional_id


def servListInsumos(id=None):
    rows = query(
        """SELECT id, uuid, codigo, nombre, categoria, proveedor, cantidad,
                  unidad, precioUnitario, valor_estimado, estado, nivel_stock
           FROM V_INVENTARIO_INSUMOS
           {where}
           ORDER BY nombre"""
        .format(where="WHERE id = %s" if id is not None else ""),
        (id,) if id is not None else (),
    )
    return serialize_rows(rows)


def _payload(data):
    codigo = clean(data.get("codigo"))
    nombre = clean(data.get("nombre"))
    try:
        cantidad = float(data.get("cantidad") or 0)
    except (TypeError, ValueError):
        cantidad = 0.0
    unidad = clean(data.get("unidad"), "metros")
    try:
        precio = float(data.get("precioUnitario") or data.get("precio") or 0)
    except (TypeError, ValueError):
        precio = 0.0
    estado = clean(data.get("estado"), "Disponible")
    if estado not in ("Disponible", "Agotado", "Pedido"):
        estado = "Disponible"
    categoria = resolve_categoria(clean(data.get("categoria"), "General"), "CATEGORIAS_INSUMOS")
    proveedor = resolve_proveedor(clean(data.get("proveedor")))
    return codigo, nombre, cantidad, unidad, precio, estado, categoria, proveedor


def _generar_codigo(nombre):
    prefijo = (nombre or "INS").strip().upper().replace(" ", "")[:6] or "INS"
    ultimo = query(
        "SELECT MAX(INS_ID) AS ultimo FROM T_INSUMOS WHERE INS_CODIGO LIKE %s",
        (f"{prefijo}-%",),
    )[0]["ultimo"] or 0
    return f"{prefijo}-{int(ultimo) + 1:03d}"


def addInsumos(data):
    if data.get("estado") not in (None, "", "Disponible", "Agotado", "Pedido"):
        return {"mensaje": "El estado del insumo no es valido"}, 400
    for field in ("cantidad", "precioUnitario", "precio"):
        value = data.get(field)
        if value not in (None, ""):
            _, error, status = non_negative_number(value, field)
            if error:
                return error, status
    user_id, error = optional_id(data.get("usua_id"), "usua_id")
    if error:
        return error
    if user_id is not None and not query(
        "SELECT USUA_ID FROM T_USUARIOS WHERE USUA_ID = %s", (user_id,)
    ):
        return {"mensaje": "Usuario no encontrado"}, 404
    codigo, nombre, cantidad, unidad, precio, estado, categoria, proveedor = _payload(data)
    if not nombre:
        return {"mensaje": "El nombre del insumo es obligatorio"}, 400
    if not codigo:
        codigo = _generar_codigo(nombre)
    if query("SELECT INS_ID FROM T_INSUMOS WHERE INS_CODIGO = %s", (codigo,)):
        return {"mensaje": "Ya existe un insumo con ese codigo"}, 409

    ins_id = execute(
        """INSERT INTO T_INSUMOS
           (INS_UUID, INS_CODIGO, INS_NOMBRE, INS_CANTIDAD, INS_UNIDAD, INS_PRECIO,
            INS_ESTADO, INS_USUA_ID, INS_PROV_ID, INS_DET_ETC_ID)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (new_uuid(), codigo, nombre, cantidad, unidad, precio, estado,
         user_id, proveedor, categoria),
    )
    return {"mensaje": "Insumo agregado correctamente", "id": ins_id}, 201


def updateInsumos(id, data):
    if not query("SELECT INS_ID FROM T_INSUMOS WHERE INS_ID = %s", (id,)):
        return {"mensaje": "Insumo no encontrado"}, 404

    if data.get("estado") not in (None, "", "Disponible", "Agotado", "Pedido"):
        return {"mensaje": "El estado del insumo no es valido"}, 400
    for field in ("cantidad", "precioUnitario", "precio"):
        value = data.get(field)
        if value not in (None, ""):
            _, error, status = non_negative_number(value, field)
            if error:
                return error, status
    codigo, nombre, cantidad, unidad, precio, estado, categoria, proveedor = _payload(data)
    if not nombre:
        return {"mensaje": "El nombre del insumo es obligatorio"}, 400
    if not codigo:
        codigo = query("SELECT INS_CODIGO FROM T_INSUMOS WHERE INS_ID = %s", (id,))[0]["INS_CODIGO"]
    if query("SELECT INS_ID FROM T_INSUMOS WHERE INS_CODIGO = %s AND INS_ID <> %s", (codigo, id)):
        return {"mensaje": "Ya existe otro insumo con ese codigo"}, 409

    execute(
        """UPDATE T_INSUMOS SET INS_CODIGO = %s, INS_NOMBRE = %s, INS_CANTIDAD = %s,
           INS_UNIDAD = %s, INS_PRECIO = %s, INS_ESTADO = %s, INS_PROV_ID = %s,
           INS_DET_ETC_ID = %s
           WHERE INS_ID = %s""",
        (codigo, nombre, cantidad, unidad, precio, estado, proveedor, categoria, id),
    )
    return {"mensaje": "Insumo actualizado correctamente", "id": id}, 200


def deleteInsumos(id):
    if not query("SELECT INS_ID FROM T_INSUMOS WHERE INS_ID = %s", (id,)):
        return {"mensaje": "Insumo no encontrado"}, 404
    execute("DELETE FROM T_INSUMOS WHERE INS_ID = %s", (id,))
    return {"mensaje": "Insumo eliminado correctamente"}, 200
