from flask_restful import Resource, reqparse
from flask_restful import marshal
from src.services.pokemon_service import PokemonService
from src.views.pokemon_view import pokemon_fields, pokemon_list_fields

class PokemonController(Resource):
    
    def __init__(self):
        self.service = PokemonService()
    
    def get(self, pokemon_id=None):
        if pokemon_id:
            p = self.service.buscar_pokemon_por_id(pokemon_id)
            if not p:
                return {'erro': 'Não existe'}, 404
            return marshal(p, pokemon_fields), 200
        
        pokemons = self.service.listar_pokemons()
        return [marshal(p, pokemon_list_fields) for p in pokemons], 200
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('raca', type=str, required=True)
        parser.add_argument('tipo', type=str, required=True)
        parser.add_argument('nome', type=str)
        parser.add_argument('genero', type=bool, required=True)
        parser.add_argument('level', type=int, default=1)
        args = parser.parse_args()
        
        try:
            pokemon = self.service.criar_pokemon(args['raca'], args['tipo'], args.get('nome'), 
                                            args['genero'], args.get('level', 1))
            return marshal(pokemon, pokemon_fields), 201
        except ValueError as e:
            return {'erro': str(e)}, 400
    
    def put(self, pokemon_id):
        parser = reqparse.RequestParser()
        parser.add_argument('raca', type=str)
        parser.add_argument('tipo', type=str)
        parser.add_argument('nome', type=str)
        parser.add_argument('genero', type=bool)
        parser.add_argument('level', type=int)
        parser.add_argument('equipe_id', type=int)
        parser.add_argument('caixa_id', type=int)
        args = parser.parse_args()
        
        try:
            pokemon = self.service.atualizar_pokemon(
                pokemon_id, 
                args.get('raca'), 
                args.get('tipo'),
                args.get('nome'), 
                args.get('genero'), 
                args.get('level'),
                args.get('equipe_id'),
                args.get('caixa_id')
            )
            return marshal(pokemon, pokemon_fields), 200
        except ValueError as e:
            return {'erro': str(e)}, 400
    
    def delete(self, pokemon_id):
        try:
            self.service.deletar_pokemon(pokemon_id)
            return {}, 204
        except ValueError:
            return {'erro': 'ID inválido'}, 404

