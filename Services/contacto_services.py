from flask import current_app
from Models.contacto import Contacto
import uuid as uuid_lib

class contacto_services:
    def servListContacto():
        sql = "SELECT * FROM T_CONTACTO"

        c   = current_app.mysql.connection.cursor() 
        c.execute(sql)
        
        data = c.fetchall()
        print(data)
        
        contactos_l =[ ]
        for u in data:
            contactos_l.append(Contacto(u[0],u[1],u[2],u[3],u[4]).to_dic())

        print(contactos_l)
        c.close()

        return contactos_l

    def addContacto(tipo_contacto, contenido, proveedor_id):
        uuid = str(uuid_lib.uuid4())

        sql = "INSERT INTO T_CONTACTO (CONT_UUID, CONT_TIPO_DATO, CONT_CONTENIDO, CONT_PROV_ID) VALUES (%s, %s, %s, %s)"

        c   = current_app.mysql.connection.cursor()
        c.execute(sql, (uuid, tipo_contacto, contenido, proveedor_id))
        current_app.mysql.connection.commit()

        c.close()
        return "Contacto agregado correctamente"

    def deleteContacto(id):
        sql = "DELETE FROM T_CONTACTO WHERE CONT_ID = %s"

        c = current_app.mysql.connection.cursor()
        c.execute(sql, (id,))
        current_app.mysql.connection.commit()
        c.close()

        return "Contacto eliminado correctamente"

    def updateContacto(id, tipo_contacto, contenido, proveedor_id):
        sql = "UPDATE T_CONTACTO SET CONT_TIPO_DATO = %s, CONT_CONTENIDO = %s, CONT_PROV_ID = %s WHERE CONT_ID = %s"

        c = current_app.mysql.connection.cursor()
        c.execute(sql, (tipo_contacto, contenido, proveedor_id, id))
        current_app.mysql.connection.commit()
        c.close()

        return "Contacto actualizado correctamente"
