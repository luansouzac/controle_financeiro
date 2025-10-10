from models import db
from datetime import datetime

class Carteira(db.Model):
    __tablename__ = 'carteiras'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship('User', back_populates='carteiras')

    def to_dict(self):
        return {
            "id": self.id,
            "id_usuario": self.id_usuario,
            "nome": self.nome,
            "descricao": self.descricao,
            "criado_em": self.criado_em.strftime("%Y-%m-%d %H:%M:%S")
            if self.criado_em else None
        }
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
    
    def update(cls, carteira_id, carteira_data):
        carteira = cls.get_by_id(carteira_id)
        if not carteira:
            return None
        for key, value in carteira_data.items():
            setattr(carteira, key, value)
        db.session.commit()
        return carteira
    
    def delete(cls, carteira_id):
        carteira = cls.get_by_id(carteira_id)
        if not carteira:
            return None
        db.session.delete(carteira)
        db.session.commit()
        return carteira