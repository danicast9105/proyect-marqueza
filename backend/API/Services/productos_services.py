import re
import uuid as uuid_lib

from flask import current_app
from Services.helpers import (clean, execute, new_uuid, query,
                              resolve_categoria, serialize_rows)
from Services.validation import non_negative_number, optional_id

_PRODUCT_CODE_LOCK = "marqueza_product_code_sequence"


def _next_product_code(codes):
    numbers = [
        int(match.group(1))
        for code in codes
        if (match := re.fullmatch(r"P(\d+)", str(code or ""), re.IGNORECASE))
    ]
    return f"P{max(numbers, default=0) + 1:03d}"


def _compact_product_codes(cursor, products):
    for product_id, _ in products:
        cursor.execute(
            "UPDATE T_PRODUCTOS SET PROD_CODIGO = %s WHERE PROD_ID = %s",
            (f"TMP-{uuid_lib.uuid4().hex}", product_id),
        )
    for index, (product_id, _) in enumerate(products, start=1):
        cursor.execute(
            "UPDATE T_PRODUCTOS SET PROD_CODIGO = %s WHERE PROD_ID = %s",
            (f"P{index:03d}", product_id),
        )


def _acquire_product_code_lock(cursor):
    cursor.execute("SELECT GET_LOCK(%s, 10)", (_PRODUCT_CODE_LOCK,))
    result = cursor.fetchone()
    return bool(result and result[0] == 1)


def _release_product_code_lock(cursor):
    cursor.execute("SELECT RELEASE_LOCK(%s)", (_PRODUCT_CODE_LOCK,))


def servListProductos(id=None):
    rows = query(
        """SELECT id, uuid, codigo, nombre, cantidad, precio, valor_inventario,
                  estado, categoria, nivel_stock, clase_badge
           FROM V_CATALOGO_PRODUCTOS
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
        cantidad = int(float(data.get("cantidad") or 0))
    except (TypeError, ValueError):
        cantidad = 0
    try:
        precio = float(data.get("precio") or 0)
    except (TypeError, ValueError):
        precio = 0.0
    estado = clean(data.get("estado"), "Activo")
    if estado not in ("Activo", "Inactivo"):
        estado = "Activo"
    categoria = resolve_categoria(clean(data.get("categoria"), "General"), "CATEGORIAS_PRODUCTOS")
    return codigo, nombre, cantidad, precio, estado, categoria


def addProductos(data):
    if data.get("estado") not in (None, "", "Activo", "Inactivo"):
        return {"mensaje": "El estado del producto no es valido"}, 400
    for field, integer in (("cantidad", True), ("precio", False)):
        value = data.get(field)
        if value not in (None, ""):
            _, error, status = non_negative_number(value, field, integer=integer)
            if error:
                return error, status
    user_id, error = optional_id(data.get("usua_id"), "usua_id")
    if error:
        return error
    if user_id is not None and not query(
        "SELECT USUA_ID FROM T_USUARIOS WHERE USUA_ID = %s", (user_id,)
    ):
        return {"mensaje": "Usuario no encontrado"}, 404
    _, nombre, cantidad, precio, estado, categoria = _payload(data)
    if not nombre:
        return {"mensaje": "El nombre es obligatorio"}, 400

    connection = current_app.mysql.connection
    cursor = connection.cursor()
    lock_acquired = False
    try:
        lock_acquired = _acquire_product_code_lock(cursor)
        if not lock_acquired:
            return {"mensaje": "No se pudo reservar un código de producto; inténtalo de nuevo"}, 503
        cursor.execute("SELECT PROD_CODIGO FROM T_PRODUCTOS ORDER BY PROD_ID FOR UPDATE")
        codes = [row[0] for row in cursor.fetchall()]
        codigo = _next_product_code(codes)
        cursor.execute(
            """INSERT INTO T_PRODUCTOS
               (PROD_UUID, PROD_CODIGO, PROD_NOMBRE, PROD_CANTIDAD, PROD_PRECIO,
                PROD_ESTADO, PROD_USUA_ID, PROD_DET_ETC_ID)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (new_uuid(), codigo, nombre, cantidad, precio, estado,
             user_id, categoria),
        )
        prod_id = cursor.lastrowid
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        if lock_acquired:
            _release_product_code_lock(cursor)
        cursor.close()
    return {"mensaje": "Producto agregado correctamente", "id": prod_id}, 201


def updateProductos(id, data):
    existente = query("SELECT PROD_ID, PROD_CODIGO FROM T_PRODUCTOS WHERE PROD_ID = %s", (id,))
    if not existente:
        return {"mensaje": "Producto no encontrado"}, 404

    if data.get("estado") not in (None, "", "Activo", "Inactivo"):
        return {"mensaje": "El estado del producto no es valido"}, 400
    for field, integer in (("cantidad", True), ("precio", False)):
        value = data.get(field)
        if value not in (None, ""):
            _, error, status = non_negative_number(value, field, integer=integer)
            if error:
                return error, status
    _, nombre, cantidad, precio, estado, categoria = _payload(data)
    if not nombre:
        return {"mensaje": "El nombre es obligatorio"}, 400

    execute(
        """UPDATE T_PRODUCTOS SET PROD_NOMBRE = %s, PROD_CANTIDAD = %s,
           PROD_PRECIO = %s, PROD_ESTADO = %s, PROD_DET_ETC_ID = %s
           WHERE PROD_ID = %s""",
        (nombre, cantidad, precio, estado, categoria, id),
    )
    return {"mensaje": "Producto actualizado correctamente", "id": id}, 200


def deleteProductos(id):
    connection = current_app.mysql.connection
    cursor = connection.cursor()
    lock_acquired = False
    try:
        lock_acquired = _acquire_product_code_lock(cursor)
        if not lock_acquired:
            return {"mensaje": "No se pudo reservar la secuencia de códigos; inténtalo de nuevo"}, 503
        cursor.execute("SELECT PROD_ID FROM T_PRODUCTOS WHERE PROD_ID = %s FOR UPDATE", (id,))
        if not cursor.fetchone():
            connection.rollback()
            return {"mensaje": "Producto no encontrado"}, 404
        cursor.execute("DELETE FROM T_PRODUCTOS WHERE PROD_ID = %s", (id,))
        cursor.execute("SELECT PROD_ID, PROD_CODIGO FROM T_PRODUCTOS ORDER BY PROD_ID FOR UPDATE")
        products = cursor.fetchall()
        _compact_product_codes(cursor, products)
        connection.commit()
    except Exception:
        connection.rollback()
        return {"mensaje": "No se puede eliminar: el producto tiene ventas o cotizaciones asociadas"}, 409
    finally:
        if lock_acquired:
            _release_product_code_lock(cursor)
        cursor.close()
    return {"mensaje": "Producto eliminado correctamente"}, 200
