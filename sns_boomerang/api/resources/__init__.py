from flask_restplus import Api
from .topics import ns as topics
from .jobs import ns as jobs
from .subscriber import ns as subscribers

api = Api(title='sns boomerang', description='serverless sns scheduler with lambda', doc='/doc/')

api.add_namespace(topics)
api.add_namespace(jobs)
api.add_namespace(subscribers)
