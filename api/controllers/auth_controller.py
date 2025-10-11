from flask import request, jsonify
from models.user_model import User
from flask_jwt_extended import create_access_token
from models import db

class AuthController:
    @staticmethod
    def register():
        data = request.get_json()

        if not data or not data.get('email') or not data.get('senha'):
            return jsonify({"erro": "Email e senha são obrigatórios"}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"erro": "Este email já está em uso"}), 409
        
        if User.query.filter_by(cpf=data['cpf']).first():
            return jsonify({"erro": "Este CPF já está em uso"}), 409

        try:
            novo_usuario = User.create(data)
            return jsonify(novo_usuario.to_dict()), 201
        except Exception as e:
            return jsonify({"erro": "Erro ao criar usuário", "detalhes": str(e)}), 500
        
    @staticmethod
    def login():
        data = request.get_json()

        if not data or not data.get('email') or not data.get('senha'):
            return jsonify({"erro": "Email e senha são obrigatórios"}), 400
        
        email = data.get('email')
        password = data.get('senha')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            access_token = create_access_token(identity=str(user.id))
            return jsonify(access_token=access_token)

        return jsonify({"erro": "Credenciais inválidas"}), 401