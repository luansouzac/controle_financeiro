from flask import jsonify
from models.carteira_model import Carteiras
from models import db

def get_carteiras():
    carteiras = Carteiras.query.all()
    return jsonify([c.to_dict() for c in carteiras])