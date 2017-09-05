from flask_restplus import Resource, Namespace
from sns_boomerang.common.items import Job, Topic, TopicSubscriptions
from flask import request
import sns_boomerang.settings.util as util

# todo: use marshal_with decorator


from .schemas import *

ns = Namespace('topics', description='schedule job')

job = ns.model('Job', model=job_request_model())
subscriber = ns.models('Subscriber', module=subscriber_request_model())


@ns.route('/<string:topic>/schedule')
@ns.param('topic', 'topic name: topic excepts \'a-z\', \'-\' and \'0-9\' only')
class ScheduleJob(Resource):

    @staticmethod
    @ns.expect(job, validate=True)
    def post(topic):
        if not util.letters_and_numbers_only(topic):
            return 'bad topic name, topic excepts \'a-z\' and \'-\' and \'0-9\' only ', 400
        json_request = request.json
        if not json_request.get('is_valid') in [0, 1]:
            return 'is_valid, could only be either 0 or 1'
        json_request['topic'] = topic
        job_request = Job(**json_request)
        job_request.add_or_update()
        return {'id': job_request.id}, 201


@ns.route('/<string:topic>')
@ns.param('topic', 'topic name')
class Topics(Resource):
    @staticmethod
    def get(topic):
        """
        get topic by topic name
        :param topic: topic name
        :return:
        """
        if not util.letters_and_numbers_only(topic):
            return 'bad topic name, topic excepts \'a-z\' and \'-\' and \'0-9\' only ', 400
        topic_item = Topic.get(topic)
        if topic_item:
            return topic_item.__dict__, 200
        return 404


@ns.route('/<string:topic>/subscriptions')
@ns.param('topic', 'topic name')
class Subscriptions(Resource):
    @staticmethod
    def get(topic):
        subscriptions = TopicSubscriptions(topic)
        return subscriptions.lists(), 200


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

