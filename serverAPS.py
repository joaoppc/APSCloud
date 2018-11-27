#!/usr/bin/env python

from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'joaoppc':
        return 'python'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'mensagem': 'Acesso não autorizado'}), 403)

tarefas = [
    {
        'id': 1,
        'titulo': u'Compras',
        'descricao': u'Queijo, Energetico',
        'done': False
    },
    {
        'id': 2,
        'titulo': u'Cebolinha',
        'descricao': u'Monica sua fecha a polta',
        'done': False
    }
]

task_fields = {
        'titulo': fields.String,
        'descricao': fields.String, 
        'done': fields.Boolean, 
        'uri': fields.Url('tarefas')
}

class Tarefas():
    def __init__(self, titulo, descricao, done=False):
        self.id = tarefas[len(tarefas)-1]['id']+1
        self.titulo = titulo
        self.descricao = descricao
        self.done = done

        tarefa = {'id':self.id,
        'titulo':self.titulo,
        'descricao':self.descricao,
        'done':self.done
        }

        tarefas.append(tarefa)

app = Flask(__name__, static_url_path="")
api = Api(app)

class Healthy(Resource):
    decorators = [auth.login_required]

    def get(self):
        return 200

class ListaTarefasAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('titulo', type=str, required=True, help='Título não fornecido', location='json')
        self.reqparse.add_argument('descricao', type=str, default="", location='json')
        self.reqparse.add_argument('done', type=bool, location='json')
        super(ListaTarefasAPI, self).__init__()

    def get(self):
        return {'tarefas': [marshal(tarefas, task_fields) for tarefas in tarefas]}

    def post(self):
        args = self.reqparse.parse_args()
        if args['done'] is None:
            done = False
        else:
            done = args['done']
        tarefa = Tarefas(args['titulo'], args['descricao'], done)
        del tarefa
        return {'tarefas': marshal(tarefas, task_fields)}, 201

class TarefasAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('titulo', type=str, location='json')
        self.reqparse.add_argument('descricao', type=str, location='json')
        self.reqparse.add_argument('done', type=bool, location='json')
        super(TarefasAPI, self).__init__()

    def get(self, id):
        tarefa = [tarefa for tarefa in tarefas if tarefa['id'] == id]
        if len(tarefa) == 0:
            abort(404)
        return {'tarefas': marshal(tarefa[0], task_fields)}

    def put(self, id):
        tarefa = [tarefa for tarefa in tarefas if tarefa['id'] == id]
        if len(tarefa) == 0:
            abort(404)
        tarefa = tarefa[0]
        args = self.reqparse.parse_args()
        for i, j in args.items():
            if j is not None:
                tarefa[i] = j
        return {'tarefas': marshal(tarefa, task_fields)}

    def delete(self, id):
        tarefas = [tarefas for tarefas in tarefas if tarefas['id'] == id]
        if len(tarefas) == 0:
            abort(404)
        tarefas.remove(tarefas[0])
        return {'resultado': True}

api.add_resource(ListaTarefasAPI, '/Tarefa', endpoint='tarefas')
api.add_resource(TarefasAPI, '/Tarefa/<int:id>', endpoint='tarefa')
api.add_resource(Healthy, '/healthcheck', endpoint='health')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


