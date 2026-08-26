from flask import current_app
from Models.cliente import Cliente
import uuid as uuid_lib

class cliente_services:
    def servListCliente():
        sql = "SELECT * FROM T_CLIENTE"

        c   = current_app.mysql.connection.cursor() 
        c.execute(sql)
        
        data = c.fetchall()
        print(data)
        
        clientes_l =[ ]
        for u in data:
            clientes_l.append(Cliente(u[0],u[1],u[2]).to_dic())

        print(clientes_l)
        c.close()

        return clientes_l

    def addCliente(persona_id):
        uuid = str(uuid_lib.uuid4())

        c   = current_app.mysql.connection.cursor()
        sql = "INSERT INTO T_CLIENTE (CLI_UUID, CLI_PER_ID) VALUES (%s, %s)"

        c.execute(sql, (uuid, persona_id))
        current_app.mysql.connection.commit()

        c.close()
        return {
            "mensaje": "Cliente agregado correctamente",
        }

    def deleteCliente(id):

        sql = "DELETE FROM T_CLIENTE WHERE CLI_ID = %s"

        c = current_app.mysql.connection.cursor()
        c.execute(sql, (id,))
        current_app.mysql.connection.commit()
        c.close()

        return "Cliente eliminado correctamente"

    def updateCliente():
        sql = "UPDATE T_CLIENTE SET CLI_UUID = %s, CLI_PER_ID = %s"

        c = current_app.mysql.connection.cursor()
        c.execute(sql, ("cli_uuid", "cli_per_id"))
        current_app.mysql.connection.commit()
        c.close()

        return "Cliente actualizado correctamente"