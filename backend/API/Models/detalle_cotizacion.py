class DetalleCotizacion:

    def __init__(self, DETCOT_ID, DETCOT_UUID, DETCOT_COT_ID, DETCOT_PROD_ID, DETCOT_CODIGO, DETCOT_NOMBRE, DETCOT_CANTIDAD, DETCOT_PRECIO_UNITARIO, DETCOT_SUBTOTAL):
        self.DETCOT_ID = DETCOT_ID
        self.DETCOT_UUID = DETCOT_UUID
        self.DETCOT_COT_ID = DETCOT_COT_ID
        self.DETCOT_PROD_ID = DETCOT_PROD_ID
        self.DETCOT_CODIGO = DETCOT_CODIGO
        self.DETCOT_NOMBRE = DETCOT_NOMBRE
        self.DETCOT_CANTIDAD = DETCOT_CANTIDAD
        self.DETCOT_PRECIO_UNITARIO = DETCOT_PRECIO_UNITARIO
        self.DETCOT_SUBTOTAL = DETCOT_SUBTOTAL

    def to_dic(self):
        return {
            "id": self.DETCOT_ID,
            "uuid": self.DETCOT_UUID,
            "cot_id": self.DETCOT_COT_ID,
            "prod_id": self.DETCOT_PROD_ID,
            "codigo": self.DETCOT_CODIGO,
            "nombre": self.DETCOT_NOMBRE,
            "cantidad": self.DETCOT_CANTIDAD,
            "precio_unitario": self.DETCOT_PRECIO_UNITARIO,
            "subtotal": self.DETCOT_SUBTOTAL
        }
