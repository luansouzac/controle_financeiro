from models import db
from datetime import datetime

class Carteiras(db.Model):
    __tablename__ = 'carteiras'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "id_usuario": self.id_usuario,
            "nome": self.nome,
            "descricao": self.descricao,
            "criado_em": self.criado_em.strftime("%Y-%m-%d %H:%M:%S")
            if self.criado_em else None
        }