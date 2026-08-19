class ventas:

    def __init__(self,id,uuid, producto_codigo, producto_nombre, usuario, cliente):
        self.VENT_ID                 =   id
        self.VENT_UUID               =   uuid
        self.VENT_PRO_CODIGO         =   producto_codigo
        self.VENT_PRO_NOMBRE         =   producto_nombre
        self.VENT_USUA_ID            =   usuario
        self.VENT_CLI_ID             =   cliente

    # convierte objeto en diccionario 
    def to_dic(self):
        return {
            "id"                    : self.VENT_ID             ,    
            "uuid"                  : self.VENT_UUID           ,   
            "producto_codigo"       : self.VENT_PRO_CODIGO     ,
            "producto_nombre"       : self.VENT_PRO_NOMBRE      , 
            "usuario"               : self.VENT_USUA_ID       ,
            "cliente"               : self.VENT_CLI_ID
        }