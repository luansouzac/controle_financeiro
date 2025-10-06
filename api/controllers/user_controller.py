from flask import jsonify
from models.user_model import Users


def get_users():
    users = Users.query.all()
    return jsonify([u.to_dict() for u in users])

# def get_user_by_id(user_id):
#     user = next((u for u in users if u["id"] == user_id), None)
#     if user:
#         return jsonify(user)
#     return jsonify({"error": "Usuário não encontrado"}), 404
