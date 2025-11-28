from flask_restful import fields

caixa_fields = {
    'id': fields.Integer,
    'nome': fields.String,
    'jogador_id': fields.Integer
}

caixa_list_fields = {
    'id': fields.Integer,
    'nome': fields.String,
    'jogador_id': fields.Integer,
    'jogador_nome': fields.String(attribute='jogador.nome'),
    'total_pokemons': fields.Integer
}




