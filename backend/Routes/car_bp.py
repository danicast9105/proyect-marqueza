from flask import Blueprint,jsonify
# from Controllers.cars_controller import cntListCars

car_bp = Blueprint('cars_bp', __name__)

@car_bp.route('/', methods=['GET'])
def listCars():
    return ""

@car_bp.route('/create', methods=['POST'])
def createCar():
    return ""

@car_bp.route('/edit', methods=['PUT'])
def updateCar():
    return ""

@car_bp.route('/delete', methods=['DELETE'])
def deleteCar():
    return ""