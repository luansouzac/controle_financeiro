from flask import jsonify
from models.user_model import Users
from models import db

def get_users():
    users = Users.query.all()
    return jsonify([u.to_dict() for u in users])

def get_user_by_id(user_id):
    user = Users.query.get(user_id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({"error": "Usuário não encontrado"}), 404

def create_user(user_data):
    user = Users(**user_data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

def update_user(user_id, user_data):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    for key, value in user_data.items():
        setattr(user, key, value)

    db.session.commit()
    return jsonify(user.to_dict())

def delete_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Usuário deletado com sucesso"}), 200

# def get_user_by_id(user_id):
#     user = next((u for u in users if u["id"] == user_id), None)
#     if user:
#         return jsonify(user)
#     return jsonify({"error": "Usuário não encontrado"}), 404
