from sns_boomerang.api.resources.topics import ScheduleJob, Subscriptions, Topics
from sns_boomerang.common.items import Job, Topic, TopicSubscriptions, sns_resource
import pytest
from unittest import mock
from werkzeug.exceptions import NotFound, BadRequest
from .conftest import test_topic
from app import app
import json


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


def test_post_job_with_bad_naming():
    with pytest.raises(BadRequest):
        ScheduleJob.post('BAD_TOPIC')


def test_post_job_with_wrong_status(client):
    response = post_json(
        client, '/topics/good-topic/schedule', {'key': 'value'})
    print(response)
    assert response.status_code == 400


def test_schedule_job_post(client, monkeypatch):
    def mock_add_or_update(self):
        pass

    monkeypatch.setattr(Job, 'add_or_update', mock_add_or_update)

    response = post_json(client,
                         '/topics/good-topic/schedule',
                         {'is_valid': 1, 'payload': 'pay load', 'time_due': 1})

    assert response.status_code == 201


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


def test_list_topic_subscriptions(setup_topic_resource):
    response = Subscriptions.get(test_topic)
    assert response[0]
    assert response[1] == 200
