from flask import request, jsonify
from models import db
from models.transacao_model import Transacao
from models.carteira_model import Carteira
from models.saldo_model import Saldo
from flask_jwt_extended import jwt_required, get_jwt_identity

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
    @jwt_required()
    def get_minhas_transacoes():
        id_usuario_logado = get_jwt_identity()
        
        transacoes_do_usuario = Transacao.query.join(Carteira).filter(Carteira.id_usuario == id_usuario_logado).all()

        resultado = [transacao.to_dict() for transacao in transacoes_do_usuario]

        return jsonify(resultado), 200
    @staticmethod
    @jwt_required()
    def create_transacao():
        data = request.get_json()
        id_usuario_logado = get_jwt_identity()

        required_fields = ['id_carteira', 'id_categoria', 'tipo', 'valor']
        if not all(field in data for field in required_fields):
            return jsonify({"erro": "Campos obrigatórios ausentes"}), 400

        id_carteira = data['id_carteira']
        valor_str = str(data.get('valor'))
        tipo = data.get('tipo')

        carteira = Carteira.query.filter_by(id=id_carteira, id_usuario=id_usuario_logado).first()
        if not carteira:
            return jsonify({"erro": "Carteira não encontrada ou não pertence ao usuário"}), 404

        try:
            valor = float(valor_str)
            if valor <= 0:
                return jsonify({"erro": "O valor deve ser positivo"}), 400
            
            saldo = Saldo.query.filter_by(id_carteira=id_carteira).first()
            if not saldo:
                return jsonify({"erro": "Saldo não encontrado para esta carteira"}), 500

            if tipo:
                saldo.valor += valor
            else:
                saldo.valor -= valor

            nova_transacao = Transacao(
                id_carteira=id_carteira,
                id_categoria=data.get('id_categoria'),
                tipo=tipo,
                valor=valor,
                descricao=data.get('descricao')
            )

            db.session.add(nova_transacao)
            db.session.commit()

            return jsonify(nova_transacao.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"erro": "Erro ao criar transação", "detalhes": str(e)}), 500
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