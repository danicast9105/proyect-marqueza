class Vent_prod:

    def __init__(self, VENTPRO_ID, VENTPRO_UUID, VENTPRO_CANTIDAD, VENTPRO_VENT_ID, VENTPRO_PROD_ID):
        self.VENTPRO_ID = VENTPRO_ID
        self.VENTPRO_UUID = VENTPRO_UUID
        self.VENTPRO_CANTIDAD = VENTPRO_CANTIDAD
        self.VENTPRO_VENT_ID = VENTPRO_VENT_ID
        self.VENTPRO_PROD_ID = VENTPRO_PROD_ID

    def to_dic(self):
        return {
            "id": self.VENTPRO_ID,
            "uuid": self.VENTPRO_UUID,
            "cantidad": self.VENTPRO_CANTIDAD,
            "vent_id": self.VENTPRO_VENT_ID,
            "prod_id": self.VENTPRO_PROD_ID
        }