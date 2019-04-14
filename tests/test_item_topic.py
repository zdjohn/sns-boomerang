from sns_boomerang.common.items import sns_client, Job, Topic, TOPIC_TABLE
import pytest
from datetime import datetime


@pytest.mark.parametrize("test_input, status, check, expected", [
    ("active-topic", 1, True, True),
    ("not-active-check-status", 0, True, False),
    ("not-active-no-check-status", 0, False, True)
])
def test_topic_get(test_input, status, check, expected, monkeypatch):
    topic_name = 'x'

    def mock_get_item(Key, **kwargs):
        assert Key['topic'] == test_input
        return {'Item': {'topic': topic_name, 'arn': 'payload', 'is_active': status}}

    monkeypatch.setattr(TOPIC_TABLE, 'get_item', mock_get_item)

    topic_result = Topic.get(test_input, check)
    if expected:
        assert topic_result.topic == topic_name
        assert topic_result.time_updated
    else:
        assert topic_result == None


def test_topic_add_or_update(monkeypatch):
    test_topic_name = 'test_name_value'
    mock_topic_arn = 'arn_value'

    def mock_create_topic(Name):
        assert Name == test_topic_name
        return {'TopicArn': mock_topic_arn}

    def mock_put_item(Item):
        assert Item['arn'] == mock_topic_arn
        assert Item['time_updated']
        assert Item['topic'] == test_topic_name

    monkeypatch.setattr(sns_client, 'create_topic', mock_create_topic)
    monkeypatch.setattr(TOPIC_TABLE, 'put_item', mock_put_item)

    test_topic = Topic(test_topic_name)
    topic = test_topic.add_or_update()

    assert topic['arn'] == mock_topic_arn
