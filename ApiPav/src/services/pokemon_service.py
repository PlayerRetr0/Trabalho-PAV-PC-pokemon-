from src.models.base import db
from src.models.pokemon import Pokemon
from src.models.tipoEnum import TipoEnum
from src.models.racaEnum import RacaEnum
from src.models.equipe import Equipe
from src.models.caixa import Caixa
from typing import List, Optional

class PokemonService:
    
    def criar_pokemon(self, raca: str, tipo: str, nome: str, genero: bool, level: int = 1) -> Pokemon:
        try:
            raca_enum = RacaEnum[raca.upper()]
            tipo_enum = TipoEnum[tipo.upper()]
        except KeyError as e:
            raise ValueError(f"Enum inválido: {e}")
        
        if nome and len(nome) > 15:
            raise ValueError("Nome muito longo")
        if not (1 <= level <= 100):
            raise ValueError("Level fora do range")
        
        p = Pokemon(raca=raca_enum, tipo=tipo_enum, nome=nome, genero=genero, level=level)
        db.session.add(p)
        db.session.commit()
        return p
    
    def listar_pokemons(self) -> List[Pokemon]:
        return Pokemon.query.all()
    
    def buscar_pokemon_por_id(self, pokemon_id: int) -> Optional[Pokemon]:
        return Pokemon.query.get(pokemon_id)
    
    def atualizar_pokemon(self, pokemon_id: int, raca: str = None, 
                         tipo: str = None, nome: str = None, 
                         genero: bool = None, level: int = None,
                         equipe_id: int = None, caixa_id: int = None) -> Pokemon:
        p = self.buscar_pokemon_por_id(pokemon_id)
        if not p:
            raise ValueError("Não existe")
        
        if raca is not None:
            try:
                p.raca = RacaEnum[raca.upper()]
            except KeyError:
                raise ValueError(f"Raça inválida")
        if tipo is not None:
            try:
                p.tipo = TipoEnum[tipo.upper()]
            except KeyError:
                raise ValueError(f"Tipo inválido")
        if nome is not None:
            if len(nome) > 15:
                raise ValueError("Nome muito longo")
            p.nome = nome
        if genero is not None:
            p.genero = genero
        if level is not None:
            if not (1 <= level <= 100):
                raise ValueError("Level fora do range")
            p.level = level
        
        # Atualizar equipe_id
        if equipe_id is not None:
            if equipe_id == 0:  # Permite remover da equipe definindo 0
                p.equipe_id = None
            else:
                equipe = Equipe.query.get(equipe_id)
                if not equipe:
                    raise ValueError("Equipe não existe")
                # Verificar se a equipe já tem 6 pokémons (sem contar o atual se já estiver na equipe)
                pokemons_na_equipe = [pok for pok in equipe.pokemons if pok.id != pokemon_id]
                if len(pokemons_na_equipe) >= 6:
                    raise ValueError("Equipe cheia")
                p.equipe_id = equipe_id
                # Remover da caixa se estiver movendo para equipe
                p.caixa_id = None
        
        # Atualizar caixa_id
        if caixa_id is not None:
            if caixa_id == 0:  # Permite remover da caixa definindo 0
                p.caixa_id = None
            else:
                caixa = Caixa.query.get(caixa_id)
                if not caixa:
                    raise ValueError("Caixa não existe")
                p.caixa_id = caixa_id
                # Remover da equipe se estiver movendo para caixa
                p.equipe_id = None
        
        db.session.commit()
        return p
    
    def deletar_pokemon(self, pokemon_id: int) -> bool:
        p = self.buscar_pokemon_por_id(pokemon_id)
        if not p:
            raise ValueError("Não existe")
        db.session.delete(p)
        db.session.commit()
        return True

