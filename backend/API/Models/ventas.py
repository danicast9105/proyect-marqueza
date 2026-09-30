class Ventas:

    def __init__(self, VENT_ID, VENT_UUID, VENT_FECHA, VENT_TOTAL, VENT_ESTADO, VENT_USUA_ID, VENT_CLI_ID, VENT_OBSERVACIONES):
        self.VENT_ID = VENT_ID
        self.VENT_UUID = VENT_UUID
        self.VENT_FECHA = VENT_FECHA
        self.VENT_TOTAL = VENT_TOTAL
        self.VENT_ESTADO = VENT_ESTADO
        self.VENT_USUA_ID = VENT_USUA_ID
        self.VENT_CLI_ID = VENT_CLI_ID
        self.VENT_OBSERVACIONES = VENT_OBSERVACIONES

    def to_dic(self):
        return {
            "id": self.VENT_ID,
            "uuid": self.VENT_UUID,
            "fecha": self.VENT_FECHA,
            "total": self.VENT_TOTAL,
            "estado": self.VENT_ESTADO,
            "usua_id": self.VENT_USUA_ID,
            "cli_id": self.VENT_CLI_ID,
            "observaciones": self.VENT_OBSERVACIONES
        }
