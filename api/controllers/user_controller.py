from flask import jsonify
from models.user_model import Users

def get_users():
    users_list = Users.get_all_users()
    return jsonify([u.to_dict() for u in users_list])

def get_user_by_id(user_id):
    user = Users.get_by_id(user_id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({"error": "Usuário não encontrado"}), 404

def create_user(user_data):
    new_user = Users.create(user_data)
    return jsonify(new_user.to_dict()), 201

def update_user(user_id, user_data):
    user = Users.get_by_id(user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404
    
    user.update(user_data)
    return jsonify(user.to_dict())

def delete_user(user_id):
    user = Users.get_by_id(user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404
    
    user.delete()
    return jsonify({"message": "Usuário deletado com sucesso"}), 200