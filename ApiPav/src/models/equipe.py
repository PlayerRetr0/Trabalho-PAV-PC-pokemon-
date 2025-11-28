from src.models.base import db

class Equipe(db.Model):
    __tablename__ = 'equipe'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    jogador_id = db.Column(db.Integer, db.ForeignKey("jogador.id"), nullable=False)

    pokemons = db.relationship(
        "Pokemon",
        backref=db.backref("equipe", uselist=False),
        primaryjoin="Equipe.id == Pokemon.equipe_id",
        cascade="all, delete-orphan"
    )
