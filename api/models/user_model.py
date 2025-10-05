from models import db
from datetime import datetime


class Users(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "cpf": self.cpf,
            "nome": self.nome,
            "email": self.email,
            "criado_em": self.criado_em.strftime("%Y-%m-%d %H:%M:%S")
            if self.criado_em else None
        }
