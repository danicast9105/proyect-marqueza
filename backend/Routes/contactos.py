from flask import Blueprint
from Controllers.contacto_controller import cntListContactos, cntCreateContacto, cntUpdateContacto, cntDeleteContacto

contacto_bp = Blueprint('contacto_bp', __name__)

@contacto_bp.route('/', methods=['GET'])
def listContactos():
    return cntListContactos()

@contacto_bp.route('/create', methods=['POST'])
def createContacto():
    return cntCreateContacto()

@contacto_bp.route('/edit', methods=['PUT'])
def updateContacto():
    return cntUpdateContacto()

@contacto_bp.route('/delete', methods=['DELETE'])
def deleteContacto():
    return cntDeleteContacto()

# http://127.0.0.1:5000/contactos/
# http://127.0.0.1:5000/contactos/create
# http://127.0.0.1:5000/contactos/edit
# http://127.0.0.1:5000/contactos/delete