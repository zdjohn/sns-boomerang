from sns_boomerang.api.resources.topics import ScheduleJob, Subscriptions, Topics
from sns_boomerang.common.items import Job, Topic, TopicSubscriptions, sns_resource
import pytest
from unittest import mock
from werkzeug.exceptions import NotFound, BadRequest


def test_post_job_with_bad_naming():
    with pytest.raises(BadRequest):
        ScheduleJob.post('BAD_TOPIC')


def test_get_topic_with_bad_naming():
    with pytest.raises(BadRequest):
        Topics.get('BAD_TOPIC')


def test_get_topic_details(monkeypatch):
    test_topic = 'test-topic'

    def mock_topic_get(topic):
        topic == test_topic
        return Topic(test_topic, 'test_arn')

    monkeypatch.setattr(Topic, 'get', mock_topic_get)
    response = Topics.get(test_topic)

    assert response[0]
    assert response[1] == 200
