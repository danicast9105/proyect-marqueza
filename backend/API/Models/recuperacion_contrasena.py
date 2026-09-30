class RecuperacionContrasena:

    def __init__(self, REC_ID, REC_UUID, REC_USUA_ID, REC_CORREO, REC_TOKEN, REC_CREADO_EN, REC_EXPIRA_EN, REC_USADO):
        self.REC_ID = REC_ID
        self.REC_UUID = REC_UUID
        self.REC_USUA_ID = REC_USUA_ID
        self.REC_CORREO = REC_CORREO
        self.REC_TOKEN = REC_TOKEN
        self.REC_CREADO_EN = REC_CREADO_EN
        self.REC_EXPIRA_EN = REC_EXPIRA_EN
        self.REC_USADO = REC_USADO

    def to_dic(self):
        return {
            "id": self.REC_ID,
            "uuid": self.REC_UUID,
            "usua_id": self.REC_USUA_ID,
            "correo": self.REC_CORREO,
            "token": self.REC_TOKEN,
            "creado_en": str(self.REC_CREADO_EN),
            "expira_en": str(self.REC_EXPIRA_EN),
            "usado": self.REC_USADO
        }
