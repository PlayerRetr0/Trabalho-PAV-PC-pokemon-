from flask_restful import fields

caixa_resumo_fields = {
    'id': fields.Integer,
    'nome': fields.String,
}

jogador_fields = {
    'id': fields.Integer,
    'nome': fields.String,
    'idade': fields.Integer,
    'caixas': fields.List(fields.Nested(caixa_resumo_fields), attribute='caixas', default=[]),
    'equipe_id': fields.Integer(attribute='equipe.id', default=None),
}

jogador_list_fields = {
    'id': fields.Integer,
    'nome': fields.String,
    'idade': fields.Integer,
    'equipe_id': fields.Integer(attribute='equipe.id', default=None),
}


