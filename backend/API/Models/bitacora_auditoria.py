class BitacoraAuditoria:

    def __init__(self, AUD_ID, AUD_UUID, AUD_FECHA_HORA, AUD_ACTOR, AUD_CORREO, AUD_ROL, AUD_ACCION, AUD_MODULO, AUD_ENTIDAD, AUD_DETALLE, AUD_RESULTADO):
        self.AUD_ID = AUD_ID
        self.AUD_UUID = AUD_UUID
        self.AUD_FECHA_HORA = AUD_FECHA_HORA
        self.AUD_ACTOR = AUD_ACTOR
        self.AUD_CORREO = AUD_CORREO
        self.AUD_ROL = AUD_ROL
        self.AUD_ACCION = AUD_ACCION
        self.AUD_MODULO = AUD_MODULO
        self.AUD_ENTIDAD = AUD_ENTIDAD
        self.AUD_DETALLE = AUD_DETALLE
        self.AUD_RESULTADO = AUD_RESULTADO

    def to_dic(self):
        return {
            "id": self.AUD_ID,
            "uuid": self.AUD_UUID,
            "fecha_hora": str(self.AUD_FECHA_HORA),
            "actor": self.AUD_ACTOR,
            "correo": self.AUD_CORREO,
            "rol": self.AUD_ROL,
            "accion": self.AUD_ACCION,
            "modulo": self.AUD_MODULO,
            "entidad": self.AUD_ENTIDAD,
            "detalle": self.AUD_DETALLE,
            "resultado": self.AUD_RESULTADO
        }
