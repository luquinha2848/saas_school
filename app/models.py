# app/models.py
from . import db
from datetime import datetime

class Responsavel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    parentesco = db.Column(db.String(50), nullable=False)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    alunos = db.relationship('Aluno', backref='responsavel', lazy=True)

    def __repr__(self):
        return f'<Responsavel {self.nome_completo}>'

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(120), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), unique=True)
    telefone = db.Column(db.String(15))
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)

    # Chave estrangeira para o responsável
    responsavel_id = db.Column(db.Integer, db.ForeignKey('responsavel.id'), nullable=True)

    def __repr__(self):
        return f'<Aluno {self.nome_completo}>'

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(15))
    data_contratacao = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Professor {self.nome_completo}>'
