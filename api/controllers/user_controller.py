from flask import jsonify
from models.user_model import User

class UserController:
    @staticmethod
    def get_users():
        users_list = User.get_all_users()
        return jsonify([u.to_dict() for u in users_list])
    @staticmethod
    def get_user_by_id( user_id):
        user = User.get_by_id(user_id)
        if user:
            return jsonify(user.to_dict())
        return jsonify({"error": "Usuário não encontrado"}), 404
    @staticmethod
    def create_user( user_data):
        new_user = User.create(user_data)
        return jsonify(new_user.to_dict()), 201
    @staticmethod
    def update_user( user_id, user_data):
        user = User.get_by_id(user_id)
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        user.update(user_data)
        return jsonify(user.to_dict())
    @staticmethod
    def delete_user( user_id):
        user = User.get_by_id(user_id)
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        user.delete()
        return jsonify({"message": "Usuário deletado com sucesso"}), 200