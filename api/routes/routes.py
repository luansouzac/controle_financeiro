from flask import Blueprint
from flask import request
from controllers.user_controller import UserController
from controllers.carteira_controller import CarteiraController
from controllers.saldo_controller import SaldoController

routes_bp = Blueprint('routes_bp', __name__)


@routes_bp.route('/users', methods=['GET'])
def users():
    return UserController.get_users()
@routes_bp.route('/users/<int:user_id>', methods=['GET'])
def user_detail(user_id):
    return UserController.get_user_by_id(user_id)
@routes_bp.route('/users', methods=['POST'])
def create_user():
    user_data = request.get_json()
    return UserController.create_user(user_data)
@routes_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.get_json()
    return UserController.update_user(user_id, user_data)
@routes_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return UserController.delete_user(user_id)


@routes_bp.route('/carteiras', methods=['GET'])
def carteiras():
    return CarteiraController.get_carteiras()
@routes_bp.route('/carteiras/<int:carteira_id>', methods=['GET'])
def carteira_detail(carteira_id):
    return CarteiraController.get_carteira_by_id(carteira_id)
@routes_bp.route('/carteiras', methods=['POST'])
def create_carteira():
    carteira_data = request.get_json()
    return CarteiraController.create_carteira(carteira_data)
@routes_bp.route('/carteiras/<int:carteira_id>', methods=['PUT'])
def update_carteira(carteira_id):
    carteira_data = request.get_json()
    return CarteiraController.update_carteira(carteira_id, carteira_data)
@routes_bp.route('/carteiras/<int:carteira_id>', methods=['DELETE'])
def delete_carteira(carteira_id):
    return CarteiraController.delete_carteira(carteira_id)

@routes_bp.route('/saldos', methods=['GET'])
def saldos():
    return SaldoController.get_saldos()
@routes_bp.route('/saldos/<int:saldo_id>', methods=['GET'])
def saldo_detail(saldo_id):
    return SaldoController.get_saldo_by_id(saldo_id)
@routes_bp.route('/saldos', methods=['POST'])
def create_saldo():
    saldo_data = request.get_json()
    return SaldoController.create_saldo(saldo_data)
@routes_bp.route('/saldos/<int:saldo_id>', methods=['PUT'])
def update_saldo(saldo_id):
    saldo_data = request.get_json()
    return SaldoController.update_saldo(saldo_id, saldo_data)
@routes_bp.route('/saldos/<int:saldo_id>', methods=['DELETE'])
def delete_saldo(saldo_id):
    return SaldoController.delete_saldo(saldo_id)




# @routes_bp.route('/posts', methods=['GET'])
# def posts():
#     return get_posts()
