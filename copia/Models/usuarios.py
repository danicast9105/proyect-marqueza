class Usuarios:

    def __init__(self, USUA_ID, USUA_UUID, USUA_NOMBRE, USUA_CORREO, USUA_CONTRASENA, USUA_ESTADO, USUA_DET_ETC_ID):
        self.USUA_ID = USUA_ID
        self.USUA_UUID = USUA_UUID
        self.USUA_NOMBRE = USUA_NOMBRE
        self.USUA_CORREO = USUA_CORREO
        self.USUA_CONTRASENA = USUA_CONTRASENA
        self.USUA_ESTADO = USUA_ESTADO
        self.USUA_DET_ETC_ID = USUA_DET_ETC_ID

    def to_dic(self):
        return {
            "id": self.USUA_ID,
            "uuid": self.USUA_UUID,
            "nombre": self.USUA_NOMBRE,
            "correo": self.USUA_CORREO,
            "contrasena": self.USUA_CONTRASENA,
            "estado": self.USUA_ESTADO,
            "det_etc_id": self.USUA_DET_ETC_ID
        }