from models import db
from datetime import datetime

class CategoriaTransacao(db.Model):
    __tablename__ = 'categorias_transacoes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "criado_em": self.criado_em.strftime("%Y-%m-%d %H:%M:%S")
            if self.criado_em else None
        }
    
    @classmethod
    def get_all_categorias(cls):
        return cls.query.all()
    @classmethod
    def get_by_id(cls, categoria_id):
        return cls.query.get(categoria_id)
    @classmethod
    def create(cls, categoria_data):
        categoria = cls(**categoria_data)
        db.session.add(categoria)
        db.session.commit()
        return categoria
    @classmethod
    def update(cls, categoria_id, categoria_data):
        categoria = cls.get_by_id(categoria_id)
        if not categoria:
            return None
        for key, value in categoria_data.items():
            setattr(categoria, key, value)
        db.session.commit()
        return categoria
    @classmethod
    def delete(cls, categoria_id):
        categoria = cls.get_by_id(categoria_id)
        if not categoria:
            return None
        db.session.delete(categoria)
        db.session.commit()
        return categoria
    