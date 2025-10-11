from flask import request, jsonify
from models.carteira_model import Carteira
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.saldo_model import Saldo 
from models import db


class CarteiraController:
    @staticmethod 
    def get_carteiras():
        carteiras_list = Carteira.get_all_carteiras()
        return jsonify([c.to_dict() for c in carteiras_list])

    @staticmethod 
    def get_carteira_by_id(carteira_id):
        carteira = Carteira.get_by_id(carteira_id)
        if carteira:
            return jsonify(carteira.to_dict())
        return jsonify({"error": "Carteira não encontrada"}), 404
    @staticmethod 
    @jwt_required()
    def create_carteira():
        id_usuario_logado = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('nome'):
            return jsonify({"erro": "O campo 'nome' é obrigatório"}), 400

        try:
            nova_carteira = Carteira(
                nome=data.get('nome'),
                descricao=data.get('descricao'),
                id_usuario=id_usuario_logado
            )
            db.session.add(nova_carteira)

            saldo_inicial = Saldo(carteira=nova_carteira, valor=0.00)
            db.session.add(saldo_inicial)

            db.session.commit()
            
            return jsonify(nova_carteira.to_dict()), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({"erro": "Erro ao criar carteira", "detalhes": str(e)}), 500
    @staticmethod 
    def update_carteira(carteira_id, carteira_data):
        carteira = Carteira.get_by_id(carteira_id)
        if not carteira:
            return jsonify({"error": "Carteira não encontrada"}), 404
        
        updated_carteira = Carteira.update(carteira_id, carteira_data)
        return jsonify(updated_carteira.to_dict())
    @staticmethod 
    def delete_carteira(carteira_id):
        carteira = Carteira.get_by_id(carteira_id)
        if not carteira:
            return jsonify({"error": "Carteira não encontrada"}), 404
        
        Carteira.delete(carteira_id)
        return jsonify({"message": "Carteira deletada com sucesso"}), 200
    
    @staticmethod
    @jwt_required()
    def get_minhas_carteiras():
        id_usuario_logado = get_jwt_identity()
        carteiras_do_usuario = Carteira.query.filter_by(id_usuario=id_usuario_logado).all()
        
        resultado = [carteira.to_dict() for carteira in carteiras_do_usuario]
        
        return jsonify(resultado), 200