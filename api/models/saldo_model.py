from models import db
from datetime import datetime

class Saldo(db.Model):
    __tablename__ = 'saldos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_carteira = db.Column(db.Integer, db.ForeignKey('carteiras.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    ult_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "id_carteira": self.id_carteira,
            "valor": self.valor,
            "criado_em": self.criado_em.strftime("%Y-%m-%d %H:%M:%S")
            if self.criado_em else None,
            "ult_atualizacao": self.ult_atualizacao.strftime("%Y-%m-%d %H:%M:%S")
            if self.ult_atualizacao else None
        }
    @classmethod
    def get_all_saldos(cls):
        return cls.query.all()
    @classmethod
    def get_by_id(cls, saldo_id):
        return cls.query.get(saldo_id)
    @classmethod
    def create(cls, saldo_data):
        saldo = cls(**saldo_data)
        db.session.add(saldo)
        db.session.commit()
        return saldo
    @classmethod
    def update(cls, saldo_id, saldo_data):
        saldo = cls.get_by_id(saldo_id)
        if not saldo:
            return None
        for key, value in saldo_data.items():
            setattr(saldo, key, value)
        db.session.commit()
        return saldo
    @classmethod
    def delete(cls, saldo_id):
        saldo = cls.get_by_id(saldo_id)
        if not saldo:
            return None
        db.session.delete(saldo)
        db.session.commit()
        return saldo