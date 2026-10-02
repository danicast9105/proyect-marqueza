import uuid as uuid_lib

from Services.helpers import clean, query, serialize_rows


class documentacion_services:
    """La tabla T_DOCUMENTACION no existe en marqueza_db: la API responde vacio."""

    TABLA_EXISTE = None

    @staticmethod
    def _tabla_disponible():
        if documentacion_services.TABLA_EXISTE is None:
            try:
                query("SELECT 1 FROM T_DOCUMENTACION LIMIT 1")
                documentacion_services.TABLA_EXISTE = True
            except Exception:
                documentacion_services.TABLA_EXISTE = False
        return documentacion_services.TABLA_EXISTE

    @staticmethod
    def servListDocumentacion(id=None):
        if not documentacion_services._tabla_disponible():
            return []
        rows = query(
            """SELECT DOC_ID AS id, DOC_UUID AS uuid, DOC_TIPO AS tipo,
                      DOC_TITULO AS titulo, DOC_DESCRIPCION AS descripcion,
                      DOC_RUTA AS ruta, DOC_ACTIVO AS activo
               FROM T_DOCUMENTACION
               {where}
               ORDER BY DOC_ID DESC""".format(
                where="WHERE DOC_ID = %s" if id is not None else ""
            ),
            (id,) if id is not None else (),
        )
        return serialize_rows(rows)

    @staticmethod
    def addDocumentacion(tipo, titulo, descripcion, ruta, activo=True):
        if not documentacion_services._tabla_disponible():
            return {"mensaje": "El modulo de documentacion no esta disponible"}, 503
        if not all(isinstance(value, str) and value.strip() for value in (tipo, titulo, ruta)):
            return {"mensaje": "Los campos tipo, titulo y ruta son obligatorios"}, 400
        if not isinstance(activo, bool):
            return {"mensaje": "El campo activo debe ser booleano"}, 400
        execute_sql = (
            "INSERT INTO T_DOCUMENTACION "
            "(DOC_UUID, DOC_TIPO, DOC_TITULO, DOC_DESCRIPCION, DOC_RUTA, DOC_ACTIVO) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        from Services.helpers import execute
        execute(execute_sql, (str(uuid_lib.uuid4()), tipo, titulo, descripcion, ruta, 1 if activo else 0))
        return {"mensaje": "Documentacion agregada correctamente"}, 201

    @staticmethod
    def deleteDocumentacion(id):
        if not documentacion_services._tabla_disponible():
            return {"mensaje": "El modulo de documentacion no esta disponible"}, 503
        if not query("SELECT DOC_ID FROM T_DOCUMENTACION WHERE DOC_ID = %s", (id,)):
            return {"mensaje": "Documentacion no encontrada"}, 404
        from Services.helpers import execute
        execute("DELETE FROM T_DOCUMENTACION WHERE DOC_ID = %s", (id,))
        return {"mensaje": "Documentacion eliminada correctamente"}, 200

    @staticmethod
    def updateDocumentacion(id, tipo, titulo, descripcion, ruta, activo):
        if not documentacion_services._tabla_disponible():
            return {"mensaje": "El modulo de documentacion no esta disponible"}, 503
        if not query("SELECT DOC_ID FROM T_DOCUMENTACION WHERE DOC_ID = %s", (id,)):
            return {"mensaje": "Documentacion no encontrada"}, 404
        if not all(isinstance(value, str) and value.strip() for value in (tipo, titulo, ruta)):
            return {"mensaje": "Los campos tipo, titulo y ruta son obligatorios"}, 400
        if not isinstance(activo, bool):
            return {"mensaje": "El campo activo debe ser booleano"}, 400
        from Services.helpers import execute
        execute(
            "UPDATE T_DOCUMENTACION SET DOC_TIPO=%s, DOC_TITULO=%s, DOC_DESCRIPCION=%s, "
            "DOC_RUTA=%s, DOC_ACTIVO=%s WHERE DOC_ID=%s",
            (tipo, titulo, descripcion, ruta, 1 if activo else 0, id),
        )
        return {"mensaje": "Documentacion actualizada correctamente"}, 200
