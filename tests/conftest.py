import pytest
from sns_boomerang.common.items import sns_client, sns_resource, Topic, TopicSubscriptions, TOPIC_TABLE


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
