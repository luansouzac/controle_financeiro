from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.categoria_transacao_model import CategoriaTransacao
from sqlalchemy import or_

class CategoriaTransacaoController:
    @staticmethod
    @jwt_required()
    def get_categorias():
        id_usuario_logado = get_jwt_identity()
        categorias = CategoriaTransacao.query.filter(
            or_(
                CategoriaTransacao.id_usuario == id_usuario_logado,
                CategoriaTransacao.id_usuario == None
            )
        ).all()
        return jsonify([categoria.to_dict() for categoria in categorias])

    @staticmethod
    @jwt_required()
    def get_categoria_by_id(categoria_id):
        id_usuario_logado = get_jwt_identity()
        categoria = CategoriaTransacao.query.filter(
            CategoriaTransacao.id == categoria_id,
            or_(
                CategoriaTransacao.id_usuario == id_usuario_logado,
                CategoriaTransacao.id_usuario == None
            )
        ).first()
        if categoria:
            return jsonify(categoria.to_dict())
        return jsonify({"error": "Categoria não encontrada"}), 404

    @staticmethod
    @jwt_required()
    def create_categoria():
        id_usuario_logado = get_jwt_identity()
        data = request.get_json()
        if not data or not data.get('nome'):
            return jsonify({"error": "O campo 'nome' é obrigatório"}), 400
        data['id_usuario'] = id_usuario_logado
        new_categoria = CategoriaTransacao.create(data)
        return jsonify(new_categoria.to_dict()), 201

    @staticmethod
    @jwt_required()
    def update_categoria(categoria_id):
        id_usuario_logado = get_jwt_identity()
        data = request.get_json()
        if not data:
            return jsonify({"error": "Nenhum dado fornecido para atualização"}), 400
        
        categoria = CategoriaTransacao.query.filter_by(id=categoria_id, id_usuario=id_usuario_logado).first()
        
        if not categoria:
            return jsonify({"error": "Categoria não encontrada ou você não tem permissão para editá-la"}), 404
        
        if 'id_usuario' in data:
            del data['id_usuario']
            
        categoria.update(data)
        return jsonify(categoria.to_dict())

    @staticmethod
    @jwt_required()
    def delete_categoria(categoria_id):        
        id_usuario_logado = get_jwt_identity()

        categoria = CategoriaTransacao.query.filter_by(id=categoria_id, id_usuario=id_usuario_logado).first()
        
        if not categoria:
            return jsonify({"error": "Categoria não encontrada ou você não tem permissão para deletá-la"}), 404
        
        categoria.delete()
        return jsonify({"message": "Categoria deletada com sucesso"}), 200