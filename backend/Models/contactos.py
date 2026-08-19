class contactos:

    def __init__(self,id,uuid, tipo_dato, contenido, proveedor):
        self.CONT_ID                   =   id
        self.CONT_UUID                 =   uuid
        self.CONT_TIPO_DATO            =   tipo_dato
        self.CONT_CONTENIDO            =   contenido
        self.CONT_PROV_ID              =   proveedor
        
    # convierte objeto en diccionario 
    def to_dic(self):
        return {
            "id"                        : self.CONT_ID           ,    
            "uuid"                      : self.CONT_UUID         ,   
            "tipo_dato"                 : self.CONT_TIPO_DATO     ,
            "contenido"                 : self.CONT_CONTENIDO      , 
            "proveedor"                 : self.CONT_PROV_ID            
        }