from flask import jsonify
from models.transacao_model import Transacao

class TransacaoController:
    @staticmethod
    def get_transacoes():
        transacoes_list = Transacao.get_all_transacoes()
        return jsonify([t.to_dict() for t in transacoes_list])
    @staticmethod
    def get_transacao_by_id(transacao_id):
        transacao = Transacao.get_by_id(transacao_id)
        if transacao:
            return jsonify(transacao.to_dict())
        return jsonify({"error": "Transação nao encontrada"}), 404
    @staticmethod
    def create_transacao(transacao_data):
        new_transacao = Transacao.create(transacao_data)
        return jsonify(new_transacao.to_dict()), 201
    @staticmethod
    def update_transacao(transacao_id, transacao_data):
        transacao = Transacao.get_by_id(transacao_id)
        if not transacao:
            return jsonify({"error": "Transação nao encontrada"}), 404
        
        updated_transacao = Transacao.update(transacao_id, transacao_data)
        return jsonify(updated_transacao.to_dict())
    @staticmethod
    def delete_transacao(transacao_id):
        transacao = Transacao.get_by_id(transacao_id)
        if not transacao:
            return jsonify({"error": "Transação nao encontrada"}), 404
        Transacao.delete(transacao_id)
        return jsonify({"message": "Transação deletada com sucesso"}), 200