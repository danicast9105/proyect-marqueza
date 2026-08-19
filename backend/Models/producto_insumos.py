class insumo_insumos:

    def __init__(self,id,uuid, cantidad, producto, insumo):
        self.PROINSU_ID                   =   id
        self.PROINSU_UUID                 =   uuid
        self.PROINSU_CANTIDAD             =   cantidad
        self.PROINSU_PROD_ID              =   producto
        self.PROINSU_INS_ID               =   insumo
        
    # convierte objeto en diccionario 
    def to_dic(self):
        return {
            "id"                        : self.PROINSU_ID           ,    
            "uuid"                      : self.PROINSU_UUID         ,   
            "cantidad"                  : self.PROINSU_CANTIDAD     ,
            "producto"                  : self.PROINSU_PROD_ID      , 
            "insumo"                    : self.PROINSU_INS_ID            
        }