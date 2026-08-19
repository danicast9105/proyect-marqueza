class productos:

    def __init__(self,id,uuid, codigo, nombre, cantidad, precio, tipo, unidad_medida, detalles):
        self.PROD_ID                     =   id
        self.PROD_UUID                   =   uuid
        self.PROD_CODIGO                 =   codigo
        self.PROD_NOMBRE                 =   nombre
        self.PROD_CANTIDAD               =   cantidad
        self.PROD_PRECIO                 =   precio
        self.PROD_TIPO_ID                =   tipo
        self.PROD_UND_MEDIDA             =   unidad_medida
        self.PROD_ETC_DET_ETC_ID         =   detalles
        
    # convierte objeto en diccionario 
    def to_dic(self):
        return {
            "id"                     : self.PROD_ID             ,    
            "uuid"                   : self.PROD_UUID           ,   
            "codigo"                 : self.PROD_CODIGO         ,
            "nombre"                 : self.PROD_NOMBRE         , 
            "cantidad"               : self.PROD_CANTIDAD       ,
            "precio"                 : self.PROD_PRECIO         ,
            "tipo"                   : self.PROD_TIPO_ID        ,
            "unidad_medida"          : self.PROD_UND_MEDIDA     ,
            "detalles"               : self.PROD_ETC_DET_ETC_ID            
        }