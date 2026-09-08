class Productos:

    def __init__(self, PROD_ID, PROD_UUID, PROD_CODIGO, PROD_NOMBRE, PROD_CANTIDAD, PROD_PRECIO, PROD_ESTADO, PROD_USUA_ID, PROD_DET_ETC_ID):
        self.PROD_ID = PROD_ID
        self.PROD_UUID = PROD_UUID
        self.PROD_CODIGO = PROD_CODIGO
        self.PROD_NOMBRE = PROD_NOMBRE
        self.PROD_CANTIDAD = PROD_CANTIDAD
        self.PROD_PRECIO = PROD_PRECIO
        self.PROD_ESTADO = PROD_ESTADO
        self.PROD_USUA_ID = PROD_USUA_ID
        self.PROD_DET_ETC_ID = PROD_DET_ETC_ID

    def to_dic(self):
        return {
            "id": self.PROD_ID,
            "uuid": self.PROD_UUID,
            "codigo": self.PROD_CODIGO,
            "nombre": self.PROD_NOMBRE,
            "cantidad": self.PROD_CANTIDAD,
            "precio": self.PROD_PRECIO,
            "estado": self.PROD_ESTADO,
            "usua_id": self.PROD_USUA_ID,
            "det_etc_id": self.PROD_DET_ETC_ID
        }