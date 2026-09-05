class Ventas:

    def __init__(self, VENT_ID, VENT_UUID, VENT_PRO_CODIGO, VENT_PRO_NOMBRE, VENT_USUA_ID, VENT_CLI_ID):
        self.VENT_ID = VENT_ID
        self.VENT_UUID = VENT_UUID
        self.VENT_PRO_CODIGO = VENT_PRO_CODIGO
        self.VENT_PRO_NOMBRE = VENT_PRO_NOMBRE
        self.VENT_USUA_ID = VENT_USUA_ID
        self.VENT_CLI_ID = VENT_CLI_ID

    def to_dic(self):
        return {
            "id": self.VENT_ID,
            "uuid": self.VENT_UUID,
            "pro_codigo": self.VENT_PRO_CODIGO,
            "pro_nombre": self.VENT_PRO_NOMBRE,
            "usua_id": self.VENT_USUA_ID,
            "cli_id": self.VENT_CLI_ID
        }