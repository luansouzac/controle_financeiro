from models import db
from datetime import datetime

class Transacao(db.Model):
    __tablename__ = 'transacoes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_carteira = db.Column(db.Integer, db.ForeignKey('carteiras.id'), nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias_transacoes.id'), nullable=False)
    tipo = db.Column(db.Boolean, nullable=False)  # False (0) para receita, True (1) para despesa
    valor = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "id_carteira": self.id_carteira,
            "id_categoria": self.id_categoria,
            "tipo": self.tipo,
            "valor": float(self.valor) if self.valor is not None else None,
            "descricao": self.descricao,
            "criado_em": self.criado_em.strftime("%Y-%m-%d %H:%M:%S")
            if self.criado_em else None
        }
    
    @classmethod
    def get_all_transacoes(cls):
        return cls.query.all()
    @classmethod
    def get_by_id(cls, transacao_id):
        return cls.query.get(transacao_id)
    @classmethod
    def create(cls, transacao_data):
        transacao = cls(**transacao_data)
        db.session.add(transacao)
        db.session.commit()
        return transacao
    @classmethod
    def update(cls, transacao_id, transacao_data):
        transacao = cls.get_by_id(transacao_id)
        if not transacao:
            return None
        for key, value in transacao_data.items():
            setattr(transacao, key, value)
        db.session.commit()
        return transacao
    @classmethod
    def delete(cls, transacao_id):
        transacao = cls.get_by_id(transacao_id)
        if not transacao:
            return None
        db.session.delete(transacao)
        db.session.commit()
        return transacao

       