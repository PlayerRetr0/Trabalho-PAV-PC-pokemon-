from src.controllers.jogador_controller import JogadorController
from src.controllers.pokemon_controller import PokemonController
from src.controllers.caixa_controller import CaixaController
from src.controllers.equipe_controller import EquipeController

def endpoints(api):
    

    api.add_resource(JogadorController, '/jogador', '/jogador/<int:jogador_id>')
    
    api.add_resource(PokemonController, '/pokemon', '/pokemon/<int:pokemon_id>')
    
    api.add_resource(CaixaController, '/caixa', '/caixa/<int:caixa_id>')
    
    api.add_resource(EquipeController, '/equipe', '/equipe/<int:equipe_id>')