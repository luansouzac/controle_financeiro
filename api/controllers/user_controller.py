from flask import request, jsonify, current_app, send_from_directory 
from models.user_model import User
from models import db 
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename 
from PIL import Image 
import os             
import uuid

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class UserController:

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    

    @staticmethod
    @jwt_required()
    def get_me():
        id_usuario_logado = get_jwt_identity()
        user = User.query.get(id_usuario_logado)
        
        if not user:
            return jsonify({"erro": "Usuário não encontrado"}), 404
            
        return jsonify(user.to_dict())

    @staticmethod
    @jwt_required()
    def update_me():
        id_usuario_logado = get_jwt_identity()
        data = request.get_json()
        
        user = User.query.get(id_usuario_logado)
        
        if not user:
            return jsonify({"erro": "Usuário não encontrado"}), 404
            
        if 'email' in data and data['email'] != user.email:
            if User.query.filter_by(email=data['email']).first():
                return jsonify({"erro": "Este email já está em uso"}), 409

        user.update(data)
        return jsonify(user.to_dict())
    @staticmethod
    @jwt_required()
    def delete_me():
        """Permite que o usuário logado delete sua própria conta."""
        id_usuario_logado = get_jwt_identity()
        user = User.query.get(id_usuario_logado)
        
        if not user:
            return jsonify({"erro": "Usuário não encontrado"}), 404
            
        user.delete()
        
        return jsonify({"mensagem": "Usuário deletado com sucesso"})
    
    @staticmethod 
    @jwt_required()
    def upload_my_profile_picture(): 
        id_usuario_logado = get_jwt_identity()
        usuario = User.query.get(id_usuario_logado) 

        if not usuario:
            return jsonify({"erro": "Usuário não encontrado"}), 404

        if 'image' not in request.files:
            return jsonify({"erro": "Campo 'image' não encontrado no formulário"}), 400

        file = request.files['image']

        if file.filename == '':
            return jsonify({"erro": "Nenhum arquivo selecionado"}), 400

        if not UserController.allowed_file(file.filename): 
            return jsonify({"erro": "Tipo de arquivo não permitido"}), 400

        filepath = None
        try:
            ext = file.filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{id_usuario_logado}_{uuid.uuid4().hex}.{ext}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)

            img = Image.open(file.stream)
            img.thumbnail((300, 300))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(filepath, format='JPEG', quality=85) 
            img.close() 

            old_filename = usuario.image  
            if old_filename:
                old_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], old_filename)
                if os.path.exists(old_filepath):
                    try:
                        os.remove(old_filepath)
                    except OSError as e:
                        print(f"Erro ao deletar arquivo antigo {old_filepath}: {e}") 

            usuario.image = unique_filename 
            db.session.commit()

            return jsonify({"message": "Upload bem-sucedido", "filename": unique_filename}), 200

        except Exception as e:
            db.session.rollback() 
            if filepath and os.path.exists(filepath):
                 try:
                    os.remove(filepath)
                 except OSError as e_remove:
                     print(f"Erro ao remover arquivo parcialmente salvo {filepath}: {e_remove}")
            print(f"Erro no upload/processamento: {e}") 
            return jsonify({"erro": f"Falha ao processar a imagem: {str(e)}"}), 500
            
    @staticmethod
    @jwt_required()
    def get_profile_image():
        id_usuario_logado = get_jwt_identity()
        user = User.query.get(id_usuario_logado)

        if not user or not user.image:
            return jsonify({"erro": "Imagem não encontrada"}), 404

        try:
            return send_from_directory(
                current_app.config['UPLOAD_FOLDER'],
                user.image, 
                as_attachment=False 
            )
        except FileNotFoundError:
            return jsonify({"erro": "Arquivo físico não encontrado"}), 404

    
    #caso tenha area de admin a gente usa essas funcoes abaixo
    # @staticmethod
    # def get_users():
    #     users_list = User.get_all_users()
    #     return jsonify([u.to_dict() for u in users_list])
    # @staticmethod
    # def get_user_by_id( user_id):
    #     user = User.get_by_id(user_id)
    #     if user:
    #         return jsonify(user.to_dict())
    #     return jsonify({"error": "Usuário não encontrado"}), 404
    # @staticmethod
    # def create_user( user_data):
    #     new_user = User.create(user_data)
    #     return jsonify(new_user.to_dict()), 201
    # @staticmethod
    # def update_user( user_id, user_data):
    #     user = User.get_by_id(user_id)
    #     if not user:
    #         return jsonify({"error": "Usuário não encontrado"}), 404
        
    #     user.update(user_data)
    #     return jsonify(user.to_dict())
    # @staticmethod
    # def delete_user( user_id):
    #     user = User.get_by_id(user_id)
    #     if not user:
    #         return jsonify({"error": "Usuário não encontrado"}), 404
        
    #     user.delete()
    #     return jsonify({"message": "Usuário deletado com sucesso"}), 200