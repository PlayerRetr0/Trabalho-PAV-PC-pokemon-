from src.models.base import db
from src.models.jogador import Jogador
from typing import List, Optional

class JogadorService:
    
    def criar_jogador(self, nome: str, idade: int) -> Jogador:
        if idade <= 0:
            raise ValueError("Idade inválida")
        if not nome or not nome.strip():
            raise ValueError("Nome vazio")
        
        j = Jogador(nome=nome, idade=idade)
        db.session.add(j)
        db.session.commit()
        return j
    
    def listar_jogadores(self) -> List[Jogador]:
        return Jogador.query.all()
    
    def buscar_jogador_por_id(self, jogador_id: int) -> Optional[Jogador]:
        return Jogador.query.get(jogador_id)
    
    def atualizar_jogador(self, jogador_id: int, nome: str = None, idade: int = None) -> Jogador:
        j = self.buscar_jogador_por_id(jogador_id)
        if not j:
            raise ValueError("Não existe")
        
        if nome is not None:
            if not nome.strip():
                raise ValueError("Nome vazio")
            j.nome = nome
        if idade is not None:
            if idade <= 0:
                raise ValueError("Idade inválida")
            j.idade = idade
        
        db.session.commit()
        return j
    
    def deletar_jogador(self, jogador_id: int) -> bool:
        j = self.buscar_jogador_por_id(jogador_id)
        if not j:
            raise ValueError("Não existe")
        db.session.delete(j)
        db.session.commit()
        return True

