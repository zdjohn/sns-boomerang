from flask_restplus import Resource, Namespace
from sns_boomerang.common.items import TopicSubscriptions
from flask import request
from .schemas import *

ns = Namespace('subscribers', description='schedule job')
subscriber = ns.model('Subscriber', model=subscriber_request_model())


@ns.route('/<string:topic>/lambda')
@ns.param('topic', 'topic name')
class LambdaSubscription(Resource):
    @staticmethod
    @ns.expect(subscriber, validate=True)
    def post(topic):
        subscriptions = TopicSubscriptions(topic)
        json_request = request.json
        endpoint = json_request.get('endpoint')
        if endpoint:
            response = subscriptions.add(subscription_type='lambda', endpoint=endpoint)
            #todo: add to dynamo to persist
            return response
        else:
            return 'endpoint is required', 400
