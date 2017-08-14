from flask_restplus import Api
from .topics import ns as topics
from .jobs import ns as jobs

api = Api(title='sns boomerang', description='serverless sns scheduler with lambda', doc='/doc/')

api.add_namespace(topics)
api.add_namespace(jobs)
