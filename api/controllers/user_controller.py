from flask import request, jsonify
from models.user_model import User
from flask_jwt_extended import jwt_required, get_jwt_identity

class UserController:

    @staticmethod
    @jwt_required()
    def get_me():
        id_usuario_logado = get_jwt_identity()
        user = User.query.get(id_usuario_logado)
        
        if not user:
            return jsonify({"erro": "Usuário não encontrado"}), 404
            
        return jsonify(user.to_dict())

    @staticmethod
    @jwt_required()
    def update_me():
        id_usuario_logado = get_jwt_identity()
        data = request.get_json()
        
        user = User.query.get(id_usuario_logado)
        
        if not user:
            return jsonify({"erro": "Usuário não encontrado"}), 404
            
        if 'email' in data and data['email'] != user.email:
            if User.query.filter_by(email=data['email']).first():
                return jsonify({"erro": "Este email já está em uso"}), 409

        user.update(data)
        return jsonify(user.to_dict())
    @staticmethod
    @jwt_required()
    def delete_me():
        """Permite que o usuário logado delete sua própria conta."""
        id_usuario_logado = get_jwt_identity()
        user = User.query.get(id_usuario_logado)
        
        if not user:
            return jsonify({"erro": "Usuário não encontrado"}), 404
            
        user.delete()
        
        return jsonify({"mensagem": "Usuário deletado com sucesso"})
    
    #caso tenha area de admin a gente usa essas funcoes abaixo
    # @staticmethod
    # def get_users():
    #     users_list = User.get_all_users()
    #     return jsonify([u.to_dict() for u in users_list])
    # @staticmethod
    # def get_user_by_id( user_id):
    #     user = User.get_by_id(user_id)
    #     if user:
    #         return jsonify(user.to_dict())
    #     return jsonify({"error": "Usuário não encontrado"}), 404
    # @staticmethod
    # def create_user( user_data):
    #     new_user = User.create(user_data)
    #     return jsonify(new_user.to_dict()), 201
    # @staticmethod
    # def update_user( user_id, user_data):
    #     user = User.get_by_id(user_id)
    #     if not user:
    #         return jsonify({"error": "Usuário não encontrado"}), 404
        
    #     user.update(user_data)
    #     return jsonify(user.to_dict())
    # @staticmethod
    # def delete_user( user_id):
    #     user = User.get_by_id(user_id)
    #     if not user:
    #         return jsonify({"error": "Usuário não encontrado"}), 404
        
    #     user.delete()
    #     return jsonify({"message": "Usuário deletado com sucesso"}), 200