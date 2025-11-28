from src.models.base import db
from src.models.equipe import Equipe
from src.models.jogador import Jogador
from src.models.pokemon import Pokemon
from typing import List, Optional

class EquipeService:
    
    def criar_equipe(self, jogador_id: int) -> Equipe:
        j = Jogador.query.get(jogador_id)
        if not j:
            raise ValueError("Jogador não existe")
        if j.equipe:
            raise ValueError("Já tem equipe")
        
        e = Equipe(jogador_id=jogador_id)
        db.session.add(e)
        db.session.commit()
        return e
    
    def listar_equipes(self) -> List[Equipe]:
        return Equipe.query.all()
    
    def buscar_equipe_por_id(self, equipe_id: int) -> Optional[Equipe]:
        return Equipe.query.get(equipe_id)
    
    def buscar_equipe_por_jogador(self, jogador_id: int) -> Optional[Equipe]:
        return Equipe.query.filter_by(jogador_id=jogador_id).first()
    
    def adicionar_pokemon(self, equipe_id: int, pokemon_id: int) -> Equipe:
        e = self.buscar_equipe_por_id(equipe_id)
        p = Pokemon.query.get(pokemon_id)
        if not e or not p:
            raise ValueError("Não existe")
        if len(e.pokemons) >= 6:
            raise ValueError("Equipe cheia")
        if p in e.pokemons:
            raise ValueError("Já está na equipe")
        e.pokemons.append(p)
        db.session.commit()
        return e
    
    def remover_pokemon(self, equipe_id: int, pokemon_id: int) -> Equipe:
        e = self.buscar_equipe_por_id(equipe_id)
        p = Pokemon.query.get(pokemon_id)
        if not e or not p:
            raise ValueError("Não existe")
        if p not in e.pokemons:
            raise ValueError("Não está na equipe")
        e.pokemons.remove(p)
        db.session.commit()
        return e
    
    def deletar_equipe(self, equipe_id: int) -> bool:
        e = self.buscar_equipe_por_id(equipe_id)
        if not e:
            raise ValueError("Não existe")
        db.session.delete(e)
        db.session.commit()
        return True

