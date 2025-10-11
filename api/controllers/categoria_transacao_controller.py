from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.categoria_transacao_model import CategoriaTransacao

class CategoriaTransacaoController:
    @staticmethod
    def get_categorias():
        categorias = CategoriaTransacao.get_all_categorias()
        return jsonify([categoria.to_dict() for categoria in categorias])
    @staticmethod
    def get_categoria_by_id(categoria_id):
        categoria = CategoriaTransacao.get_by_id(categoria_id)
        if categoria:
            return jsonify(categoria.to_dict())
        return jsonify({"error": "Categoria não encontrada"}), 404
    @staticmethod
    #@jwt_required()
    def create_categoria():
        data = request.get_json()
        if not data or not data.get('nome'):
            return jsonify({"error": "O campo 'nome' é obrigatório"}), 400
        new_categoria = CategoriaTransacao.create(data)
        return jsonify(new_categoria.to_dict()), 201
    @staticmethod
    #@jwt_required()
    def update_categoria(categoria_id):
        data = request.get_json()
        if not data:
            return jsonify({"error": "Nenhum dado fornecido para atualização"}), 400
        
        categoria = CategoriaTransacao.get_by_id(categoria_id)
        if not categoria:
            return jsonify({"error": "Categoria não encontrada"}), 404
        
        categoria.update(data)
        return jsonify(categoria.to_dict())
    @staticmethod
    #@jwt_required()
    def delete_categoria(categoria_id):        
        categoria = CategoriaTransacao.get_by_id(categoria_id)
        if not categoria:
            return jsonify({"error": "Categoria não encontrada"}), 404
        
        categoria.delete()
        return jsonify({"message": "Categoria deletada com sucesso"}), 200