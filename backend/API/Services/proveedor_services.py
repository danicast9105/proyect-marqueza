from Services.helpers import (clean, execute, new_uuid, query,
                              serialize_rows, unique_identificacion)


def servListProveedor():
    rows = query(
        """SELECT id, uuid, empresa, contacto, telefono, correo, direccion, estado
           FROM v_proveedores_completo
           ORDER BY empresa"""
    )
    return serialize_rows(rows)


def _split_nombre(nombre):
    partes = (nombre or "").split(None, 1)
    return partes[0] if partes else "Contacto", (partes[1] if len(partes) > 1 else "")


def addProveedor(data):
    empresa = clean(data.get("empresa"))
    if not empresa:
        return {"mensaje": "El nombre de la empresa es obligatorio"}, 400

    contacto = clean(data.get("contacto"))
    telefono = clean(data.get("telefono"), "")
    correo = clean(data.get("correo"), "")
    direccion = clean(data.get("direccion"), "")

    if query("SELECT PROV_ID FROM t_proveedores WHERE PROV_EMPRESA = %s", (empresa,)):
        return {"mensaje": "Ya existe un proveedor con esa empresa"}, 409

    per_id = None
    if contacto:
        base, resto = _split_nombre(contacto)
        per_id = execute(
            """INSERT INTO t_persona (PER_UUID, PER_NOMBRE, PER_SEG_NOMBRE, PER_PRI_APELLIDO,
                                      PER_CORREO, PER_DIRECCION, PER_IDENTIFICACION, PER_TELEFONO)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (new_uuid(), base, "", resto, correo, direccion, unique_identificacion(), telefono),
        )

    prov_id = execute(
        """INSERT INTO t_proveedores
           (PROV_UUID, PROV_EMPRESA, PROV_PER_ID, PROV_DIRECCION, PROV_TELEFONO, PROV_CORREO)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (new_uuid(), empresa, per_id, direccion, telefono, correo),
    )
    return {"mensaje": "Proveedor agregado correctamente", "id": prov_id}, 201


def updateProveedor(id, data):
    fila = query("SELECT PROV_ID, PROV_PER_ID FROM t_proveedores WHERE PROV_ID = %s", (id,))
    if not fila:
        return {"mensaje": "Proveedor no encontrado"}, 404

    empresa = clean(data.get("empresa"))
    if not empresa:
        return {"mensaje": "El nombre de la empresa es obligatorio"}, 400
    if query("SELECT PROV_ID FROM t_proveedores WHERE PROV_EMPRESA = %s AND PROV_ID <> %s", (empresa, id)):
        return {"mensaje": "Ya existe otro proveedor con esa empresa"}, 409

    contacto = clean(data.get("contacto"))
    telefono = clean(data.get("telefono"), "")
    correo = clean(data.get("correo"), "")
    direccion = clean(data.get("direccion"), "")

    per_id = fila[0]["PROV_PER_ID"]
    if contacto:
        if per_id:
            base, resto = _split_nombre(contacto)
            execute(
                """UPDATE t_persona SET PER_NOMBRE = %s, PER_PRI_APELLIDO = %s,
                   PER_TELEFONO = %s, PER_CORREO = %s, PER_DIRECCION = %s
                   WHERE PER_ID = %s""",
                (base, resto, telefono, correo, direccion, per_id),
            )
        else:
            base, resto = _split_nombre(contacto)
            per_id = execute(
                """INSERT INTO t_persona (PER_UUID, PER_NOMBRE, PER_SEG_NOMBRE, PER_PRI_APELLIDO,
                                          PER_CORREO, PER_DIRECCION, PER_IDENTIFICACION, PER_TELEFONO)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (new_uuid(), base, "", resto, correo, direccion, unique_identificacion(), telefono),
            )

    execute(
        """UPDATE t_proveedores SET PROV_EMPRESA = %s, PROV_PER_ID = %s, PROV_DIRECCION = %s,
           PROV_TELEFONO = %s, PROV_CORREO = %s
           WHERE PROV_ID = %s""",
        (empresa, per_id, direccion, telefono, correo, id),
    )
    return {"mensaje": "Proveedor actualizado correctamente", "id": id}, 200


def deleteProveedor(id):
    if not query("SELECT PROV_ID FROM t_proveedores WHERE PROV_ID = %s", (id,)):
        return {"mensaje": "Proveedor no encontrado"}, 404
    try:
        execute("DELETE FROM t_proveedores WHERE PROV_ID = %s", (id,))
    except Exception:
        return {"mensaje": "No se puede eliminar el proveedor"}, 409
    return {"mensaje": "Proveedor eliminado correctamente"}, 200
