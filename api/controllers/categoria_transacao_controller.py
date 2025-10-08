from flask import jsonify
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
    def create_categoria(categoria_data):
        new_categoria = CategoriaTransacao.create(categoria_data)
        return jsonify(new_categoria.to_dict()), 201
    @staticmethod
    def update_categoria(categoria_id, categoria_data):
        categoria = CategoriaTransacao.get_by_id(categoria_id)
        if not categoria:
            return jsonify({"error": "Categoria não encontrada"}), 404
        
        updated_categoria = CategoriaTransacao.update(categoria_id, categoria_data)
        return jsonify(updated_categoria.to_dict())
    @staticmethod
    def delete_categoria(categoria_id):
        categoria = CategoriaTransacao.get_by_id(categoria_id)
        if not categoria:
            return jsonify({"error": "Categoria não encontrada"}), 404
        
        CategoriaTransacao.delete(categoria_id)
        return jsonify({"message": "Categoria deletada com sucesso"}), 200