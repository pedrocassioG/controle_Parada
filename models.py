from app import db
from datetime import datetime

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    chapa = db.Column(db.String(20), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    ordem = db.Column(db.String(100), nullable=False)

    retiradas = db.relationship('Retirada', backref='usuario', lazy=True)
    devolucoes = db.relationship('Devolucao', backref='usuario', lazy=True)

    def __repr__(self):
        return f"<Usuario {self.nome} ({self.chapa})>"


class Retirada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    refletores = db.Column(db.Integer, default=0)
    extensoes = db.Column(db.Integer, default=0)
    exaustores = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Retirada {self.usuario.nome} - {self.data}>"


class Devolucao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    refletores = db.Column(db.Integer, default=0)
    extensoes = db.Column(db.Integer, default=0)
    exaustores = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Devolucao {self.usuario.nome} - {self.data}>"
