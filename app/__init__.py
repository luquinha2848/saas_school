# app/__init__.py
import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key-for-dev')
    # Carrega a URI do banco de dados da variável de ambiente, com um fallback para desenvolvimento local
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:xbala@localhost:5432/saas_escola')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Configuração do logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    app.logger.info('Aplicativo Dó Ré Mi iniciado com sucesso.')


    with app.app_context():
        from . import routes

    return app
