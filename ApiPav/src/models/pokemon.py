from src.models.base import db
from src.models.tipoEnum import TipoEnum
from src.models.racaEnum import RacaEnum


class Pokemon(db.Model):
    __tablename__ = 'pokemon'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    raca = db.Column(db.Enum(RacaEnum), nullable=False)
    tipo = db.Column(db.Enum(TipoEnum), nullable=False)
    nome = db.Column(db.String(15))
    genero = db.Column(db.Boolean(), nullable=False)
    level = db.Column(db.Integer, nullable=False, default=1)
    
    caixa_id = db.Column(db.Integer, db.ForeignKey("caixa.id"), nullable=True)
    equipe_id = db.Column(db.Integer, db.ForeignKey("equipe.id"), nullable=True)