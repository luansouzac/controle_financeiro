from flask import Blueprint
import controllers.user_controller as user_ctrl

routes_bp = Blueprint('routes_bp', __name__)


@routes_bp.route('/users', methods=['GET'])
def users():
    return user_ctrl.get_users()
@routes_bp.route('/users/<int:user_id>', methods=['GET'])
def user_detail(user_id):
    return user_ctrl.get_user_by_id(user_id)
@routes_bp.route('/users', methods=['POST'])
def create_user():
    from flask import request
    user_data = request.get_json()
    return user_ctrl.create_user(user_data)
@routes_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    from flask import request
    user_data = request.get_json()
    return user_ctrl.update_user(user_id, user_data)
@routes_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return user_ctrl.delete_user(user_id)



# @routes_bp.route('/posts', methods=['GET'])
# def posts():
#     return get_posts()
