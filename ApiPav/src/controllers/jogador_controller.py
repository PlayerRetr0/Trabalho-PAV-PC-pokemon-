from flask_restful import Resource, reqparse
from flask_restful import marshal_with, marshal
from src.services.jogador_service import JogadorService
from src.views.jogador_view import jogador_fields, jogador_list_fields

class JogadorController(Resource):
    
    def __init__(self):
        self.service = JogadorService()
    
    @marshal_with(jogador_fields)
    def get(self, jogador_id=None):
        if jogador_id:
            jogador = self.service.buscar_jogador_por_id(jogador_id)
            if not jogador:
                return {'erro': 'ID inválido'}, 404
            return jogador
        
        jogadores = self.service.listar_jogadores()
        return [{**marshal(j, jogador_list_fields), 'total_caixas': len(j.caixas or []), 'tem_equipe': j.equipe is not None} 
                for j in jogadores], 200
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nome', type=str, required=True)
        parser.add_argument('idade', type=int, required=True)
        args = parser.parse_args()
        
        try:
            jogador = self.service.criar_jogador(args['nome'], args['idade'])
            return marshal(jogador, jogador_fields), 201
        except ValueError as e:
            return {'erro': str(e)}, 400
    
    def put(self, jogador_id):
        parser = reqparse.RequestParser()
        parser.add_argument('nome', type=str)
        parser.add_argument('idade', type=int)
        args = parser.parse_args()
        
        try:
            jogador = self.service.atualizar_jogador(jogador_id, args.get('nome'), args.get('idade'))
            return marshal(jogador, jogador_fields), 200
        except ValueError as e:
            return {'erro': str(e)}, 400
    
    def delete(self, jogador_id):
        try:
            self.service.deletar_jogador(jogador_id)
            return {}, 204
        except ValueError:
            return {'erro': 'ID inválido'}, 404

