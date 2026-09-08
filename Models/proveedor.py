class Proveedor:

    def __init__(self, PROV_ID, PROV_UUID, PROV_PER_ID):
        self.PROV_ID = PROV_ID
        self.PROV_UUID = PROV_UUID
        self.PROV_PER_ID = PROV_PER_ID

    def to_dic(self):
        return {
            "id": self.PROV_ID,
            "uuid": self.PROV_UUID,
            "per_id": self.PROV_PER_ID
        }