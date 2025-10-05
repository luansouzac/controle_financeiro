from flask import Blueprint
from controllers.user_controller import get_users

routes_bp = Blueprint('routes_bp', __name__)


@routes_bp.route('/users', methods=['GET'])
def users():
    return get_users()


# @routes_bp.route('/posts', methods=['GET'])
# def posts():
#     return get_posts()
