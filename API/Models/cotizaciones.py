class Cotizaciones:

    def __init__(self, COT_ID, COT_UUID, COT_PRO_CODIGO, COT_PRO_NOMBRE, COT_PRO_CANTIDAD, COT_PRO_PRECIO, COT_TOTAL_PAGAR, COT_USUA_ID, COT_CLI_ID):
        self.COT_ID = COT_ID
        self.COT_UUID = COT_UUID
        self.COT_PRO_CODIGO = COT_PRO_CODIGO
        self.COT_PRO_NOMBRE = COT_PRO_NOMBRE
        self.COT_PRO_CANTIDAD = COT_PRO_CANTIDAD
        self.COT_PRO_PRECIO = COT_PRO_PRECIO
        self.COT_TOTAL_PAGAR = COT_TOTAL_PAGAR
        self.COT_USUA_ID = COT_USUA_ID
        self.COT_CLI_ID = COT_CLI_ID

    def to_dic(self):
        return {
            "id": self.COT_ID,
            "uuid": self.COT_UUID,
            "pro_codigo": self.COT_PRO_CODIGO,
            "pro_nombre": self.COT_PRO_NOMBRE,
            "cantidad": self.COT_PRO_CANTIDAD,
            "precio": self.COT_PRO_PRECIO,
            "total_pagar": self.COT_TOTAL_PAGAR,
            "usua_id": self.COT_USUA_ID,
            "cli_id": self.COT_CLI_ID
        }