from flask import Blueprint
from flask import request
from controllers.auth_controller import AuthController
from controllers.user_controller import UserController
from controllers.carteira_controller import CarteiraController
from controllers.saldo_controller import SaldoController
from controllers.categoria_transacao_controller import CategoriaTransacaoController
from controllers.transacao_controller import TransacaoController


routes_bp = Blueprint('routes_bp', __name__)


@routes_bp.route('/register', methods=['POST'])
def register():
    return AuthController.register()

@routes_bp.route('/login', methods=['POST'])
def login():
    return AuthController.login()

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
    return CarteiraController.create_carteira()
@routes_bp.route('/carteiras/<int:carteira_id>', methods=['PUT'])
def update_carteira(carteira_id):
    carteira_data = request.get_json()
    return CarteiraController.update_carteira(carteira_id, carteira_data)
@routes_bp.route('/carteiras/<int:carteira_id>', methods=['DELETE'])
def delete_carteira(carteira_id):
    return CarteiraController.delete_carteira(carteira_id)
@routes_bp.route('/me/carteiras', methods=['GET'])
def get_minhas_carteiras():
    return CarteiraController.get_minhas_carteiras()

@routes_bp.route('/saldos', methods=['GET'])
def saldos():
    return SaldoController.get_saldos()
@routes_bp.route('/saldos/<int:saldo_id>', methods=['GET'])
def saldo_detail(saldo_id):
    return SaldoController.get_saldo_by_id(saldo_id)
# @routes_bp.route('/saldos', methods=['POST'])
# def create_saldo():
#     saldo_data = request.get_json()
#     return SaldoController.create_saldo(saldo_data)
# @routes_bp.route('/saldos/<int:saldo_id>', methods=['PUT'])
# def update_saldo(saldo_id):
#     saldo_data = request.get_json()
#     return SaldoController.update_saldo(saldo_id, saldo_data)
# @routes_bp.route('/saldos/<int:saldo_id>', methods=['DELETE'])
# def delete_saldo(saldo_id):
#     return SaldoController.delete_saldo(saldo_id)

@routes_bp.route('/categorias_transacao', methods=['GET'])
def categorias():
    return CategoriaTransacaoController.get_categorias()
@routes_bp.route('/categorias_transacao/<int:categoria_id>', methods=['GET'])
def categoria_detail(categoria_id):
    return CategoriaTransacaoController.get_categoria_by_id(categoria_id)
@routes_bp.route('/categorias_transacao', methods=['POST'])
def create_categoria():
    return CategoriaTransacaoController.create_categoria()
@routes_bp.route('/categorias_transacao/<int:categoria_id>', methods=['PUT'])
def update_categoria(categoria_id):
    return CategoriaTransacaoController.update_categoria(categoria_id)
@routes_bp.route('/categorias_transacao/<int:categoria_id>', methods=['DELETE'])
def delete_categoria(categoria_id):
    return CategoriaTransacaoController.delete_categoria(categoria_id)

@routes_bp.route('/user/transacoes', methods=['GET'])
def get_minhas_transacoes():
    return TransacaoController.get_minhas_transacoes()
@routes_bp.route('/user/transacoes/<int:transacao_id>', methods=['GET'])
def transacao_detail(transacao_id):
    return TransacaoController.get_transacao_by_id(transacao_id)
@routes_bp.route('/user/transacoes', methods=['POST'])
def create_transacao():
    return TransacaoController.create_transacao()
@routes_bp.route('/user/transacoes/<int:transacao_id>', methods=['DELETE'])
def delete_transacao(transacao_id):
    return TransacaoController.delete_transacao(transacao_id)



# @routes_bp.route('/posts', methods=['GET'])
# def posts():
#     return get_posts()
