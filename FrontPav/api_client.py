import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

class APIClient:
    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url
    
    def _get(self, endpoint):
        try:
            response = requests.get(f"{self.base_url}{endpoint}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição GET {endpoint}: {e}")
            return None
    
    def _post(self, endpoint, data=None):
        try:
            response = requests.post(
                f"{self.base_url}{endpoint}",
                json=data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição POST {endpoint}: {e}")
            return None
    
    def _put(self, endpoint, data=None):
        try:
            response = requests.put(
                f"{self.base_url}{endpoint}",
                json=data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição PUT {endpoint}: {e}")
            return None
    
    def _delete(self, endpoint):
        try:
            response = requests.delete(f"{self.base_url}{endpoint}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição DELETE {endpoint}: {e}")
            return False
    
    def listar_jogadores(self):
        return self._get("/jogador")
    
    def buscar_jogador(self, jogador_id):
        return self._get(f"/jogador/{jogador_id}")
    
    def listar_pokemons(self):
        return self._get("/pokemon")
    
    def buscar_pokemon(self, pokemon_id):
        return self._get(f"/pokemon/{pokemon_id}")
    
    def atualizar_pokemon(self, pokemon_id, **kwargs):
        data = {k: v for k, v in kwargs.items() if v is not None}
        return self._put(f"/pokemon/{pokemon_id}", data)
    
    def atualizar_pokemon_equipe_caixa(self, pokemon_id, equipe_id=None, caixa_id=None):
        data = {}
        if equipe_id is not None:
            data['equipe_id'] = equipe_id
        if caixa_id is not None:
            data['caixa_id'] = caixa_id
        elif caixa_id is None and equipe_id is not None:
            data['caixa_id'] = None
        
        try:
            response = requests.put(
                f"{self.base_url}/pokemon/{pokemon_id}",
                json=data,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except requests.exceptions.RequestException as e:
            print(f"Erro ao atualizar pokemon: {e}")
            return None
    
    def listar_caixas(self):
        return self._get("/caixa")
    
    def buscar_caixa(self, caixa_id):
        return self._get(f"/caixa/{caixa_id}")
    
    def listar_equipes(self):
        return self._get("/equipe")
    
    def buscar_equipe(self, equipe_id):
        return self._get(f"/equipe/{equipe_id}")
    
    def buscar_equipe_por_jogador(self, jogador_id):
        equipes = self.listar_equipes()
        if equipes:
            for equipe in equipes:
                if equipe.get('jogador_id') == jogador_id:
                    return self.buscar_equipe(equipe['id'])
        return None
    
    def buscar_caixas_por_jogador(self, jogador_id):
        caixas = self.listar_caixas()
        if caixas:
            return [c for c in caixas if c.get('jogador_id') == jogador_id]
        return []
    
    def buscar_pokemons_na_caixa(self, caixa_id):
        pokemons = self.listar_pokemons()
        if pokemons:
            return [p for p in pokemons if p.get('caixa_id') == caixa_id]
        return []
    
    def buscar_pokemons_na_equipe(self, equipe_id):
        equipe = self.buscar_equipe(equipe_id)
        if equipe and 'pokemons' in equipe:
            return equipe['pokemons']
        return []
    
    def buscar_pokemons_em_multiplas_caixas(self, caixa_ids):
        pokemons = self.listar_pokemons()
        if not pokemons:
            return {}
        resultado = {}
        for caixa_id in caixa_ids:
            resultado[caixa_id] = [p for p in pokemons if p.get('caixa_id') == caixa_id]
        return resultado
    
    def carregar_dados_paralelo(self, jogador_id):
        def carregar_equipe():
            equipes = self.listar_equipes()
            if equipes:
                for equipe in equipes:
                    if equipe.get('jogador_id') == jogador_id:
                        return self.buscar_equipe(equipe['id'])
            return None
        
        def carregar_caixas():
            return self.buscar_caixas_por_jogador(jogador_id)
        
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_equipe = executor.submit(carregar_equipe)
            future_caixas = executor.submit(carregar_caixas)
            
            equipe = future_equipe.result()
            caixas = future_caixas.result()
            
            return equipe, caixas
    
    def mover_pokemon_para_equipe(self, pokemon_id, equipe_id):
        pokemon = self.buscar_pokemon(pokemon_id)
        if not pokemon:
            return False, "Pokémon não encontrado"
        
        equipe = self.buscar_equipe(equipe_id)
        if not equipe:
            return False, "Equipe não encontrada"
        
        if len(equipe.get('pokemons', [])) >= 6:
            return False, "A equipe já está cheia! (Máximo 6 pokémons)"
        
        result = self.atualizar_pokemon_equipe_caixa(
            pokemon_id,
            equipe_id=equipe_id,
            caixa_id=None
        )
        
        if result:
            return True, f"{pokemon.get('nome', 'Pokémon')} foi adicionado à equipe!"
        return False, "Erro ao mover pokémon. Verifique se a API suporta atualização de equipe_id/caixa_id."
    
    def mover_pokemon_para_caixa(self, pokemon_id, caixa_id):
        pokemon = self.buscar_pokemon(pokemon_id)
        if not pokemon:
            return False, "Pokémon não encontrado"
        
        result = self.atualizar_pokemon_equipe_caixa(
            pokemon_id,
            equipe_id=None,
            caixa_id=caixa_id
        )
        
        if result:
            return True, f"{pokemon.get('nome', 'Pokémon')} foi movido para a caixa!"
        return False, "Erro ao mover pokémon. Verifique se a API suporta atualização de equipe_id/caixa_id."
    
    def criar_jogador(self, nome, idade):
        data = {"nome": nome, "idade": idade}
        result = self._post("/jogador", data)
        return result
    
    def atualizar_jogador(self, jogador_id, nome=None, idade=None):
        data = {}
        if nome:
            data["nome"] = nome
        if idade is not None:
            data["idade"] = idade
        return self._put(f"/jogador/{jogador_id}", data)
    
    def deletar_jogador(self, jogador_id):
        return self._delete(f"/jogador/{jogador_id}")
    
    def criar_pokemon(self, raca, tipo, nome=None, genero=True, level=1):
        data = {
            "raca": raca.upper(),
            "tipo": tipo.upper(),
            "genero": genero,
            "level": level
        }
        if nome:
            data["nome"] = nome
        result = self._post("/pokemon", data)
        return result
    
    def deletar_pokemon(self, pokemon_id):
        return self._delete(f"/pokemon/{pokemon_id}")
    
    def criar_caixa(self, nome, jogador_id):
        data = {"nome": nome, "jogador_id": jogador_id}
        result = self._post("/caixa", data)
        return result
    
    def atualizar_caixa(self, caixa_id, nome=None):
        data = {}
        if nome:
            data["nome"] = nome
        return self._put(f"/caixa/{caixa_id}", data)
    
    def deletar_caixa(self, caixa_id):
        return self._delete(f"/caixa/{caixa_id}")
    
    def criar_equipe(self, jogador_id):
        data = {"jogador_id": jogador_id}
        result = self._post("/equipe", data)
        return result
    
    def deletar_equipe(self, equipe_id):
        return self._delete(f"/equipe/{equipe_id}")

api = APIClient()

