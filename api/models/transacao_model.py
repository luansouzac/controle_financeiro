from models import db
from sqlalchemy.sql import func 

class Transacao(db.Model):
    __tablename__ = 'transacoes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_carteira = db.Column(db.Integer, db.ForeignKey('carteiras.id'), nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias_transacoes.id'), nullable=False)
    tipo = db.Column(db.Boolean, nullable=False)  
    valor = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    criado_em = db.Column(db.DateTime, server_default=func.now())

    carteira = db.relationship('Carteira', back_populates='transacoes')
    categoria = db.relationship('CategoriaTransacao', back_populates='transacoes')

    @classmethod
    def create_sem_commit(clas, data):
        transacao = clas(**data)
        db.session.add(transacao)
        return transacao
    
    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def delete_sem_commit(self):
        db.session.delete(self)

    def to_dict(self):
        return {
            "id": self.id,
            "tipo": "Receita" if self.tipo else "Despesa",
            "valor": float(self.valor) if self.valor is not None else None,
            "descricao": self.descricao,    
            "carteira": self.carteira.to_dict() if self.carteira else None,
            "categoria": self.categoria.to_dict() if self.categoria else None,
            "criado_em": self.criado_em.strftime("%Y-%m-%d %H:%M:%S")
            if self.criado_em else None,
        }
    
    @classmethod
    def get_all_transacoes(cls):
        return cls.query.all()
    @classmethod
    def get_by_id(cls, transacao_id):
        return cls.query.get(transacao_id)
   