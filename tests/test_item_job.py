from sns_boomerang.common.items import sns_client, Job, Topic, JOB_TABLE
from contextlib import contextmanager
import pytest
from unittest.mock import MagicMock
from datetime import datetime


def test_new_job():
    job = Job('topic', 'payload', 123)
    assert job.id
    assert job.topic == 'topic'
    assert job.payload == 'payload'


def test_add_or_update(monkeypatch):

    def mock_put_item(Item, **kwargs):
        assert Item['topic'] == 'topic'
        assert Item['time_scheduled'] > 0

    # mock_datetime = datetime.now()
    # monkeypatch.setattr(datetime, 'utcnow', mock_datetime)
    monkeypatch.setattr(JOB_TABLE, 'put_item', mock_put_item)
    job = Job('topic', 'payload', 123)
    job.add_or_update()


@pytest.mark.parametrize("test_input, status, check, expected", [
    ("active-job", 1, True, True),
    ("not-active-check-status", 0, True, False),
    ("not-active-check-status", 0, False, True)
])
def test_job_get_by_id_status(test_input, status, check, expected, monkeypatch):
    topic_name = f'{test_input}-topic'

    def mock_get_item(Key, **kwargs):
        assert Key['id'] == test_input
        return {'Item': {'topic': topic_name, 'payload': 'payload', 'time_due': 111, 'is_valid': status}}

    monkeypatch.setattr(JOB_TABLE, 'get_item', mock_get_item)

    job = Job.get(test_input, check)
    if expected:
        assert job.topic == topic_name
    else:
        assert job == None


def test_job_flush(monkeypatch):
    test_key_id = 'x'

    class batch_mock:
        def delete_item(self, Key):
            assert Key['id'] == test_key_id

    @contextmanager
    def mock_managed_context(*args, **kwds):
        try:
            yield batch_mock()
        finally:
            pass

    def mock_query(IndexName, KeyConditionExpression, **kwargs):
        assert IndexName == 'is_valid-time_due-index'
        assert KeyConditionExpression is not None
        return {'Items': [{'id': test_key_id, 'is_valid': 1}]}

    monkeypatch.setattr(JOB_TABLE, 'query', mock_query)

    monkeypatch.setattr(JOB_TABLE, 'batch_writer', mock_managed_context)

    Job.flush()


def test_job_publish_success(monkeypatch):
    mock_topic = Topic('x', arn='existing')
    mock_job = Job('x', '{"a": "b"}', 123)

    def mock_publish(TopicArn, Message, MessageStructure, **kwargs):
        assert MessageStructure == 'json'

    def mock_topic_get(topic_name):
        assert topic_name == 'x'
        return mock_topic

    monkeypatch.setattr(Topic, 'get', mock_topic_get)
    monkeypatch.setattr(sns_client, 'publish', mock_publish)

    mock_job.publish()
