class Cotizaciones:

    def __init__(self, COT_ID, COT_UUID, COT_FECHA, COT_TOTAL_PAGAR, COT_ESTADO, COT_NOTAS, COT_USUA_ID, COT_CLI_ID, COT_PRO_CODIGO, COT_PRO_NOMBRE, COT_PRO_CANTIDAD, COT_PRO_PRECIO):
        self.COT_ID = COT_ID
        self.COT_UUID = COT_UUID
        self.COT_FECHA = COT_FECHA
        self.COT_TOTAL_PAGAR = COT_TOTAL_PAGAR
        self.COT_ESTADO = COT_ESTADO
        self.COT_NOTAS = COT_NOTAS
        self.COT_USUA_ID = COT_USUA_ID
        self.COT_CLI_ID = COT_CLI_ID
        self.COT_PRO_CODIGO = COT_PRO_CODIGO
        self.COT_PRO_NOMBRE = COT_PRO_NOMBRE
        self.COT_PRO_CANTIDAD = COT_PRO_CANTIDAD
        self.COT_PRO_PRECIO = COT_PRO_PRECIO

    def to_dic(self):
        return {
            "id": self.COT_ID,
            "uuid": self.COT_UUID,
            "fecha": self.COT_FECHA,
            "total_pagar": self.COT_TOTAL_PAGAR,
            "estado": self.COT_ESTADO,
            "notas": self.COT_NOTAS,
            "usua_id": self.COT_USUA_ID,
            "cli_id": self.COT_CLI_ID,
            "pro_codigo": self.COT_PRO_CODIGO,
            "pro_nombre": self.COT_PRO_NOMBRE,
            "pro_cantidad": self.COT_PRO_CANTIDAD,
            "pro_precio": self.COT_PRO_PRECIO
        }
