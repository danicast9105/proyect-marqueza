class Detalles_etc:

    def __init__(self, DET_ETC_ID, DET_ETC_UUID, DET_ETC_NOMBRE, DET_ETC_ETC_ID, DET_ETC_PER_ID):
        self.DET_ETC_ID = DET_ETC_ID
        self.DET_ETC_UUID = DET_ETC_UUID
        self.DET_ETC_NOMBRE = DET_ETC_NOMBRE
        self.DET_ETC_ETC_ID = DET_ETC_ETC_ID
        self.DET_ETC_PER_ID = DET_ETC_PER_ID

    def to_dic(self):
        return {
            "id": self.DET_ETC_ID,
            "uuid": self.DET_ETC_UUID,
            "nombre": self.DET_ETC_NOMBRE,
            "etc_id": self.DET_ETC_ETC_ID,
            "per_id": self.DET_ETC_PER_ID
        }