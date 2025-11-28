from flask_restful import Resource, reqparse
from flask_restful import marshal_with, marshal
from src.services.caixa_service import CaixaService
from src.views.caixa_view import caixa_fields, caixa_list_fields

class CaixaController(Resource):
    
    def __init__(self):
        self.service = CaixaService()
    
    @marshal_with(caixa_fields)
    def get(self, caixa_id=None):
        if caixa_id:
            c = self.service.buscar_caixa_por_id(caixa_id)
            if not c:
                return {'erro': 'Não existe'}, 404
            return c
        
        caixas = self.service.listar_caixas()
        return [{**marshal(c, caixa_list_fields), 'total_pokemons': len(c.pokemons or [])} 
                for c in caixas], 200
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nome', type=str, required=True)
        parser.add_argument('jogador_id', type=int, required=True)
        args = parser.parse_args()
        
        try:
            caixa = self.service.criar_caixa(args['nome'], args['jogador_id'])
            return marshal(caixa, caixa_fields), 201
        except ValueError as e:
            return {'erro': str(e)}, 400
    
    def put(self, caixa_id):
        parser = reqparse.RequestParser()
        parser.add_argument('nome', type=str)
        args = parser.parse_args()
        
        try:
            caixa = self.service.atualizar_caixa(caixa_id, args.get('nome'))
            return marshal(caixa, caixa_fields), 200
        except ValueError as e:
            return {'erro': str(e)}, 400
    
    def delete(self, caixa_id):
        try:
            self.service.deletar_caixa(caixa_id)
            return {}, 204
        except ValueError:
            return {'erro': 'ID inválido'}, 404

