from models import db
from sqlalchemy.sql import func 

class CategoriaTransacao(db.Model):
    __tablename__ = 'categorias_transacoes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=True)
    criado_em = db.Column(db.DateTime, server_default=func.now())
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    usuario = db.relationship('User', back_populates='categorias_transacoes')
    transacoes = db.relationship('Transacao', back_populates='categoria', cascade="all, delete-orphan")

    #metodos de classe usam o classmethodo (cls)
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
    
    #metodos de instacia, para atualizar ou deletar o proprio objeto, utilizando o self
    def to_dict(self):
        return {
            "id": self.id,
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
    