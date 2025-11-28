from flask_restful import fields

equipe_fields = {
    'id': fields.Integer,
    'jogador_id': fields.Integer
}

equipe_list_fields = {
    'id': fields.Integer,
    'jogador_id': fields.Integer,
    'jogador_nome': fields.String(attribute='jogador.nome'),
    'total_pokemons': fields.Integer
}

pokemon_equipe_fields = {
    'id': fields.Integer,
    'raca': fields.String(attribute='raca.value'),
    'tipo': fields.String(attribute='tipo.value'),
    'nome': fields.String,
    'genero': fields.Boolean,
    'level': fields.Integer
}

equipe_detalhada_fields = {
    'id': fields.Integer,
    'jogador_id': fields.Integer,
    'jogador_nome': fields.String(attribute='jogador.nome'),
    'pokemons': fields.List(fields.Nested(pokemon_equipe_fields))
}

