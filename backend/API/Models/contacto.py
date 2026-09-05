class Contacto:

    def __init__(self, CONT_ID, CONT_UUID, CONT_TIPO_DATO, CONT_CONTENIDO, CONT_PROV_ID):
        self.CONT_ID = CONT_ID
        self.CONT_UUID = CONT_UUID
        self.CONT_TIPO_DATO = CONT_TIPO_DATO
        self.CONT_CONTENIDO = CONT_CONTENIDO
        self.CONT_PROV_ID = CONT_PROV_ID

    def to_dic(self):
        return {
            "id": self.CONT_ID,
            "uuid": self.CONT_UUID,
            "tipo_dato": self.CONT_TIPO_DATO,
            "contenido": self.CONT_CONTENIDO,
            "prov_id": self.CONT_PROV_ID
        }