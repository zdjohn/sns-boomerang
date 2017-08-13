import boto3
import hashlib
from datetime import datetime
import json
from sns_boomerang.settings import *
from boto3.dynamodb.conditions import Key
from enum import Enum
from decimal import *

dynamo = boto3.resource('dynamodb')
sns_resource = boto3.resource('sns')
sns_client =boto3.client('sns')
JOB_TABLE = dynamo.Table(TABLE_JOBS)
TOPIC_TABLE = dynamo.Table(TABLE_TOPICS)
# TOPIC_SUBSCRIBER_TABLE = dynamo.Table(TABLE_SUBSCRIBERS)


class SubscriptionType(Enum):
    """subscription type that is supported"""
    API = 'api'
    LAMBDA = 'lambda'


def _compute_default_hash(payload, version, topic, time_due):
    m = hashlib.md5()
    m.update('{}{}{}{}'.format(payload, version, topic, time_due).encode('utf-8'))
    return m.hexdigest()


class Job(object):
    """
    job class
    """
    def __init__(self, topic, payload, time_due, id='', version=1, is_valid=1, time_scheduled=None, **kwargs):
        """
        :type id: string
        """
        self.topic = topic
        self.payload = payload
        self.time_due = time_due
        self.version = version
        self.is_valid = is_valid
        self.time_scheduled = time_scheduled or Decimal(datetime.utcnow().timestamp())
        self.id = id or _compute_default_hash(payload, version, topic, time_due)

    def add_or_update(self):
        """update to add scheduled job"""
        self.time_scheduled = Decimal(datetime.utcnow().timestamp())
        JOB_TABLE.put_item(Item=self.__dict__)

    @classmethod
    def get(cls, id, check_active_status=False):
        """get job by id"""
        item_response = JOB_TABLE.get_item(
            Key={'id':id, 'is_valid':1}
        )
        if item_response.get('Item'):
            item = item_response['Item']
            if not check_active_status or item.get('is_active'):
                return cls(**item)

    @classmethod
    def from_stream_record(cls, record):
        """get job by dynamo stream image"""
        parsed_values = {
            'id': record.get("id", {}).get('S', ''),
            'version': record.get("version", {}).get('N', 1),
            'payload': record.get("payload", {}).get('S', ''),
            'topic': record.get("topic", {}).get('S', ''),
            'time_due': record.get("time_due", {}).get('N', 0),
            'time_scheduled': record.get("time_scheduled", {}).get('N', 0),
            'is_valid': record.get("is_valid", {}).get('N', 0)
        }
        return cls(**parsed_values)

    @staticmethod
    def flush():
        """

        :return:
        """
        current = Decimal(datetime.utcnow().float_timestamp)
        jobs_response = JOB_TABLE.query(
            IndexName='is_valid-time_due-index',
            KeyConditionExpression=Key('is_valid').eq(1) & Key('time_due').lt(current)
        )
        items = jobs_response.get('Items')
        if items:
            with JOB_TABLE.batch_writer() as batch:
                for i in items:
                    batch.delete_item(Key={'id': i.get('id'), 'is_valid': 1})

    def publish(self):
        """
        sns_resource could only accept json object in message
        :param topic_arn: arn
        :param payload: string of json payload
        :param version: default version to 1
        :return:
        """
        job_topic = Topic.get(self.topic)

        if not job_topic.arn:
            print('arn can not be none')
            return
        if not self.payload:
            print('payload can not be none')
            return
        message = json.dumps({'payload': json.loads(self.payload)})
        sns_client.publish(
            TopicArn=job_topic.arn,
            Message=json.dumps({
                'default': message,
                'version': self.version
            }),
            MessageStructure='json'
        )


class Topic(object):
    """
    topic class 
    """
    def __init__(self, topic, arn='', time_updated=None, is_active=True):
        self.time_updated = time_updated or datetime.utcnow().timestamp
        self.topic = topic
        self.arn = arn
        self.is_active = is_active

    @classmethod
    def get(cls, topic, check_is_active=False):
        """get topic by topic name"""
        item_response = TOPIC_TABLE.get_item(Key={'topic':topic})
        if item_response.get('Item'):
            item = item_response['Item']
            if not check_is_active or item.get('is_active'):
                return cls(**item)

    def add_or_update(self):
        """
        update or add current topic
        :return:
        """
        self.arn = self.arn or self._create_sns_topic_arn(self.topic)
        self.time_updated = datetime.utcnow().timestamp
        TOPIC_TABLE.put_item(Item=self.__dict__)

    @staticmethod
    def _create_sns_topic_arn(sns_topic):
        topic_response = sns_client.create_topic(
            Name=sns_topic
        )
        if topic_response:
            return topic_response.get('TopicArn', '')


class TopicSubscriptions(object):
    """
    subscription per topic
    """
    def __init__(self, topic):
        topic = Topic.get(topic, check_is_active=True)
        if topic:
            self.topic = sns_resource.Topic(topic.arn)
        raise NameError("topic: {} dose not exists".format(topic))

    def lists(self):
        """
        list all subscription
        """
        subscription_iterator = self.topic.subscriptions.all()
        return subscription_iterator

    def add(self, subscription_type=SubscriptionType.API, endpoint=''):
        """
        add subscriptions by type
        """
        switcher = {
            SubscriptionType.API: self._add_https,
            SubscriptionType.LAMBDA: self._add_lambda
        }
        response = switcher[subscription_type](endpoint)
        return response

    def remove(self, subscription_arn):
        """remove subscription by arn"""
        subscription = sns_resource.Subscription(subscription_arn)
        subscription.delete()

    def _add_https(self, endpoint):
        self.topic.subscribe(Protocol='https', Endpoint=endpoint)

    def _add_lambda(self, lambda_arn):
        self.topic.subscribe(Protocol='lambda', Endpoint=lambda_arn)


if __name__ == '__main__':
    # j = Job.flush()
    pass
