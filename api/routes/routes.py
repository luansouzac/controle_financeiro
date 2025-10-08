from flask import Blueprint
from flask import request
import controllers.user_controller as user_ctrl
import controllers.carteira_controller as carteira_ctrl

routes_bp = Blueprint('routes_bp', __name__)


@routes_bp.route('/users', methods=['GET'])
def users():
    return user_ctrl.get_users()
@routes_bp.route('/users/<int:user_id>', methods=['GET'])
def user_detail(user_id):
    return user_ctrl.get_user_by_id(user_id)
@routes_bp.route('/users', methods=['POST'])
def create_user():
    user_data = request.get_json()
    return user_ctrl.create_user(user_data)
@routes_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.get_json()
    return user_ctrl.update_user(user_id, user_data)
@routes_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return user_ctrl.delete_user(user_id)


@routes_bp.route('/carteiras', methods=['GET'])
def carteiras():
    return carteira_ctrl.get_carteiras()
@routes_bp.route('/carteiras/<int:carteira_id>', methods=['GET'])
def carteira_detail(carteira_id):
    return carteira_ctrl.get_carteira_by_id(carteira_id)
@routes_bp.route('/carteiras', methods=['POST'])
def create_carteira():
    carteira_data = request.get_json()
    return carteira_ctrl.create_carteira(carteira_data)
@routes_bp.route('/carteiras/<int:carteira_id>', methods=['PUT'])
def update_carteira(carteira_id):
    carteira_data = request.get_json()
    return carteira_ctrl.update_carteira(carteira_id, carteira_data)
@routes_bp.route('/carteiras/<int:carteira_id>', methods=['DELETE'])
def delete_carteira(carteira_id):
    return carteira_ctrl.delete_carteira(carteira_id)



# @routes_bp.route('/posts', methods=['GET'])
# def posts():
#     return get_posts()
