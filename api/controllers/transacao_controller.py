from flask import request, jsonify
from models import db
from models.transacao_model import Transacao
from models.carteira_model import Carteira
from models.saldo_model import Saldo
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from sqlalchemy import func, extract

class TransacaoController:

    @staticmethod
    @jwt_required()
    def get_minhas_transacoes():
        id_usuario_logado = get_jwt_identity()
        query = Transacao.query.join(Carteira).filter(Carteira.id_usuario == id_usuario_logado)

        # filtro carteira
        if 'carteira_id' in request.args:
            query = query.filter(Transacao.id_carteira == request.args.get('carteira_id', type=int))

        # filtro por tipo de transacao
        if 'tipo' in request.args:
            if request.args['tipo'].lower() == 'receita':
                query = query.filter(Transacao.tipo == True)
            elif request.args['tipo'].lower() == 'despesa':
                query = query.filter(Transacao.tipo == False)

        # filtro de data
        if 'data_inicio' in request.args:
            query = query.filter(Transacao.criado_em >= datetime.fromisoformat(request.args['data_inicio']))
        if 'data_fim' in request.args:
            query = query.filter(Transacao.criado_em <= datetime.fromisoformat(request.args['data_fim']))

        transacoes = query.order_by(Transacao.criado_em.desc()).all()
        return jsonify([t.to_dict() for t in transacoes])
    
    @staticmethod
    @jwt_required()
    def get_transacao_by_id(transacao_id):
        transacao = Transacao.get_by_id(transacao_id)
        if transacao:
            return jsonify(transacao.to_dict())
        return jsonify({"error": "Transação nao encontrada"}), 404
    
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
                if saldo.valor < valor:
                    return jsonify({"erro": "Saldo insuficiente"}), 400
                saldo.valor -= valor

            dados_da_transacao = {
                "id_carteira": id_carteira,
                "id_categoria": data.get('id_categoria'),
                "tipo": data.get('tipo'),
                "valor": valor,
                "descricao": data.get('descricao')
            }

            nova_transacao = Transacao.create_sem_commit(dados_da_transacao)

            db.session.commit()

            return jsonify(nova_transacao.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"erro": "Erro ao criar transação", "detalhes": str(e)}), 500    
    @staticmethod
    @jwt_required()
    def delete_transacao(transacao_id):
        id_usuario_logado = get_jwt_identity()

        transacao = Transacao.query.join(Carteira).filter(
            Transacao.id == transacao_id,
            Carteira.id_usuario == id_usuario_logado
        ).first()

        if not transacao:
            return jsonify({"erro": "Transação não encontrada"}), 404
        
        try:
            saldo = Saldo.query.filter_by(id_carteira=transacao.id_carteira).first()
            if transacao.tipo:  # Se a transação era uma RECEITA (True), o dinheiro SAI
                saldo.valor -= transacao.valor
            else:  # Se a transação era uma DESPESA (False), o dinheiro VOLTA
                saldo.valor += transacao.valor
            
            transacao.delete_sem_commit()

            db.session.commit()
            
            return jsonify({"mensagem": "Transação deletada com sucesso"})

        except Exception as e:
            db.session.rollback()
            return jsonify({"erro": "Erro ao deletar transação", "detalhes": str(e)}), 500
    @staticmethod
    @jwt_required()
    def get_dashboard():
        id_usuario_logado = get_jwt_identity()
        mes = request.args.get('mes', datetime.now().month, type=int)
        ano = request.args.get('ano', datetime.now().year, type=int)

        base_query = db.session.query(func.sum(Transacao.valor)).join(Carteira).filter(
            Carteira.id_usuario == id_usuario_logado,
            extract('month', Transacao.criado_em) == mes,
            extract('year', Transacao.criado_em) == ano
        )

        total_receitas = base_query.filter(Transacao.tipo == True).scalar() or float('0.00')
        total_despesas = base_query.filter(Transacao.tipo == False).scalar() or float('0.00')

        return jsonify({
            "total_receitas": str(total_receitas),
            "total_despesas": str(total_despesas),
            "saldo_do_mes": str(total_receitas - total_despesas)
        })
            