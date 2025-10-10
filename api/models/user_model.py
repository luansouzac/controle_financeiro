from models import db
from datetime import datetime
import bcrypt

class User(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    carteiras = db.relationship('Carteira', back_populates='usuario', cascade="all, delete-orphan")
    def to_dict(self):
        return {
            "id": self.id,
            "cpf": self.cpf,
            "nome": self.nome,
            "email": self.email,
            "criado_em": self.criado_em.strftime("%Y-%m-%d %H:%M:%S")
            if self.criado_em else None
        }
    
    def set_password(self, password):
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        self.senha = hashed_password.decode('utf-8')
    def check_password(self, password):
        password_bytes = password.encode('utf-8')
        stored_password_bytes = self.senha.encode('utf-8')
        return bcrypt.checkpw(password_bytes, stored_password_bytes)

    @classmethod
    def get_all_users(cls): #cls é chamar a propria classe dentro do metodo
        return cls.query.all()

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)

    @classmethod
    def create(cls, user_data):
        password = user_data.pop('senha', None) #separando a senha do dicionario e transformando em hash
        user = cls(**user_data)
    
        if password:
            user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, user_data):
        for key, value in user_data.items():
            setattr(self, key, value)
        db.session.commit()
        return self
    def delete(self):
        db.session.delete(self)
        db.session.commit()
