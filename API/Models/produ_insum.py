class Produ_insum:

    def __init__(self, PROINSU_ID, PROINSU_UUID, PROINSU_CANTIDAD, PROINSU_PROD_ID, PROINSU_INS_ID):
        self.PROINSU_ID = PROINSU_ID
        self.PROINSU_UUID = PROINSU_UUID
        self.PROINSU_CANTIDAD = PROINSU_CANTIDAD
        self.PROINSU_PROD_ID = PROINSU_PROD_ID
        self.PROINSU_INS_ID = PROINSU_INS_ID

    def to_dic(self):
        return {
            "id": self.PROINSU_ID,
            "uuid": self.PROINSU_UUID,
            "cantidad": self.PROINSU_CANTIDAD,
            "prod_id": self.PROINSU_PROD_ID,
            "ins_id": self.PROINSU_INS_ID
        }