from src.models.base import db

class Caixa(db.Model):
    __tablename__ = 'caixa'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(20), nullable=False)

    jogador_id = db.Column(db.Integer, db.ForeignKey("jogador.id"), nullable=False)

    pokemons = db.relationship(
        "Pokemon", 
        backref=db.backref("caixa", uselist=False),
        primaryjoin="Caixa.id == Pokemon.caixa_id",
        cascade="all, delete-orphan")
