#exemplo 


from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth
import json
import pyrebase


app = Flask(__name__, static_url_path="")
api = Api(app)



config = {
    "apiKey": "AIzaSyAD7XaGs_117Naof60BnP2opuHqo-udAiQ",
    "authDomain": "projeto-cloud-29792.firebaseapp.com",
    "databaseURL": "https://projeto-cloud-29792.firebaseio.com",
    "projectId": "projeto-cloud-29792",
    "storageBucket": "projeto-cloud-29792.appspot.com",
    "messagingSenderId": "567778841974"
  }

firebase = pyrebase.initialize_app(config)

db = firebase.database()



task_fields = {
    'title': fields.String,
    'description': fields.String,
    'done': fields.Boolean,
    'uri': fields.Url('task')
}
class Healthy(Resource):

    def get(self):
        return 200

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return json.dumps(db.child("tasks").get().val())


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    return jsonify({'task': make_public_task(task[0])})


@app.route('/tasks', methods=['POST'])
def create_task():
    db.child('tasks').push({'id':1})
    db.child('tasks').push({'title':'Buy groceries'})
    db.child('tasks').push({'description' :'milk, pizza, eggs'})
    db.child('tasks').push({'done': False})
    return 200


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    db.child('tasks').update({'id':1})
    db.child('tasks').update({'title':'Buy groceries'})
    db.child('tasks').update({'description' :'milk, pizza, eggs'})
    db.child('tasks').update({'done': False})
    return 200


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    db.child('tasks').delete({'id':1})
    db.child('tasks').delete({'title':'Buy groceries'})
    db.child('tasks').delete({'description' :'milk, pizza, eggs'})
    db.child('tasks').delete({'done': False})
    return 200



api.add_resource(Healthy, '/healthcheck', endpoint='health')


if __name__ == '__main__':
    app.run(debug=True)




    def get(self):
        print(db.child("tasks").get().val())
        return json.dumps(db.child("tasks").get().val())

