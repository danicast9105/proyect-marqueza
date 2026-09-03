from flask import Blueprint, jsonify
from Controllers.cotizaciones_controller import cntListCotizaciones, cntAddCotizaciones, cntDelCotizaciones, cntModCotizaciones

cotizaciones_bp = Blueprint('cotizaciones_bp', __name__)

@cotizaciones_bp.route('/', methods=['GET'])
def listCotizaciones():
    x = cntListCotizaciones()
    return x

@cotizaciones_bp.route('/', methods=['POST'])
def createCotizaciones():
    x = cntAddCotizaciones
    return x

@cotizaciones_bp.route('/', methods=['PUT'])
def updateCotizaciones():
    x = cntModCotizaciones
    return x

@cotizaciones_bp.route('/', methods=['DELETE'])
def deleteCotizaciones():
    x = cntDelCotizaciones
    return x