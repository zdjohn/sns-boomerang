from sns_boomerang.common.items import Job, JOB_TABLE
import pytest


def test_new_job():
    job = Job('topic', 'payload', 123)
    assert job.id
    assert job.topic == 'topic'
    assert job.payload == 'payload'


def test_add_or_update(monkeypatch):

    def mock_put_item(Item, **kwargs):
        assert Item['topic'] == 'topic'

    monkeypatch.setattr(JOB_TABLE, 'put_item', mock_put_item)
    job = Job('topic', 'payload', 123)
    job.add_or_update()


@pytest.mark.parametrize("test_input, status, check, expected", [
    ("active-job", 1, True, True),
    ("not-active-check-status", 0, True, False),
    ("not-active-check-status", 0, False, True)
])
def test_job_get_by_id_status(test_input, status, check, expected, monkeypatch):
    def mock_get_item(Key, **kwargs):
        assert Key['id'] == test_input
        return {'Item': {'topic': test_input, 'payload': 'payload', 'time_due': 111, 'is_valid': status}}

    monkeypatch.setattr(JOB_TABLE, 'get_item', mock_get_item)

    job = Job.get(test_input, check)
    if expected:
        assert job.topic == test_input
    else:
        assert job == None
