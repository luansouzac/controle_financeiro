from models import db
from sqlalchemy.sql import func 

class Carteira(db.Model):
    __tablename__ = 'carteiras'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    criado_em = db.Column(db.DateTime, server_default=func.now())

    usuario = db.relationship('User', back_populates='carteiras')
    saldo = db.relationship('Saldo', back_populates='carteira', uselist=False, cascade="all, delete-orphan")
    transacoes = db.relationship('Transacao', back_populates='carteira', cascade="all, delete-orphan", lazy='dynamic')
    #metodos de classe usam o classmethodo (cls)
    @classmethod
    def get_all_carteiras(cls):
        return cls.query.all()
    @classmethod
    def get_by_id(cls, carteira_id):
        return cls.query.get(carteira_id)

    @classmethod
    def create(cls, carteira_data):
        carteira = cls(**carteira_data)
        db.session.add(carteira)
        db.session.commit()
        return carteira
    
    #metodos de instacia, para atualizar ou deletar o proprio objeto, utilizando o self
    def to_dict(self):
        return {
            "id": self.id,
            "id_usuario": self.id_usuario,
            "nome": self.nome,
            "descricao": self.descricao,
            "criado_em": self.criado_em.strftime("%Y-%m-%d %H:%M:%S")
            if self.criado_em else None
        }

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()