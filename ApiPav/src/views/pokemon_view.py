from flask_restful import fields

pokemon_fields = {
    'id': fields.Integer,
    'raca': fields.String(attribute='raca.value'),
    'tipo': fields.String(attribute='tipo.value'),
    'nome': fields.String,
    'genero': fields.Boolean,
    'level': fields.Integer
}

pokemon_list_fields = {
    'id': fields.Integer,
    'raca': fields.String(attribute='raca.value'),
    'tipo': fields.String(attribute='tipo.value'),
    'nome': fields.String,
    'genero': fields.Boolean,
    'level': fields.Integer,
    'caixa_id': fields.Integer(attribute='caixa.id', default=None),
    'equipe_id': fields.Integer(attribute='equipe.id', default=None)
}

