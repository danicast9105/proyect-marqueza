class detalles_etc:

    def __init__(self,id,uuid, nombre, etc):
        self.DET_ETC_ID                   =   id
        self.DET_ETC_UUID                 =   uuid
        self.DET_ETC_NOMBRE               =   nombre
        self.DET_ETC_DET_ETC_ID           =   etc
                
    # convierte objeto en diccionario 
    def to_dic(self):
        return {
            "id"                        : self.DET_ETC_ID           ,    
            "uuid"                      : self.DET_ETC_UUID         ,   
            "nombre"                    : self.DET_ETC_NOMBRE       ,
            "etc"                       : self.DET_ETC_DET_ETC_ID          
        }