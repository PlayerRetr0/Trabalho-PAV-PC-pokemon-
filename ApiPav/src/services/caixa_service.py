from src.models.base import db
from src.models.caixa import Caixa
from src.models.jogador import Jogador
from typing import List, Optional

class CaixaService:
    
    def criar_caixa(self, nome: str, jogador_id: int) -> Caixa:
        if not nome or not nome.strip():
            raise ValueError("Nome vazio")
        if len(nome) > 20:
            raise ValueError("Nome muito longo")
        
        if not Jogador.query.get(jogador_id):
            raise ValueError("Jogador não existe")
        
        c = Caixa(nome=nome, jogador_id=jogador_id)
        db.session.add(c)
        db.session.commit()
        return c
    
    def listar_caixas(self) -> List[Caixa]:
        return Caixa.query.all()
    
    def buscar_caixa_por_id(self, caixa_id: int) -> Optional[Caixa]:
        return Caixa.query.get(caixa_id)
    
    def listar_caixas_por_jogador(self, jogador_id: int) -> List[Caixa]:
        return Caixa.query.filter_by(jogador_id=jogador_id).all()
    
    def atualizar_caixa(self, caixa_id: int, nome: str = None) -> Caixa:
        c = self.buscar_caixa_por_id(caixa_id)
        if not c:
            raise ValueError("Não existe")
        
        if nome is not None:
            if not nome.strip():
                raise ValueError("Nome vazio")
            if len(nome) > 20:
                raise ValueError("Nome muito longo")
            c.nome = nome
        
        db.session.commit()
        return c
    
    def deletar_caixa(self, caixa_id: int) -> bool:
        c = self.buscar_caixa_por_id(caixa_id)
        if not c:
            raise ValueError("Não existe")
        db.session.delete(c)
        db.session.commit()
        return True

