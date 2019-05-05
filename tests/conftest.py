import pytest
from sns_boomerang.common.items import sns_client, sns_resource, Topic, TopicSubscriptions, TOPIC_TABLE
from app import app
import json


test_topic = 'test_topic_name'
test_topic_arn = 'test_topic_arn'
test_sub_arn = 'test-sub-arn'
test_protocol = 'test-protocol-value'
test_endpoint = 'test-endpoint-value'

test_subscibers_list = ['subscription', 'iterator']


class MockSubscriptions():
    def all(self):
        return test_subscibers_list


class MockTopic():
    def __init__(self, arn):
        self.subscriptions = MockSubscriptions()

    def subscribe(self, Protocol, Endpoint):
        assert Protocol == test_protocol
        assert Endpoint == test_endpoint
        return True

    def add_or_update(self):
        return {'topic': 'moked_item'}


class MockSub():
    def __init__(self, arn):
        self.is_deleted = False
        self.arn = arn

    def delete(self):
        self.is_deleted = True


mock_topic = Topic(test_topic, arn=test_topic_arn)


sub_mock = MockSub(test_sub_arn)


@pytest.fixture(scope='function')
def setup_topic_resource(monkeypatch):

    def mock_topic_get(topic_name, check_is_active):
        assert topic_name == test_topic
        assert check_is_active == True
        return mock_topic

    def mock_boto3_topic_resource(arn):
        assert arn == test_topic_arn
        return MockTopic(arn)

    def mock_get_sub(sub_arn):
        assert sub_arn == test_sub_arn
        return sub_mock

    monkeypatch.setattr(Topic, 'get', mock_topic_get)
    monkeypatch.setattr(sns_resource, 'Topic', mock_boto3_topic_resource)
    monkeypatch.setattr(sns_resource, 'Subscription', mock_get_sub)


@pytest.fixture
def client(request):
    test_client = app.test_client()

    def teardown():
        pass  # databases and resourses have to be freed at the end. But so far we don't have anything

    request.addfinalizer(teardown)
    return test_client


def post_json(client, url, json_dict):
    """Send dictionary json_dict as a json to the specified url """
    return client.post(url, data=json.dumps(json_dict), content_type='application/json')


def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))
