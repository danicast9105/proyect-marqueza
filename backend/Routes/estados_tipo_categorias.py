from flask import Blueprint
from Controllers.estado_tipo_categoria_controller import cntListEstadosTiposCategorias, cntCreateEstadoTipoCategoria, cntUpdateEstadoTipoCategoria, cntDeleteEstadoTipoCategoria

etc_bp = Blueprint('etc_bp', __name__)

@etc_bp.route('/', methods=['GET'])
def listEstadosTiposCategorias():
    return cntListEstadosTiposCategorias()

@etc_bp.route('/create', methods=['POST'])
def createEstadoTipoCategoria():
    return cntCreateEstadoTipoCategoria()

@etc_bp.route('/edit', methods=['PUT'])
def updateEstadoTipoCategoria():
    return cntUpdateEstadoTipoCategoria()

@etc_bp.route('/delete', methods=['DELETE'])
def deleteEstadoTipoCategoria():
    return cntDeleteEstadoTipoCategoria()

# http://127.0.0.1:5000/estados_tipos_categorias/
# http://127.0.0.1:5000/estados_tipos_categorias/create
# http://127.0.0.1:5000/estados_tipos_categorias/edit
# http://127.0.0.1:5000/estados_tipos_categorias/delete