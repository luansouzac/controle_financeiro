from flask import jsonify
from models.saldo_model import Saldo
from flask_jwt_extended import jwt_required, get_jwt_identity

class SaldoController:
    @staticmethod
    @jwt_required()
    def get_saldos():
        saldos_list = Saldo.get_all_saldos()
        return jsonify([s.to_dict() for s in saldos_list])
    @staticmethod
    @jwt_required()
    def get_saldo_by_id(saldo_id):
        saldo = Saldo.get_by_id(saldo_id)
        if saldo:
            return jsonify(saldo.to_dict())
        return jsonify({"error": "Saldo não encontrado"}), 404
    @staticmethod
    @jwt_required()
    def create_saldo(saldo_data):
        new_saldo = Saldo.create(saldo_data)
        return jsonify(new_saldo.to_dict()), 201
    @staticmethod
    @jwt_required()
    def update_saldo(saldo_id, saldo_data):
        saldo = Saldo.get_by_id(saldo_id)
        if not saldo:
            return jsonify({"error": "Saldo não encontrado"}), 404
        
        updated_saldo = Saldo.update(saldo_id, saldo_data)
        return jsonify(updated_saldo.to_dict())
    @staticmethod
    @jwt_required()
    def delete_saldo(saldo_id):
        saldo = Saldo.get_by_id(saldo_id)
        if not saldo:
            return jsonify({"error": "Saldo não encontrado"}), 404
        
        Saldo.delete(saldo_id)
        return jsonify({"message": "Saldo deletado com sucesso"}), 200