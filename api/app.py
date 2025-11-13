from flask import Flask
from flask_cors import CORS
from routes.routes import routes_bp
# from dotenv import load_dotenv  # <-- REMOVA OU COMENTE ISSO
from models import db
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta
from flask_migrate import Migrate

# load_dotenv() # <-- REMOVA OU COMENTE ISSO

app = Flask(__name__)

CORS(app) 

# --- SEÇÃO MODIFICADA ---
# 1. Capture as variáveis do docker-compose
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

# 2. Construa a URI. 
#    A porta interna do container MySQL é 3306.
#    (O 3307 é só para o SEU PC acessar, a API acessa pela porta 3306).
db_uri = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:3306/{db_name}"

print(f"--- String de Conexão Gerada: {db_uri} ---") # Linha de debug

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# --- FIM DA MODIFICAÇÃO ---

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') # Lembre de adicionar no docker-compose
app.config["JWT_SECRET_KEY"] = "123456789"
app.config['JSON_SORT_KEYS'] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads', 'profile_pics')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
jwt = JWTManager(app)
app.register_blueprint(routes_bp)

migrate = Migrate(app, db)


@app.route('/')
def home():
    return 'API Flask MVC + Banco conectado!'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug, port=port)