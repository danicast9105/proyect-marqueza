class Produ_insum:

    def __init__(self, PRODINSU_ID, PRODINSU_UUID, PRODINSU_CANTIDAD, PRODINSU_PROD_ID, PRODINSU_INS_ID):
        self.PRODINSU_ID = PRODINSU_ID
        self.PRODINSU_UUID = PRODINSU_UUID
        self.PRODINSU_CANTIDAD = PRODINSU_CANTIDAD
        self.PRODINSU_PROD_ID = PRODINSU_PROD_ID
        self.PRODINSU_INS_ID = PRODINSU_INS_ID

    def to_dic(self):
        return {
            "id": self.PRODINSU_ID,
            "uuid": self.PRODINSU_UUID,
            "cantidad": self.PRODINSU_CANTIDAD,
            "prod_id": self.PRODINSU_PROD_ID,
            "ins_id": self.PRODINSU_INS_ID
        }