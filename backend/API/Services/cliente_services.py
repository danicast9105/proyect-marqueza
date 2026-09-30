from Services.helpers import (clean, execute, new_uuid, query, scalar,
                              serialize_rows, unique_identificacion)


class cliente_services:
    @staticmethod
    def servListCliente():
        rows = query(
            """SELECT id, nombre, documento, telefono, correo, direccion, estado
               FROM v_clientes_completo
               ORDER BY nombre"""
        )
        return serialize_rows(rows)

    @staticmethod
    def _split_nombre(nombre):
        partes = (nombre or "").split(None, 1)
        return partes[0] if partes else "Cliente", (partes[1] if len(partes) > 1 else "")

    @staticmethod
    def addCliente(data):
        nombre = clean(data.get("nombre"))
        documento = clean(data.get("documento"), "")
        telefono = clean(data.get("telefono"), "")
        correo = clean(data.get("correo"), "")
        direccion = clean(data.get("direccion"), "")

        if not nombre:
            return {"mensaje": "El nombre es obligatorio"}, 400

        existente = scalar(
            "SELECT id FROM v_clientes_completo WHERE documento = %s LIMIT 1",
            (documento,),
        )
        if existente and documento:
            return {"mensaje": "Ya existe un cliente con ese documento", "id": existente}, 409

        base_nombre, resto = cliente_services._split_nombre(nombre)

        per_id = None
        if documento:
            per_id = scalar("SELECT PER_ID FROM t_persona WHERE PER_IDENTIFICACION = %s LIMIT 1", (documento,))
        if per_id is None:
            per_id = execute(
                """INSERT INTO t_persona
                   (PER_UUID, PER_NOMBRE, PER_SEG_NOMBRE, PER_PRI_APELLIDO, PER_SEG_APELLIDO,
                    PER_CORREO, PER_DIRECCION, PER_IDENTIFICACION, PER_TELEFONO)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (new_uuid(), base_nombre, "", resto, "", correo, direccion,
                 unique_identificacion(documento), telefono),
            )
        else:
            execute(
                """UPDATE t_persona SET PER_NOMBRE = %s, PER_PRI_APELLIDO = %s,
                   PER_TELEFONO = %s, PER_CORREO = %s, PER_DIRECCION = %s
                   WHERE PER_ID = %s""",
                (base_nombre, resto, telefono, correo, direccion, per_id),
            )

        cli_id = execute(
            "INSERT INTO t_cliente (CLI_UUID, CLI_PER_ID) VALUES (%s, %s)",
            (new_uuid(), per_id),
        )
        return {"mensaje": "Cliente agregado correctamente", "id": cli_id}, 201

    @staticmethod
    def updateCliente(id, data):
        nombre = clean(data.get("nombre"))
        documento = clean(data.get("documento"), "")
        telefono = clean(data.get("telefono"), "")
        correo = clean(data.get("correo"), "")
        direccion = clean(data.get("direccion"), "")

        fila = query(
            """SELECT c.CLI_ID, c.CLI_PER_ID, p.PER_IDENTIFICACION
               FROM t_cliente c
               JOIN t_persona p ON p.PER_ID = c.CLI_PER_ID
               WHERE c.CLI_ID = %s""",
            (id,),
        )
        if not fila:
            return {"mensaje": "Cliente no encontrado"}, 404
        per_id = fila[0]["CLI_PER_ID"]
        identificacion = documento or fila[0]["PER_IDENTIFICACION"]

        base_nombre, resto = cliente_services._split_nombre(nombre or "")
        try:
            execute(
                """UPDATE t_persona SET PER_NOMBRE = %s, PER_PRI_APELLIDO = %s,
                   PER_IDENTIFICACION = %s, PER_TELEFONO = %s, PER_CORREO = %s, PER_DIRECCION = %s
                   WHERE PER_ID = %s""",
                (base_nombre, resto, identificacion, telefono, correo, direccion, per_id),
            )
        except Exception:
            return {"mensaje": "Ya existe otro cliente con ese documento"}, 409
        return {"mensaje": "Cliente actualizado correctamente", "id": id}, 200

    @staticmethod
    def deleteCliente(id):
        existente = query("SELECT CLI_ID FROM t_cliente WHERE CLI_ID = %s", (id,))
        if not existente:
            return {"mensaje": "Cliente no encontrado"}, 404
        try:
            execute("DELETE FROM t_cliente WHERE CLI_ID = %s", (id,))
        except Exception:
            return {"mensaje": "No se puede eliminar: el cliente tiene ventas o cotizaciones asociadas"}, 409
        return {"mensaje": "Cliente eliminado correctamente"}, 200
