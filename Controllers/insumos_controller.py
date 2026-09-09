from flask import jsonify, request
from Services.insumos_services import insumos_services
class insumos_controller:
    def cntListInsumos():
        data = insumos_services.servListInsumos()
        return jsonify(data), 200

    def cntAddInsumos():
        data = request.get_json(silent=True)

        codigo = data["codigo"]
        nombre = data["nombre"]
        cantidad = data["cantidad"]
        precio = data["precio"]
        estado = data["estado"]
        usuario_id = data["usuario_id"]
        proveedor_id = data["proveedor_id"]
        etc_id = data["etc_id"]

        x = insumos_services.addInsumos(codigo, nombre, cantidad, precio, estado, usuario_id, proveedor_id, etc_id)
        return jsonify(x), 200

    def cntDelInsumos(id):
        data = insumos_services.deleteInsumos(id)
        return jsonify(data), 200

    def cntModInsumos(id):
        data = request.get_json(silent=True)

        codigo = data["codigo"]
        nombre = data["nombre"]
        cantidad = data["cantidad"]
        precio = data["precio"]
        estado = data["estado"]
        usuario_id = data["usuario_id"]
        proveedor_id = data["proveedor_id"]
        etc_id = data["etc_id"]

        x = insumos_services.updateInsumos(id, codigo, nombre, cantidad, precio, estado, usuario_id, proveedor_id, etc_id)
        return jsonify(x), 201

