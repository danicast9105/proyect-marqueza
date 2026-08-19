from typing import Self


class usuarios:

    def __init__(self,id,uuid, nombre, identificacion, correo, password, rol):
        self.USUA_ID                     =   id
        self.USUA_UUID                   =   uuid
        Self.USUA_NOMBRE                 =   nombre
        self.USUA_NUM_IDENTIFICACION     =   identificacion
        self.USUA_CORREO_ELECT           =   correo
        self.USUA_PASSWORD               =   password
        self.USUA_ROL_ID                 =   rol

    # convierte objeto en diccionario 
    def to_dic(self):
        return {
            "id"                        : self.USUA_ID             ,    
            "uuid"                      : self.USUA_UUID           ,
            "nombre"                    : self.USUA_NOMBRE         ,   
            "identificacion"            : self.USUA_NUM_IDENTIFICACION     ,
            "correo"                    : self.USUA_CORREO_ELECT      , 
            "password"                  : self.USUA_PASSWORD       ,
            "rol"                       : self.USUA_ROL_ID
        }