from flask import Flask
from routes.routes import routes_bp
from dotenv import load_dotenv
from models import db
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config["JWT_SECRET_KEY"] = "123456789"  # Chave secreta demais
app.config['JSON_SORT_KEYS'] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)


db.init_app(app)
jwt = JWTManager(app)
app.register_blueprint(routes_bp)


@app.route('/')
def home():
    return 'API Flask MVC + Banco conectado!'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug, port=port)
