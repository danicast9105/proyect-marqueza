class Insumos:

    def __init__(self, INS_ID, INS_UUID, INS_CODIGO, INS_NOMBRE, INS_CANTIDAD, INS_PRECIO, INS_ESTADO, INS_USUA_ID, INS_DET_ETC_ID, INS_PROV_ID):
        self.INS_ID = INS_ID
        self.INS_UUID = INS_UUID
        self.INS_CODIGO = INS_CODIGO
        self.INS_NOMBRE = INS_NOMBRE
        self.INS_CANTIDAD = INS_CANTIDAD
        self.INS_PRECIO = INS_PRECIO
        self.INS_ESTADO = INS_ESTADO
        self.INS_USUA_ID = INS_USUA_ID
        self.INS_DET_ETC_ID = INS_DET_ETC_ID
        self.INS_PROV_ID = INS_PROV_ID

    def to_dic(self):
        return {
            "id": self.INS_ID,
            "uuid": self.INS_UUID,
            "codigo": self.INS_CODIGO,
            "nombre": self.INS_NOMBRE,
            "cantidad": self.INS_CANTIDAD,
            "precio": self.INS_PRECIO,
            "estado": self.INS_ESTADO,
            "usua_id": self.INS_USUA_ID,
            "det_etc_id": self.INS_DET_ETC_ID,
            "prov_id": self.INS_PROV_ID
        }