from src.models.base import db

class EquipePokemon(db.Model):
    __tablename__ = 'equipe_pokemon'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    equipe_id = db.Column(db.Integer, db.ForeignKey("equipe.id"), nullable=False)
    pokemon_id = db.Column(db.Integer, db.ForeignKey("pokemon.id"), nullable=False)

    posicao = db.Column(db.Integer, nullable=False)
