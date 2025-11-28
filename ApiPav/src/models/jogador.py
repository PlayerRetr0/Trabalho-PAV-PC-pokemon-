from src.models.base import db

class Jogador(db.Model):
    __tablename__ = 'jogador'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(30), nullable=False)
    idade = db.Column(db.Integer, nullable=False)

    caixas = db.relationship("Caixa", backref="jogador", cascade="all, delete-orphan")

    equipe = db.relationship("Equipe", backref="jogador", uselist=False, cascade="all, delete-orphan")
