from flask_restful import Resource, reqparse
from flask_restful import marshal_with, marshal
from src.services.equipe_service import EquipeService
from src.views.equipe_view import equipe_fields, equipe_list_fields, equipe_detalhada_fields

class EquipeController(Resource):
    
    def __init__(self):
        self.service = EquipeService()
    
    def get(self, equipe_id=None):
        if equipe_id:
            e = self.service.buscar_equipe_por_id(equipe_id)
            if not e:
                return {'erro': 'Não existe'}, 404
            return marshal(e, equipe_detalhada_fields), 200
        
        equipes = self.service.listar_equipes()
        return [{**marshal(e, equipe_list_fields), 'total_pokemons': len(e.pokemons or [])} 
                for e in equipes], 200
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('jogador_id', type=int, required=True)
        args = parser.parse_args()
        
        try:
            equipe = self.service.criar_equipe(args['jogador_id'])
            return marshal(equipe, equipe_fields), 201
        except ValueError as e:
            return {'erro': str(e)}, 400
    
    def delete(self, equipe_id):
        try:
            self.service.deletar_equipe(equipe_id)
            return {}, 204
        except ValueError:
            return {'erro': 'ID inválido'}, 404

