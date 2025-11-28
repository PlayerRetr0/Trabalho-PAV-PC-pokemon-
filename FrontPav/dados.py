from api_client import api

class DadosPokemon:
    def __init__(self):
        self.jogador_id = None
        self.equipe_id = None
        self.caixa_ids = []
        self._carregar_dados_iniciais()
    
    def _carregar_dados_iniciais(self):
        jogadores = api.listar_jogadores()
        if jogadores and len(jogadores) > 0:
            self.jogador_id = jogadores[0].get('id')
            self._carregar_equipe()
            self._carregar_caixas()
    
    def _carregar_equipe(self):
        if self.jogador_id:
            equipe = api.buscar_equipe_por_jogador(self.jogador_id)
            if equipe:
                self.equipe_id = equipe.get('id')
    
    def _carregar_caixas(self):
        if self.jogador_id:
            caixas = api.buscar_caixas_por_jogador(self.jogador_id)
            self.caixa_ids = [c.get('id') for c in caixas if c]
    
    def get_equipe(self):
        if not self.equipe_id:
            return []
        pokemons = api.buscar_pokemons_na_equipe(self.equipe_id)
        return pokemons if pokemons else []
    
    def get_caixa(self):
        pokemons_caixa = []
        for caixa_id in self.caixa_ids:
            pokemons = api.buscar_pokemons_na_caixa(caixa_id)
            if pokemons:
                pokemons_caixa.extend(pokemons)
        return pokemons_caixa
    
    def get_total_equipe(self):
        return len(self.get_equipe())
    
    def get_total_caixa(self):
        return len(self.get_caixa())
    
    def mover_para_equipe(self, pokemon_id):
        if not self.equipe_id:
            return False, "Equipe não encontrada. Crie uma equipe primeiro."
        
        return api.mover_pokemon_para_equipe(pokemon_id, self.equipe_id)
    
    def remover_da_equipe(self, pokemon_id):
        if not self.caixa_ids or len(self.caixa_ids) == 0:
            return False, "Nenhuma caixa disponível."
        
        caixa_id = self.caixa_ids[0]
        return api.mover_pokemon_para_caixa(pokemon_id, caixa_id)
    
    def atualizar(self):
        try:
            if self.jogador_id:
                equipe, caixas = api.carregar_dados_paralelo(self.jogador_id)
                if equipe:
                    self.equipe_id = equipe.get('id')
                else:
                    self.equipe_id = None
                if caixas:
                    self.caixa_ids = [c.get('id') for c in caixas if c and c.get('id')]
                else:
                    self.caixa_ids = []
            else:
                jogadores = api.listar_jogadores()
                if jogadores and len(jogadores) > 0:
                    self.jogador_id = jogadores[0].get('id')
                self._carregar_equipe()
                self._carregar_caixas()
        except Exception as e:
            print(f"Erro ao atualizar dados: {e}")
            try:
                self._carregar_equipe()
                self._carregar_caixas()
            except:
                pass

dados = DadosPokemon()
