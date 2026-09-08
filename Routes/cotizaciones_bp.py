from flask import Blueprint, jsonify
from Controllers.cotizaciones_controller import cotizaciones_controller

cotizaciones_bp = Blueprint('cotizaciones_bp', __name__)

@cotizaciones_bp.route('/', methods=['GET'])
def listCotizaciones():
    x = cotizaciones_controller.cntListCotizaciones()
    return x

@cotizaciones_bp.route('/', methods=['POST'])
def createCotizaciones():
    x = cotizaciones_controller.cntAddCotizaciones()
    return x

@cotizaciones_bp.route('/<id>', methods=['PUT'])
def updateCotizaciones(id):
    x = cotizaciones_controller.cntModCotizaciones(id)
    return x

@cotizaciones_bp.route('/<id>', methods=['DELETE'])
def deleteCotizaciones(id):
    x = cotizaciones_controller.cntDelCotizaciones(id)
    return x