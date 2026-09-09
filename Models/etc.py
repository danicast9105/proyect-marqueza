class ETC:

    def __init__(self, ETC_ID, ETC_UUID, ETC_NOMBRE):
        self.ETC_ID = ETC_ID
        self.ETC_UUID = ETC_UUID
        self.ETC_NOMBRE = ETC_NOMBRE

    def to_dic(self):
        return {
            "id": self.ETC_ID,
            "uuid": self.ETC_UUID,
            "nombre": self.ETC_NOMBRE
        }