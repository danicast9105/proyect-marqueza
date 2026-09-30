from flask import Blueprint, jsonify
from Controllers.detalle_cotizacion_controller import detalle_cotizacion_controller

detalle_cotizacion_bp = Blueprint('detalle_cotizacion_bp', __name__)

@detalle_cotizacion_bp.route('/', methods=['GET'])
def listDetalleCotizacion():
    x = detalle_cotizacion_controller.cntListDetalleCotizacion()
    return x

@detalle_cotizacion_bp.route('/', methods=['POST'])
def createDetalleCotizacion():
    x = detalle_cotizacion_controller.cntAddDetalleCotizacion()
    return x

@detalle_cotizacion_bp.route('/<id>', methods=['PUT'])
def updateDetalleCotizacion(id):
    x = detalle_cotizacion_controller.cntModDetalleCotizacion(id)
    return x

@detalle_cotizacion_bp.route('/<id>', methods=['DELETE'])
def deleteDetalleCotizacion(id):
    x = detalle_cotizacion_controller.cntDelDetalleCotizacion(id)
    return x
