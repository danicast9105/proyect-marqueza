from flask import Blueprint
from Controllers.cotizacion_controller import cntListCotizaciones, cntCreateCotizacion, cntUpdateCotizacion, cntDeleteCotizacion

cotizacion_bp = Blueprint('cotizacion_bp', __name__)

@cotizacion_bp.route('/', methods=['GET'])
def listCotizaciones():
    return cntListCotizaciones()

@cotizacion_bp.route('/create', methods=['POST'])
def createCotizacion():
    return cntCreateCotizacion()

@cotizacion_bp.route('/edit', methods=['PUT'])
def updateCotizacion():
    return cntUpdateCotizacion()

@cotizacion_bp.route('/delete', methods=['DELETE'])
def deleteCotizacion():
    return cntDeleteCotizacion()

# http://127.0.0.1:5000/cotizaciones/
# http://127.0.0.1:5000/cotizaciones/create
# http://127.0.0.1:5000/cotizaciones/edit/<id>
# http://127.0.0.1:5000/cotizaciones/delete/<id>
