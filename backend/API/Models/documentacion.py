class Documentacion:

    def __init__(self, DOC_ID, DOC_UUID, DOC_TIPO, DOC_TITULO, DOC_DESCRIPCION, DOC_RUTA, DOC_ACTIVO):
        self.DOC_ID = DOC_ID
        self.DOC_UUID = DOC_UUID
        self.DOC_TIPO = DOC_TIPO
        self.DOC_TITULO = DOC_TITULO
        self.DOC_DESCRIPCION = DOC_DESCRIPCION
        self.DOC_RUTA = DOC_RUTA
        self.DOC_ACTIVO = DOC_ACTIVO

    def to_dic(self):
        return {
            "id": self.DOC_ID,
            "uuid": self.DOC_UUID,
            "tipo": self.DOC_TIPO,
            "titulo": self.DOC_TITULO,
            "descripcion": self.DOC_DESCRIPCION,
            "ruta": self.DOC_RUTA,
            "activo": self.DOC_ACTIVO
        }
