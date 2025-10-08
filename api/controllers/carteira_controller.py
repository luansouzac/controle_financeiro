from flask import jsonify
from models.carteira_model import Carteiras

def get_carteiras():
    carteiras_list = Carteiras.get_all_carteiras()
    return jsonify([c.to_dict() for c in carteiras_list])

def get_carteira_by_id(carteira_id):
    carteira = Carteiras.get_by_id(carteira_id)
    if carteira:
        return jsonify(carteira.to_dict())
    return jsonify({"error": "Carteira não encontrada"}), 404

def create_carteira(carteira_data):
    new_carteira = Carteiras.create(carteira_data)
    return jsonify(new_carteira.to_dict()), 201

def update_carteira(carteira_id, carteira_data):
    carteira = Carteiras.get_by_id(carteira_id)
    if not carteira:
        return jsonify({"error": "Carteira não encontrada"}), 404
    
    updated_carteira = Carteiras.update(carteira_id, carteira_data)
    return jsonify(updated_carteira.to_dict())

def delete_carteira(carteira_id):
    carteira = Carteiras.get_by_id(carteira_id)
    if not carteira:
        return jsonify({"error": "Carteira não encontrada"}), 404
    
    Carteiras.delete(carteira_id)
    return jsonify({"message": "Carteira deletada com sucesso"}), 200